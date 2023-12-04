import math
import numpy as np
import os
import torch
import torch_geometric
import h5py
from gqcml.datasets import Datasets

def graph_to_Data(nf, am, output):
    """
    A function that converts a set of tensor to a Data object from torch_geometric

    Arguments
        :nf (torch.Tensor): A tensor containing the node features associated with the graphs
        :am (torch.Tensor): A tensor containing the adjacency matrices describing the graphs
        :output (torch.Tensor): The graph property tensor associated with the graphs
    Returns
        :dp (torch_geometric.data.Data): A data object where the node features are stored in the x attribute of Data.
                                         The adjacency matrix is split into the indices and weights and are stored in their respective attributes
    """
    edge_index, edge_attr = torch_geometric.utils.dense_to_sparse(am)
    dp = torch_geometric.data.Data(x=nf.double(),
                                   edge_index=edge_index.long(),
                                   edge_attr=edge_attr.double(),
                                   y=output.double())
    return dp

def TriuDataset(dim, trius, output_values, residual=False):
    """
    Function to convert a set of trius to a set of datapoints
    """
    node_features, adj_matrices = Datasets.trius_to_graphs(dim, trius, residual=residual)
    if residual:
        adj_matrices += np.eye(dim)
    node_features = torch.from_numpy(node_features)
    adj_matrices = torch.from_numpy(adj_matrices)
    output_values = torch.from_numpy(output_values)
    datapoints = []
    for nf, am, e in zip(node_features, adj_matrices, output_values):
        datapoints.append(graph_to_Data(nf, am, e))
    return datapoints
                          
