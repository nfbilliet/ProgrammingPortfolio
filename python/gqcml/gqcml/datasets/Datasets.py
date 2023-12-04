import os
import torch
import torch_geometric
import numpy as np
from gqcml.data import Data
from h5py import File as f
from sklearn.model_selection import train_test_split

def bin_values(target_values, num_bins):
    """
    A function to partition a continuous target variable into discrete bins. This function is intended
    to work together with the train_test_split functionality from sklearn.model_selection to partition the
    dataset into representative training, validation and test data by ensuring that target values are equally 
    represented

    Arguments
        :target_values (np.array): A 2D numpy array containing the continuous target values of the dataset.
                                     Each row represents the target value of a datapoint
        :num_bins (int): An integer that determines the number of output classes that the function returns
    Returns
        :binned_values (np.array): A 2D array where the values of the input array have been classified into
                                      discrete bins determined by the minimum and maximum of the input array.
    """
    min_value = np.amin(target_values)
    max_value = np.amax(target_values)
    #A small perturbation is added to the boundary values to ensure that all bins contain more than 1 datapoint
    bins = np.linspace(min_value-(0.001*min_value),max_value+(0.001*max_value),num_bins)
    return np.digitize(target_values, bins)

def split_dataset(input_values, target_values, data_frac, seed,
                  stratify=True, num_bins=10, shuffle=True, return_output=True):
    """
    A function that splits a dataset into a training, validation and test set.

    Arguments
        :input_values (np.array): A 2D numpy array containing the input values of the dataset. Each row represents an input vector of the dataset.
        :output_values (np.array): A 2D numpy array containing the continuous target values of the dataset.
                                     Each row represents the target value of a datapoint.
        :data_frac (float): The fraction of the dataset that should be reserved for the validation and test set. 
                              This fraction will be split in half for both these sets.
        :seed (int): The random seed used to determine the split of the dataset.
        :stratify (opt,bool): Option to partition the dataset according to the distribution of the target values. This option
                                       ensures that all the sets follow the same distribution in their target.
        :num_bins (opt,int): An integer that determines the number of output classes
        :shuffle (opt,bool): Option to shuffle the dataset before partitioning it into a training, validation and test set.
    Returns
        :inputs, outputs (tuple): The function returns a tuple of the split dataset in the order of input data followed by output data.
                                     The order in which this happens is training, validation and test set
    """
    if stratify is True:
        binned_target = bin_values(target_values, num_bins)
        train_input, valtest_input, train_output, valtest_output = train_test_split(input_values, target_values,
                                                                                    test_size=data_frac, random_state=seed,
                                                                                    stratify=binned_target, shuffle=shuffle)
        binned_valtest = bin_values(valtest_output, num_bins)
        val_input, test_input, val_output, test_output = train_test_split(valtest_input, valtest_output, test_size=0.5,
                                                                          stratify=binned_valtest, random_state=seed,
                                                                          shuffle=shuffle)
        if return_output:
            return train_input, val_input, test_input, train_output, val_output, test_output
        else:
            return train_input, val_input, test_input
    else:
        train_input, valtest_input, train_output, valtest_output = train_test_split(input_values, target_values,
                                                                                    test_size=data_frac, random_state=seed,
                                                                                    shuffle=shuffle)
        val_input, test_input, val_output, test_output = train_test_split(valtest_input, valtest_output, test_size=0.5,
                                                                          random_state=seed, shuffle=shuffle)
        if return_output:
            return train_input, val_input, test_input, train_output, val_output, test_output
        else:
            return train_input, val_input, test_input

def QM9_index_splitter(indices, seed, data_frac, shuffle=True):
    train_indices, valtest_indices = train_test_split(indices, test_size=data_frac, random_state=seed, shuffle=shuffle)
    val_indices, test_indices = train_test_split(valtest_indices, test_size=0.5, random_state=seed, shuffle=shuffle)
    return train_indices, val_indices, test_indices

