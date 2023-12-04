import torch
import torch_geometric
import torch_scatter

class GCNConv(torch.nn.Module):
    """GCNConv model

    A standard graph convolutional network using the torch geomtric interface

    Arguments:

        num_sites: number of sites/atoms in the Hückel model

        node_embedding_nn (torch.nn.Module): A torch.nn.Module that processes the initial node features. This torch module
                                             takes a tensor with dimensions (B x N x f)  and should return a tensor with
                                             dimensions (B x N x F) where B is the batch size, N is the number of nodes in
                                             the graphs, f is the initial number of node features and F is the number of node features
                                             associated with each node in the graph. F should be equal to the node_input_dim
                                             parameter of the GraphConv layers.

        gcn_configs (list): A list containing the dimensions of the consecutive layers of the embedding section of the network
                            The first value of this list corresponds to the dimensions of the node feature vector and the last
                            value corresponds to the first node feature dimension of the graph convolutions section.

        activation_function (torch.nn): The activation function that will be used in after each layer in the embedding, graph convolution
                                        and property prediction phase of the network

        node_prop_nn (torch.nn.Module): A torch.nn.Module that processes the transformed node features after the application
                                        of the graph convolution operators. The network takes the node features with dimension
                                        (B x N x F) where B is the batch size, N is the number of nodes in the graph and F
                                        the number of features associated with each node in the graphs. The output of the network
                                        is a tensor that has the dimensions (B x N x 1) where the resulting features are
                                        mapped to a single node property.

        normalize (optional, boolean): Option to enable the use of the normalized form of the graph convolution

        bias (optional, boolean): Option to add a bias to the layers
    """

    def __init__(self, node_embedding_nn, gc_layers, activation_function, node_prop_nn,
                 normalize=False, bias=True, add_self_loops=False, residual=False):
        super(GCNConv, self).__init__()
        if node_embedding_nn:
            self.node_embedding=node_embedding_nn
        else:
            self.node_embedding=None
        self.GC_layers = gc_layers
        self.act_func = activation_function
        self.node_prop=node_prop_nn

    def forward(self, data):
        """Forward 

        The function to compute the model output.

        Parameters
        
            :param data (torch_geometric.data.Batch): A Batch object from torch geometric obtained from the loader
                                                      which contains x, edge_index, edge_attr and batch

            :return graph property (torch.tensor): A 2D tensor containing the output values associated with the input graphs
        """
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        # GCNConv cannot handle negative weights
        # https://github.com/rusty1s/pytorch_geometric/issues/795
        if self.emb:
            node_features = self.node_embedding(x)
        
        node_property = self.node_prop(node_features)
        node_property = torch_scatter.scatter_sum(node_property, batch, dim=0)
        return node_property.squeeze(1)

    def node_properties(self, data):
        """Node properties
        
        Returns the properties of the nodes, i.e. the output of the layer before summing to obtain the 
        graph property

        Parameters

            :param data (torch_geometric.data.Batch): A Batch object from torch geometric obtained from the loader
                                                      which contains x, edge_index, edge_attr and batch

            :return node properties (torch.tensor): A 2D tensor containing the output values associated with the
                                                    nodes of the input graphs
        """
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        # GCNConv cannot handle negative weights
        # https://github.com/rusty1s/pytorch_geometric/issues/795
        
        for layer in self.gcn_layers:
            x=self.act_func(layer(x, edge_index, edge_attr))
        for layer in self.site_prop_layers[:-1]:
            x=self.act_func(layer(x))
        x = self.site_prop_layers[-1](x)
        return x

    def meta(self):
        """Meta

        Returns a dictionary that contains all the network parameters sorted according 3
        blocks (embedding, gc and property).
        """
        GCNConv_model_dict={}
        GCNConv_model_dict["Embedding"]=self.node_embedding.meta()
        GCNConv_model_dict["Graph Convolution"]={"Graph Conv configuration":self.GCN_configs,
                                                 "Activation function":str(self.act_func),
                                                 "Normalize A":self.norm,
                                                 "Bias":self.bias}
        GCNConv_model_dict["Node properties"]=self.node_prop.meta()
        if self.bn_layers:
            GCNConv_model_dict["Batch Normalization"]=True
        if self.dropout_layers:
            GCNConv_model_dict["Dropout"]=True
        return GCNConv_model_dict

