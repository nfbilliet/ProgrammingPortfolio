import torch
import torch_geometric
import torch_scatter

class Graph_Convolution_model(torch.nn.Module):
    """
    A general graph convolution model constructor.

    Attributes
        :emb (torch.nn.Module): A sequential object that maps the initial node features to the starting embedded node features.
        :conv (torch.nn.Module): A sequential object that contains the graph convolutions 
        :prop_ddn (torch.nn.Module): A sequential object that maps the aggregated node features obtained from the conv block to the graph property
    """
    def __init__(self, emb, conv_block, prop_dnn):
        super(Graph_Convolution_model, self).__init__()
        self.emb = emb
        self.conv_block=conv_block
        self.prop_dnn=prop_dnn
        
    def forward(self, data):
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        if self.emb:
            node_feature = self.emb(x)
            node_feature = self.conv_block(node_feature, edge_index, edge_attr)
            node_feature = self.prop_dnn(node_feature)
            return torch_scatter.scatter_sum(node_feature, batch, dim=0).squeeze(1)
        else:
            node_feature = self.conv_block(x, edge_index, edge_attr)
            node_feature = self.prop_dnn(node_feature)
            return torch_scatter.scatter_sum(node_feature, batch, dim=0).squeeze(1)
        
    def meta(self):
        model_dict = {}
        model_dict["Model type"]="Standard" 
        if self.emb:
            model_dict["Embedding"] = self.emb.meta()
        else:
            model_dict["Embedding"] = None
        model_dict["Graph Convolution"]=self.conv_block.meta()
        model_dict["Property prediction"]=self.prop_dnn.meta()
        return model_dict

class Graph_Convolution_avgpool_model(torch.nn.Module):
    """
    A general graph convolution model constructor that utilizes pooling of the node features to generate a general graph feature that is 
    used to map to a graph property.

    Attributes
        :emb (torch.nn.Module): A sequential object that maps the initial node features to the starting embedded node features.
        :conv (torch.nn.Module): A sequential object that contains the graph convolutions 
        :prop_ddn (torch.nn.Module): A sequential object that maps the aggregated node features obtained from the conv block to the graph property
        :max_feature (opt, bool): A boolean that controls whether to extend the average pooled features with a max pooled set of features.
                                  This additional graph pooled features will then be concatenated to the average pooled feature
    """
    def	__init__(self, emb, conv_block, prop_dnn, max_feature=False):
        super(Graph_Convolution_avgpool_model, self).__init__()
        self.emb = emb
        self.conv_block=conv_block
        self.prop_dnn=prop_dnn
        self.max_pool=max_feature
        
    def	forward(self, data):
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        if self.emb:
            node_feature = self.emb(x)
            node_feature = self.conv_block(node_feature, edge_index, edge_attr)
            if self.max_pool:
                graph_features = torch.cat((torch_geometric.nn.global_mean_pool(node_feature, batch),
                                            torch_geometric.nn.global_max_pool(node_feature, batch)),1)
            else:
                graph_features = torch_geometric.nn.global_mean_pool(node_feature, batch)
            graph_features = self.prop_dnn(graph_features)
            return graph_features.squeeze(1)
        else:
            node_feature = self.conv_block(x, edge_index, edge_attr)
            if self.max_pool:
                graph_features = torch.cat((torch_geometric.nn.global_mean_pool(node_feature, batch),
                                            torch_geometric.nn.global_max_pool(node_feature, batch)),1)
            else:
                graph_features = torch_geometric.nn.global_mean_pool(node_feature, batch)
            graph_features = self.prop_dnn(graph_features)
            return graph_features.squeeze(1)

    def	meta(self):
        model_dict = {}
        if self.max_pool:
            model_dict["Model type"]="Graph feature average+max pooling"
        else:
            model_dict["Model type"]="Graph feature average pooling"
        if self.emb:
            model_dict["Embedding"] = self.emb.meta()
        else:
            model_dict["Embedding"] = None
        model_dict["Graph Convolution"]=self.conv_block.meta()
        model_dict["Property prediction"]=self.prop_dnn.meta()
        return model_dict

class Graph_Convolution_attentionpool_model(torch.nn.Module):
    """
    A general graph convolution model constructor that utilizes pooling of the node features to generate a general graph feature that is 
    used to map to a graph property. This pooling mechanism utilizes the attention mechanism that learns to predict node importance to the graph feature of interest.

    Attributes
        :emb (torch.nn.Module): A sequential object that maps the initial node features to the starting embedded node features.
        :conv (torch.nn.Module): A sequential object that contains the graph convolutions 
        :prop_ddn (torch.nn.Module): A sequential object that maps the aggregated node features obtained from the conv block to the graph property
        :gate_nn (torch.nn.Module): https://pytorch-geometric.readthedocs.io/en/latest/modules/nn.html#torch_geometric.nn.glob.GlobalAttention
        :nn (torch.nn.Module): https://pytorch-geometric.readthedocs.io/en/latest/modules/nn.html#torch_geometric.nn.glob.GlobalAttention
        :max_feature (opt, bool): A boolean that controls whether to extend the average pooled features with a max pooled set of features.
                                  This additional graph pooled features will then be concatenated to the average pooled feature
    """
    def __init__(self, emb, conv_block, prop_dnn, gate_nn, nn=None,max_feature=False):
        super(Graph_Convolution_attentionpool_model, self).__init__()
        self.emb = emb
        self.conv_block= conv_block
        self.prop_dnn = prop_dnn
        self.attention_pool = torch_geometric.nn.GlobalAttention(gate_nn, nn=nn)
        self.gate_nn = gate_nn
        self.nn = nn
        self.max_pool=max_feature

    def forward(self, data):
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        if self.emb:
            node_feature = self.emb(x)
            node_feature = self.conv_block(node_feature, edge_index, edge_attr)
            if self.max_pool:
                graph_features = torch.cat((self.attention_pool(node_feature, batch),
                                            torch_geometric.nn.global_max_pool(node_feature, batch)),1)
            else:
                graph_features = self.attention_pool(node_feature, batch)
            graph_features = self.prop_dnn(graph_features)
            return graph_features.squeeze(1)
        else:
            node_feature = self.conv_block(x, edge_index, edge_attr)
            if self.max_pool:
                graph_features = torch.cat((self.attention_pool(node_feature, batch),
                                            torch_geometric.nn.global_max_pool(node_feature, batch)),1)
            else:
                graph_features = self.attention_pool(node_feature, batch)
            graph_features = self.prop_dnn(graph_features)
            return graph_features.squeeze(1)

    def meta(self):
        model_dict = {}
        if self.max_pool:
            model_dict["Model type"]="Graph feature attention+max pooling"
        else:
            model_dict["Model type"]="Graph feature attention pooling"
        if self.emb:
            model_dict["Embedding"] = self.emb.meta()
        else:
            model_dict["Embedding"] = None
        model_dict["Graph Convolution"]=self.conv_block.meta()
        if self.nn:
            model_dict["Attention Pooling"]={"Gate NN": self.gate_nn.meta(),
                                             "NN":self.nn.meta()}
        else:
            model_dict["Attention Pooling"]={"Gate NN": self.gate_nn.meta(),
                                             "NN":None}
        model_dict["Property prediction"]=self.prop_dnn.meta()
        return model_dict
