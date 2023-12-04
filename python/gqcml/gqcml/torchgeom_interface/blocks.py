import torch
import torch_geometric

class GCNConv_block(torch.nn.Module):
    """
    A network component that construct a sequence of GCNConv layers from torch_geometric
    These layers all have the same structure, with expection of the first layer.
    Attributes
        :inp_dim (int): The dimension of the node feature before application of the GCNConv layers
        :hidden_channels (int): The dimension to which the GCNConv layers map the node features
        :num_layers (int): The number of GCNConv layers
        :act_fn (torch.nn): The activation function used after each layer
        :add_self_loops (opt, bool): The add_self_loops option of the GCNConv layer, this value is set to False by default
        :normalize (opt, bool): The normalize option of the GCNConv layer, this value is set to False by default
        :bias (opt, bool): The option to include a bias term in the GCNConv layer, this value is set to True by default
        :residual (opt, bool): The option to add a residual connection after application of the activation function.
    """
    def __init__(self, inp_dim, hidden_channels, num_layers, act_fn,
                 add_self_loops=False, normalize=False, bias=True, residual=False):
        super(GCNConv_block,self).__init__()
        self.layers = torch.nn.ModuleList([torch_geometric.nn.conv.GCNConv(inp_dim, hidden_channels,
                                                                           add_self_loops=add_self_loops,
                                                                           normalize=normalize, bias=bias)]+
                                          [torch_geometric.nn.conv.GCNConv(hidden_channels, hidden_channels,
                                                                           add_self_loops=add_self_loops,
                                                                           normalize=normalize, bias=bias)
                                           for _ in range(num_layers-1)])
        self.inp_dim = inp_dim
        self.hidden_channels = hidden_channels
        self.num_layers = num_layers
        self.add_self_loops=add_self_loops
        self.normalize=normalize
        self.bias=bias
        self.act_fn = act_fn
        self.residual = residual
        
    def forward(self, x, edge_idx, edge_attr):
        node_feature = self.act_fn(self.layers[0](x, edge_idx, edge_weight=edge_attr))
        for layer in self.layers[1:]:
            if self.residual:
                node_feature = node_feature+self.act_fn(layer(node_feature, edge_idx, edge_weight=edge_attr))
            else:
                node_feature = self.act_fn(layer(node_feature, edge_idx, edge_weight=edge_attr))
        return node_feature

    def meta(self):
        meta_dict = {}
        meta_dict["Graph Conv type"]="GCNConv"
        meta_dict["input dimension"]=self.inp_dim
        meta_dict["Hidden channels"]=self.hidden_channels
        meta_dict["Number of layers"]=self.num_layers
        meta_dict["Self loops"]=self.add_self_loops
        meta_dict["Normalization"]=self.normalize
        meta_dict["Bias"]=self.bias
        meta_dict["Activation function"]=str(self.act_fn)
        meta_dict["Residual"]=self.residual
        return meta_dict
    
class GraphConv_block(torch.nn.Module):
    """
    A network component that construct a sequence of GCNConv layers from torch_geometric
    These layers all have the same structure, with expection of the first layer.
    Attributes
        :inp_dim (int): The dimension of the node feature before application of the GCNConv layers
        :hidden_channels (int): The dimension to which the GCNConv layers map the node features
        :num_layers (int): The number of GCNConv layers
        :act_fn (torch.nn): The activation function used after each layer
        :aggr (opt, str): String that determines how the message should be added, this value is by default add
        :bias (opt, bool): The option to include a bias term in the GCNConv layer, this value is set to True by default
        :residual (opt, bool): The option to add a residual connection after application of the activation function.
    """
    def __init__(self, inp_dim, hidden_channels, num_layers, act_fn,
                 aggr='add', bias=True, residual=False):
        super(GraphConv_block,self).__init__()
        self.layers = torch.nn.ModuleList([torch_geometric.nn.conv.GraphConv(inp_dim, hidden_channels,
                                                                             aggr=aggr, bias=bias)]+
                                          [torch_geometric.nn.conv.GraphConv(hidden_channels, hidden_channels,
                                                                             aggr=aggr, bias=bias)
                                           for _ in range(num_layers-1)])
        self.inp_dim = inp_dim
        self.hidden_channels = hidden_channels
        self.num_layers = num_layers
        self.bias=bias
        self.act_fn = act_fn
        self.aggr = aggr
        self.residual = residual
        
    def	forward(self, x, edge_idx, edge_attr):
        node_feature = self.act_fn(self.layers[0](x, edge_idx, edge_weight=edge_attr))
        for layer in self.layers[1:]:
            if self.residual:
                node_feature = node_feature+self.act_fn(layer(node_feature, edge_idx, edge_weight=edge_attr))
            else:
                node_feature = self.act_fn(layer(node_feature, edge_idx, edge_weight=edge_attr))
        return node_feature
    
    def	meta(self):
        meta_dict = {}
        meta_dict["Graph Convolution type"]="GraphConv"
        meta_dict["input dimension"]=self.inp_dim
        meta_dict["Hidden channels"]=self.hidden_channels
        meta_dict["Number of layers"]=self.num_layers
        meta_dict["Bias"]=self.bias
        meta_dict["Activation function"]=str(self.act_fn)
        meta_dict["Aggregation method"]=self.aggr
        meta_dict["Residual"]=self.residual
        return meta_dict

class GatedGraphConv_block(torch.nn.Module):
    """
    A network component that construct a sequence of GatedGraphConv layers from torch_geometric
    These layers all have the same structure, with expection of the first layer.
    Attributes
        :hidden_channels (int): The dimension to which the GatedGraphConv layers map the node features
        :num_layers (int): The number of GCNConv layers
        :aggr (opt, str): String that determines how the message should be added, this value is by default add
        :bias (opt, bool): The option to include a bias term in the GCNConv layer, this value is set to True by default
    """
    def __init__(self, hidden_channels, num_layers, bias=True, aggr="add"):
        super(GatedGraphConv_block, self).__init__()
        self.hidden_channels = hidden_channels
        self.num_layers = num_layers
        self.bias = bias
        self.aggr = aggr
        self.layers = torch.nn.ModuleList([torch_geometric.nn.GatedGraphConv(hidden_channels, 1, bias=bias, aggr=aggr)
                                           for _ in range(num_layers)])

    def	forward(self, x, edge_idx, edge_attr):
        node_feature = self.layers[0](x, edge_idx, edge_weight=edge_attr)
        for layer in self.layers[1:]:
            node_feature = layer(node_feature, edge_idx, edge_weight=edge_attr)
        return node_feature

    def meta(self):
        meta_dict = {}
        meta_dict["Graph Convolution type"]="GatedGraphConv"
        meta_dict["Hidden channels"]=self.hidden_channels
        meta_dict["Number of layers"]=self.num_layers
        meta_dict["Bias"]=self.bias
        meta_dict["Aggregation method"]=self.aggr
        return meta_dict
