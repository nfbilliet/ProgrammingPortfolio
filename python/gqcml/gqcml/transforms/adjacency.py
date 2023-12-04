import torch

def binarize(adjacency_matrices):
    """
    A function that converts a weighted adjacency tensor stack to its binarized form. This function can convert a single
    adjacency matrix or a stack of matrices

    :param adj_matrices (torch.tensor): A tensor containing weighted adjacency matrices that has the dimensions
                                        (B x N x N) where B is the batch size/number of graphs (optional dimension)
                                        and N is the number of vertices/nodes in each graph

    :return binary_adj_matrices (torch.tensor): A tensor containing the converted weighted adjacency matrices to their
                                                binarized format
    """
    #Clone the adjacency matrix to avoid changing it
    binary_adj_matrices = adjacency_matrices.clone()
    #Convert all non-zero elements, i.e. the weighted elements to 1
    binary_adj_matrices[binary_adj_matrices!=0]=1.0
    return binary_adj_matrices

def degree(adjacency_matrices, self_loops=True):
    """
    Compute the D^(-1/2) matrix based on the adjacency matrices given

    :param adjacency_matrices (torch.tensor): A tensor containing adjacency matrices (weighted or unweighted)
                                              that has the dimensions (B x N x N) where B is the batch size/number of graphs
                                              and N is the number of vertices/nodes in each graph

    :param self_loops (bool): Option to add self loops to the adjacency matrix, i.e. the unit matrix

    :return degrees (torch.tensor): The diagonal degrees matrices raised to the -1/2 
    """
    if self_loops is True:
        degrees = torch.sum(adjacency_matrices+torch.eye(adjacency_matrices.shape[-1]),
                            len(adjacency_matrices.shape)-1)
    else:
        degrees = torch.sum(adjacency_matrices,len(adjacency_matrices.shape)-1)
    degrees = (1/torch.sqrt(degrees)).view(adjacency_matrices.shape[0], -1, 1)
    degrees = torch.mul(degrees, torch.eye(adjacency_matrices.shape[-1]))
    return degrees

def normalize(adjacency_matrices, self_loops=True):
    """
    Normalizes the adjacency matrices based on the formulas presented in 
    
    1)Semi-Supervised Classification with Graph Convolutional Networks, Kipf & Welling (arXiv:1609.02907)
    2)Simplifying Graph Convolutional Networks, F. Wu (arXiv:1902.07153)

    The adjacency matrix is normalized based on the verted degrees

      Ã = D^(-1/2).(A+I).D^(-1/2)
      Ã_ii = (A_ii.e_ii)/(d_i + 1)
      Ã_ij = (A_ij.e_ij)/(sqrt(d_i + 1).sqrt(d_j + 1))
      D_ii = sum_j Ã_ij

    Where A_ij is 1 when there exists an edge between vertex i and j, e_ij is the edge weight (1 if unweighted) and 
    d_i is the degree for vertex i.

    :param adjacency_matrix (torch.tensor): A tensor containing adjacency matrices (weighted or unweighted)
                                            that has the dimensions (B x N x N) where B is the batch size/number of graphs
                                            and N is the number of vertices/nodes in each graph
    :param (opt) residual (bool): Option to add self loops to the adjacency matrix resulting in the +1 term in Ã_ii and Ã_ij.

    :return adjacency_matrix (torch.tensor): A tensor containing the normalized adjacency matrices
    """
    
    degree_tensor = degree(adjacency_matrices, self_loops=self_loops)
    if self_loops is True:
        #Matrix multiplication D^(-1/2).(A+I).D^(-1/2)
        return torch.matmul(degree_tensor,
                            torch.matmul(adjacency_matrices+torch.eye(adjacency_matrices.shape[-1]), degree_tensor))
    else:
        #D^(-1/2).(A).D^(-1/2)
        return torch.matmul(degree_tensor,torch.matmul(adjacency_matrices, degree_tensor))
                            
