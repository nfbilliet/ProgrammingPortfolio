from h5py import File as f
import numpy as np
import os
import gqcml

def extract_overview(modelbase_name, error_filenames, meta_filenames,error_dir, meta_dir, summary_dir):
    """
    A formatting function that processes a set of error files and meta files that will be combined into
    an overview file which gathers the hyperparameters and the test set performance into a summary file
    into a latex tabular format.

    Arguments
        :error_filenames (list): A list containing a set of sorted filenames that corresponds to the 
                                    task array. This sorting is the same for the meta filenames
        :meta_filenames (list): A list containing a set of sorted filenames that corresponds to the
                                    task array. This sorting is the same for the meta filenames
        :error_dir (str/filepath): A string that contains the filepath to the collected error files
        :meta_dir (str/filepath): A string that contains the filepath to the collected meta files
        :summary_dir (str/filepath): A string that contains the filepath to the directory where the summary 
                                        should be written too
    Return
        :None: The information is added to the to the summary file.
    """
    means = []
    variances = []
    embedding = []
    graph_conv = []
    filter_layers = []
    node_prop = []
    for error_filename, meta_filename in zip(error_filenames, meta_filenames):
        metadict_path=os.path.join(meta_dir, meta_filename)
        testfile_path=os.path.join(error_dir, error_filename)
        metadict = gqcml.meta.format.load_meta(metadict_path)
        testfile = f(testfile_path, "r")
        embedding.append((len(metadict["Model"]["Embedding"]["Layer configuration"]),
                          metadict["Model"]["Embedding"]["Layer configuration"][0][1]))
        graph_conv.append((len(metadict["Model"]["Graph Convolution"]["Graph Conv configuration"]),
                           metadict["Model"]["Graph Convolution"]["Graph Conv configuration"][0][0]))
        filter_layers.append(metadict["Model"]["Graph Convolution"]["Number of filter layers per GC layer"])
        node_prop.append((len(metadict["Model"]["Node property"]["Layer configuration"]),
                          metadict["Model"]["Node property"]["Layer configuration"][0][0]))
        means.append(float(np.array(testfile["error mean"])))
        variances.append(float(np.array(testfile["error variance"])))
        testfile.close()
    overview_file=open(os.path.join(summary_dir,modelbase_name+"_summary.txt"), "w")
    table_overview = np.array([embedding, graph_conv, filter_layers, node_prop, means, variances]).T
    for line in table_overview:
        tablerow = ""
        for el in line[:-1]:
            tablerow = tablerow + str(el) + "&"
        tablerow = tablerow + str(line[-1])
        overview_file.write(tablerow+"\n")
    overview_file.close()
