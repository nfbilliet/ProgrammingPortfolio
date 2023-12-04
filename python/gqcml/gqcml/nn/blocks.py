import torch
from gqcml.nn.layers import GraphConv

class GraphConv_Block(torch.nn.Module):
    """
    A sequential block of GraphConv operators that can be used a building module of a graph convolutional model.

    Attributes
        :node_input_dim (int): The number of features that are associated with each node in the graph G
        :nmb_GraphConv_layers (int): The number of GraphConv layers that need to be present in the block
        :nmb_filter_dlayers (int): The number of non-linear transformations that are performed in each graph convolution
                                   after aggregation of the neighbourhood features. The dense layers standardly are constructed
                                   to output as many amount of features that go into them
    """
    def __init__(self,
                 node_input_dim,
                 nmb_GC_layers,
                 nmb_filter_dlayers,
                 activation_function):
        super(GraphConv_Block, self).__init__()
        self.GC_layers = torch.nn.ModuleList([GraphConv(node_input_dim, nmb_filter_dlayers, activation_function)]*nmb_GC_layers)

    def forward(self, node_feat, adj_matrix):
        """forward
        Forward propagation function that produces an output

        Arguments
            :node_feat (torch.Tensor): The initial node feature tensors that are associated with a batch of graphs. This
                                         tensor should have the dimensions (B x N x F) where B is the batch size, N the
                                         number of nodes present in the graphs and F the number of features associated
                                         with each node present in the graph
            :adj_matrix (torch.Tensor): The weighted adjacency tensors that are associated with a batch of graphs. This
                                          tensor should have the dimensions (B x N x N) where B is the batch size and N
                                          the number of nodes present in the graph
        Returns
            :transf_node_feat (torch.Tensor): The transformed node features that are obtained by consecutively performing
                                              the graph convolutional operator. This tensor has the dimensions (B x N x F)
                                              where B is the batch size, N the number of nodes present in the graph and
                                              F is the number of features associated with each node
        """
        transf_node_feat = node_feat.clone()
        for GC_layer in self.GC_layers:
            transf_node_feat = GC_layer(transf_node_feat, adj_matrix)
        return transf_node_feat