class GatedGraphConv(torch.nn.Module):
    """Gated Graph Conv model

    A standard graph convolutional network using the torch geomtric interface

    Arguments:

        num_sites: number of sites/atoms in the Hückel model

        node_embedding_nn (torch.nn.Module): A torch.nn.Module that processes the initial node features. This torch module
                                             takes a tensor with dimensions (B x N x f)  and should return a tensor with
                                             dimensions (B x N x F) where B is the batch size, N is the number of nodes in
                                             the graphs, f is the initial number of node features and F is the number of node features
                                             associated with each node in the graph. F should be equal to the node_input_dim
                                             parameter of the GraphConv layers.

        gcn_configs (list): A list containing the dimensions of the consecutive layers of the embedding section of the network
                            The first value of this list corresponds to the dimensions of the node feature vector and the last
                            value corresponds to the first node feature dimension of the graph convolutions section.

        activation_function (torch.nn): The activation function that will be used in after each layer in the embedding, graph convolution
                                        and property prediction phase of the network

        node_prop_nn (torch.nn.Module): A torch.nn.Module that processes the transformed node features after the application
                                        of the graph convolution operators. The network takes the node features with dimension
                                        (B x N x F) where B is the batch size, N is the number of nodes in the graph and F
                                        the number of features associated with each node in the graphs. The output of the network
                                        is a tensor that has the dimensions (B x N x 1) where the resulting features are
                                        mapped to a single node property.

        normalize (optional, boolean): Option to enable the use of the normalized form of the graph convolution

        bias (optional, boolean): Option to add a bias to the layers
    """

    def __init__(self, node_embedding_nn, output_channels,nmb_layers,
                 node_prop_nn,bias=True):
        super(GatedGraphConv, self).__init__()
        self.node_embedding=node_embedding_nn
        self.gatedgraph_layers = torch_geometric.nn.conv.GatedGraphConv(output_channels, nmb_layers,bias=bias)
        self.gatedgraph_config = (output_channels, nmb_layers)
        self.node_prop=node_prop_nn
        self.bias = bias
        
    def forward(self, data):
        """Forward

        The function to compute the model output.

        Parameters

            :param data (torch_geometric.data.Batch): A Batch object from torch geometric obtained from the loader
                                                      which contains x, edge_index, edge_attr and batch

            :return graph property (torch.tensor): A 2D tensor containing the output values associated with the input graphs
        """
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        # GCNConv cannot handle negative weights
        # https://github.com/rusty1s/pytorch_geometric/issues/795
        node_features = self.node_embedding(x)
        node_property = self.gatedgraph_layers(node_features, edge_index, edge_attr)
        node_property = self.node_prop(node_features)
        node_property = torch_scatter.scatter_sum(node_property, batch, dim=0)
        return node_property.squeeze(1)

    def node_properties(self, data):
        """Node properties

        Returns the properties of the nodes, i.e. the output of the layer before summing to obtain the
        graph property

        Parameters

            :param data (torch_geometric.data.Batch): A Batch object from torch geometric obtained from the loader
                                                      which contains x, edge_index, edge_attr and batch

            :return node properties (torch.tensor): A 2D tensor containing the output values associated with the
                                                    nodes of the input graphs
        """
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        # GCNConv cannot handle negative weights
        # https://github.com/rusty1s/pytorch_geometric/issues/795

        for layer in self.gcn_layers:
            x=self.act_func(layer(x, edge_index, edge_attr))
        for layer in self.site_prop_layers[:-1]:
            x=self.act_func(layer(x))
        x = self.site_prop_layers[-1](x)
        return x

    def meta(self):
        """Meta

        Returns a dictionary that contains all the network parameters sorted according 3
        blocks (embedding, gc and property).
        """
        GatedGraphConv_model_dict={}
        GatedGraphConv_model_dict["Embedding"]=self.node_embedding.meta()
        GatedGraphConv_model_dict["Graph Convolution"]={"Gated Graph Conv configuration":self.gatedgraph_config,
                                                        "Bias":self.bias}
        GatedGraphConv_model_dict["Node properties"]=self.node_prop.meta()
        return GCNConv_model_dict
