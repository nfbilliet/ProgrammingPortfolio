import torch
import torch_geometric
import gqcml
import torch_scatter

class ContConv(torch.nn.Module):
    """
    The Continuous convolution operator which will generate edge dependant feature weights

    Attributes
        :GaussianExpansion (gqcml.nn.layers): A Gaussian expansion module that maps a single edge feature 
                                              to a tensor of the same dimension as the node features
        :weight_mapping (gqcml.nn.models/torch.nn): A dense module that maps the Gaussian expansion of the edge features
                                                    to a tensor of the same dimension as the node features  
    Returns 
        :weight_tensor (torch.Tensor): A tensor containing the weights for each node feature
    """

    def __init__(self, GaussianExpansion, weight_mapping):
        super(ContConv, self).__init__()
        self.GaussianExpansion = GaussianExpansion
        self.weight_mapping = weight_mapping

    def forward(self, edge_weight):
        gaussian_expanded = self.GaussianExpansion(edge_weight)
        return self.weight_mapping(gaussian_expanded)

class InteractionBlock(torch_geometric.nn.MessagePassing):
    """
    An interaction module that weights the atoms with its neighbours
        1) Dense module that map the node features to the representation that will be weighted by the 
             continuous convolution weights
        2) Continuous convolution operation
            2.1) Gaussian expansion that converts the interatomic distance in a gaussian basis
            2.2) A Dense module that maps the Gaussian expansion to a set of weights which will 
                   be used to weight the neighbours features. The output of (2.1) is weighted element-wise
                   by the output of this section
        3) Dense module that maps the newly weighted features to the interaction terms which will be added
             to the atom state

    Arguments
        :pre_weighting (gqcml.nn.models/torch.nn.Module): A module that reweights the node features and returns them 
                                                          to be weighted by the continuous convolution weights
        :cont_conv (ContConv): See ContConv class
        :post_weighting (gqcml.nn.models/torch.nn.Module): A module that performs a non-linear mapping of the continuous 
                                                           convolution output
    Returns
        :updated_nf (torch.Tensor): T
    """
    def __init__(self, pre_weighting, cont_conv, post_weighting):
        super(InteractionBlock, self).__init__(aggr="add")
        self.pre_weighting = pre_weighting
        self.cont_conv = cont_conv
        self.post_weighting = post_weighting

    def forward(self, node_feat, edge_idx, edge_weight):
        pre_weighted_nf = self.pre_weighting(node_feat)
        weights_cc = self.cont_conv(edge_weight)
        out = self.propagate(edge_idx, nf=pre_weighted_nf, weights_cc=weights_cc)
        out = self.post_weighting(out)
        return node_feat+out

    def message(self, nf_j, weights_cc):
        return nf_j * weights_cc

class ShiftedSoftplus(torch.nn.Module):
    def __init__(self):
        super(ShiftedSoftplus, self).__init__()
        self.shift = torch.log(torch.tensor(2.0)).item()

    def forward(self, x):
        return torch.nn.functional.softplus(x) - self.shift

class SchNet(torch.nn.Module):
    def __init__(self, hidden_channels, int_blocks, nmb_gaussians, 
                 edge_lower=0, edge_upper=30):
        super(SchNet, self).__init__()
        self.embedding = torch.nn.Embedding(10, hidden_channels)
        self.edge_expansion = gqcml.nn.layers.GaussianExpansion(edge_lower, 
                                                                edge_upper,
                                                                nmb_gaussians)
        self.cont_convs = [gqcml.torchgeom_interface.schnet.ContConv(self.edge_expansion,
                                                                     gqcml.nn.models.DNN([nmb_gaussians,hidden_channels,hidden_channels],
                                                                                         ShiftedSoftplus())) for _ in range(int_blocks)]
        self.int_blocks = [gqcml.torchgeom_interface.schnet.InteractionBlock(torch.nn.Linear(hidden_channels,hidden_channels),
                                                                             cont_conv,
                                                                             gqcml.nn.models.DNN([hidden_channels]*3,
                                                                                                  ShiftedSoftplus()))
                           for cont_conv in self.cont_convs]
        self.int_blocks = torch.nn.ModuleList(self.int_blocks)
        self.prop = gqcml.nn.models.DNN([hidden_channels, hidden_channels//2, 1], ShiftedSoftplus())
    
    def forward(self, data):
        x, edge_idx, edge_attr, batch = data.x.long(), data.edge_index, data.edge_attr.double(), data.batch
        edge_attr=edge_attr.view(-1,1)
        nf = self.embedding(x)
        for int in self.int_blocks:
            nf = int(nf, edge_idx, edge_attr)
        site_prop = self.prop(nf)
        return torch_scatter.scatter_sum(site_prop, batch, dim=0).squeeze(1)