def QM9_dataloader(root_dir, indices, target_descr, batch_size, shuffle=True):
    data_name = "QM9_"+target_descr
    processed_dir = os.path.join(root_dir, "processed")
    filenames = [os.path.join(processed_dir, data_name+"_{}.pt".format(idx)) for idx in indices]
    dataset = [torch.load(filename) for filename in filenames]
    return torch_geometric.data.DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

def trius_to_inputs(trius, preprocessor, am_args,
                    preprocessor_nf_method, nf_args):
    """
    A function that interacts with the preprocessor class defined in the Data section of gqcml.
    The function takes as stack of upper triangle values and converts them to their matrix representation.
    Following the conversion to matrices we utilize methods defined in the preprocessor class to
    convert the matrices to a suitable input for graph neural networks. The different methods that are
    defined are 

        1) (categorical) degree node feature
        2) weight node feature
        3) weighted categorical degree
        4) weighted categorical pair degree 

    Arguments
        :trius (np.array): A numpy array containing the trius of the graphs that are to be processed. This
                             array has the dimension (K x M) where K is the number of graphs contained in the 
                             dataset and M=N(N-1)/2 with N the number of vertices in the graph
        :preprocessor_am_method (gqcml.data.Data): A function from the Preprocessor class that processes
                                                     the matrices to the adjacency matrices
        :am_args (list): The list of function arguments (excluding the input matrix) for the am_method.
                           When no arguments need to specified the input should be an empty list
        :preprocessor_nf_method (gqcml.data.Data.Preprocessor): A function from the Preprocessor class that
                                                                  processes the matrices into the desired node
                                                                  feature class
        :nf_args (list): The list of function arguments (excluding the input matrix) for the nf_method.
                           When no arguments need to specified the input should be an empty list
        :args (list): The arguments for the preprocessor_method excluding the matrix to be processed.
    Returns
        :node_features, adjacency_matrices: Returns the processed node features and the adjacency matrices
    """
    matrices = np.array([preprocessor.triu_to_matrix(triu) for triu in trius])
    node_features, adjacency_matrices  = [], []
    for matrix in matrices:
        am = preprocessor.adjacency_matrix(matrix, *am_args)
        nf = preprocessor_nf_method(matrix, *nf_args)
        node_features.append(nf)
        adjacency_matrices.append(am)
    return np.array(node_features), np.array(adjacency_matrices)
    
def DataLoader_constructor(input_tensors, output_tensors, batch_size, shuffle=True,
                           pin_memory=False, num_workers=0):
    """
    A function that takes in a set of input tensors and a set of output tensor and 
    constructs a data loader that can be used in the optimization of network.

    Arguments
        :input_tensors (list of torch.Tensor): A list of input tensors
        :output_tensors (torch.Tensor): A tensor that contains the corresponding output tensors
        :batch_size (int): An integer that determines the number of tensors in each batch 
        :shuffle (opt, bool): A boolean that enables the option to shuffle the data during batch iteration
        :pin_memory (opt, bool): A boolean that enables the option to pin memory in the GPUs utilized during training.
                                   This allows for faster data transfer
        :num_workers (opt, int): An integer that controls how many subprocesses to use for data loading. 
                                   0 means that the data will be loaded in the main process
    Returns
        :loader (torch.data.DataLoader): A DataLoader object that returns batch objects  
    """
    if type(input_tensors) is list:
        input_tensors = [torch.from_numpy(stack).double() for stack in input_tensors]
        output_tensors = torch.from_numpy(output_tensors).double().reshape(-1,1)
        dataset = torch.utils.data.TensorDataset(*input_tensors, output_tensors)
        loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=shuffle,
                                             pin_memory=pin_memory, num_workers=num_workers)
        return loader
    else:
        input_tensors = torch.from_numpy(input_tensors).double()
        output_tensors = torch.from_numpy(output_tensors).double().reshape(-1,1)
        dataset = torch.utils.data.TensorDataset(input_tensors, output_tensors)
        loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=shuffle,
                                             pin_memory=pin_memory, num_workers=num_workers)
        return loader


