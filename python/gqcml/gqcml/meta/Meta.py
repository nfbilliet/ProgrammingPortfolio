import os
import subprocess
import getpass
import git
import platform
import psutil
import re
import numpy as np
import torch
import torch_geometric
import torch_scatter
import torch_sparse
import sklearn
import datetime
import json

def get_script_information(submission_script,
                           meta_dict):
    """
    Function used in the extraction of meta data from a submission script. This function
    is built on the assumption that the SLURM job manager is being used to submit tasks on a
    high performance computing infrastructure.

    Arguments
        :submission_script (str): The filepath to the submission script being used 
        :meta_dict (dictionary): The dictionary in which the meta data needs to be stored.
    Returns
        :None: The information is extracted from the script and appended to the meta dict
    """
    script_dict = {}
    script_dict["User"]=getpass.getuser()
    script_dict["Script name"] = submission_script.split("/")[-1]
    with open(submission_script, "r") as script:
        for line in script:
            if "gpu" in line:
                num_gpus = line.split(":")[1].split("\n")[0]
                script_dict["Number of GPUs"]=num_gpus
            elif "cpus" in line:
                num_cpus = line.split("=")[1].split("\n")[0]
                script_dict["Number of processors"]=num_cpus
            elif "mem" in line:
                mem = line.split("=")[1].split("\n")[0]
                script_dict["Memory"]=mem
            elif "time" in line:
                time = line.split("=")[1].split("\n")[0]
                script_dict["Time"]=time
            elif ".py" in line:
                python_script = line.split(" ")[1].split("\n")[0]
                script_dict["Python script"]=python_script
    meta_dict["Submission script"]=script_dict
    return None

def get_git_information(library_directory,
                        meta_dict):
    """
    Lookup the repository metadata and returns the current active branch and the git commit sha/hash. 
    The information is store

    Arguments
        :library_directory (str): The path to the parent directory of the library from which the 
                                    data needs to be extracted. The directory should end in the parent
                                    directory name (no / at the end).
        :meta_dict (dict): The dictionary in which the meta data needs to be stored. 
    Returns
        :None: The information is extracted and appended to the meta dict
    """
    repo = git.Repo(library_directory)
    repo_name = library_directory.split("/")[-1]
    branch_name = str(repo.active_branch)
    sha = str(repo.head.object.hexsha)
    meta_dict["Git"]={'Repository name':repo_name,
                      'Branch name':branch_name,
                      'Git sha/hash':sha}
    return None
    
def get_system_information(meta_dict):
    """
    Function designed to look up system information and store it in a dictionary format

    Arguments
        :meta_dict (dict): The dictionary in which the meta data needs to be stored.
    Returns
        :None: The information about the system is extracted and appended to the meta dict
    """
    meta_dict["System"]={"Architecture":platform.architecture()[0],
                         "Machine":platform.machine(),
                         "Node":platform.node(),
                         "Platform":platform.platform(),
                         "Python compiler":platform.python_compiler()}
    return None

def get_hardware_information(meta_dict):
    """
    Function designed to look up hardware information and store it in a dictionary format

    Arguments
        :meta_dict (dict): The dictionary in which the meta data needs to be stored
    Returns
        :None: The information about the Hardware is extracted and appended to the meta dict
    """
    processor_name = ""
    out = subprocess.check_output("lscpu", shell=True).decode()
    out = out.split("\n")
    for line in out:
        if line.startswith("Model name"):
            processor_name=line
    #Substitute multiple white spaces with a single with space
    processor_name = re.sub('\s+', ' ', processor_name).split(":")[1:]
    if torch.cuda.is_available():
        meta_dict["Hardware"]={"CPU": processor_name[0][1:],
                               "GPU": str(torch.cuda.get_device_name())}
    else:
        meta_dict["Hardware"]={"CPU": processor_name[0][1:],
                               "GPU": None}
    return None

def get_software_information(meta_dict):
    """
    Function designed to look up software information and store it in a dictionary format

    Arguments
        :param meta_dict (dict): The dictionary in which the meta data needs to be stored
    Returns
        :None: The information about the software is extracted and appended to the meta dict
    """
    meta_dict["Software"]={"Python": platform.python_version(),
                           "Sci-kit learn":sklearn.__version__,
                           "Numpy":np.version.version,
                           "Torch":torch.__version__,
                           "Torch Geometric":torch_geometric.__version__,
                           "Torch Scatter":torch_scatter.__version__,
                           "Torch Sparse": torch_sparse.__version__}
    return None

def get_timestamp(meta_dict):
    """
    A function to retrieve the time stamp of the calculation

    Arguments
        :meta_dict (dict): The dictionary in which the meta data needs to be stored
    Returns
        :None: The information about the time of execution is extracted and appended to the meta dict
    """
    meta_dict["Timestamp"]={"year":str(datetime.datetime.now().year),
                            "month":str(datetime.datetime.now().month),
                            "day":str(datetime.datetime.now().day),
                            "time":str(datetime.datetime.now().time())}
    return None

def get_optimizer_information(meta_dict, optimizer):
    """
    A function to extract all the hyper parameters from the optimizer used during the training
    
    Arguments
        :meta_dict (dict): The dictionary in which the meta data needs to be stored
        :optizimer (torch.optim): Optimizer object from pytorch
    Returns
        :None: The information about the optimizer is extracted and appended to the meta dict
    """
    optim_name = str(optimizer).split("(")[0]
    optim_parameters_keys = [key for key in optimizer.param_groups[0].keys()][1:]
    optim_parameters_values = []
    for key in optim_parameters_keys:
        optim_parameters_values.append(optimizer.param_groups[0][key])
    optim_keys = ["Optimizer name"]+optim_parameters_keys
    optim_vals = [optim_name]+optim_parameters_values
    meta_dict["Optimizer"]=dict(zip(optim_keys,optim_vals))
    return None

def make_meta(meta_dir,
              modelname,
              model,
              optimizer,
              submission_script,
              library_directory,
              dataset,
              random_seed):
    """
    A function that generates a JSON file that contains all the necessary meta data of the calculation that is
    being performed. The JSON file stores
    
        - Script information
        - Git information
        - Model information
        - System information
        - Hardware information
        - Software information
        - Optimizer data
        - Dataset
        - Timestamp
        - Random seed

    Arguments
        :meta_dir (str): A filepath to the target directory where the meta data should be stored.
        :modelname (str):
        :model (gqcml.nn.models/gqcml.torchgeom_interface.models): A torch object that represents the model.
                                                                         This model is required to have the meta function
        :optimizer (torch.optim): The optimizer that is used in the training of the model
        :submission_script (str): The filepath to the submission script being used
        :library_directory (str): The path to the parent directory of the library from which the
                                        data needs to be extracted. The directory should end in the parent
                                        directory name (no / at the end).
        :dataset (str/list): A string containing the filepath to the dataset is being in the model. If multiple 
                                   datasets are used then a filepath to each of these need to be provided in a list
    Returns
        :None: The meta dict is stored in a json file and stored in the meta target dir
    """
    meta_dict={}
    get_script_information(submission_script, meta_dict)
    get_system_information(meta_dict)
    get_hardware_information(meta_dict)
    get_software_information(meta_dict)
    get_git_information(library_directory, meta_dict)
    get_timestamp(meta_dict)
    get_optimizer_information(meta_dict, optimizer)
    meta_dict["Model"]=model.meta()
    meta_dict["Dataset"]=dataset
    meta_dict["Random seed"]=random_seed
    print(meta_dict)
    metafile = os.path.join(meta_dir, modelname+"_meta.json")
    json.dump(meta_dict, open(metafile, "w"))
    
