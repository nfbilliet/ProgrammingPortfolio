from gqcml.nn.layers import GraphConv
import torch
#import torch_scatter
#import torch_geometric

class GCNConv_tg(torch.nn.Module):
    def __init__(self):
        super(GCNConv_tg, self).__init__()
        #1 input feature, 4 output features
        self.graph_conv = torch_geometric.nn.GCNConv(2, 4, normalize=True, bias=True)
        self.dense_layer = torch.nn.Linear(4, 1)

    def forward(self, data):
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        x = torch.nn.ReLU()(self.graph_conv(x, edge_index, edge_attr))
        x = self.dense_layer(x)
        return torch_scatter.scatter_sum(x, batch, dim=0)


class GCNConv_gqcml(torch.nn.Module):
    def __init__(self):
        super(GCNConv_gqcml, self).__init__()
        #1 input feature, 4 output features, 1 filter layer
        self.graph_conv = GraphConv(2, 4, 1, torch.nn.ReLU(), bias=True)
        self.dense_layer = torch.nn.Linear(4, 1)

    def forward(self, node_features, adj_matrices):
        node_features = self.graph_conv(node_features, adj_matrices)
        node_property = self.dense_layer(node_features)
        return torch.sum(node_property, 1)
