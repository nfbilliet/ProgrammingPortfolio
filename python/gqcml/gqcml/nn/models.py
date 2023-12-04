from gqcml.nn import layers
import torch

__all__ = ["DNN", "GraphConv_model"]

class DNN(torch.nn.Module):
    """
    A standard dense network consisting of multiple hidden layers

    Attributes 
        :layer_dims (list): A list containing the number of nodes in each layer for the network.
                            The first entry in the list corresponds to the number of features in the input tensor
                            and the last entry in the list corresponds to the number of features in the output tensor
        :activation_function (torch.nn): The activation used in the network after each hidden layer
        :bias (opt, bool): A boolean indication the option to include a bias term in the dense layers
    """
    def __init__(self,
                 layer_configs,
                 activation_function,
                 bias=True,
                 residual=False):
        super(DNN, self).__init__()
        self.bias=bias
        self.layer_configs = [(layer_configs[idx], layer_configs[idx+1]) for idx in range(len(layer_configs)-1)]
        self.layers = torch.nn.ModuleList([torch.nn.Linear(layer_config[0], layer_config[1], bias=bias)
                                           for layer_config in self.layer_configs])
        self.activation_function = activation_function
        self.residual = residual
        
    def forward(self, input_tensor):
        output_tensor = input_tensor.clone()
        for layer in self.layers[:-1]:
            if self.residual:
                output_tensor+=self.activation_function(layer(output_tensor))
            else:
                output_tensor=self.activation_function(layer(output_tensor))
        return self.layers[-1](output_tensor)

    def meta(self):
        """
        Takes the input arguments of the class and formats them in a dictionary format which can be used in
        creating an overarching meta file
        """
        DNN_dict = {}
        DNN_dict["Model type"]="Dense"
        DNN_dict["Layer configuration"]=self.layer_configs
        DNN_dict["Bias"]=self.bias
        DNN_dict["Activation function"]=str(self.activation_function)
        return DNN_dict
    
class Emb(torch.nn.Module):
    """
    A module that performs the linear mapping of an initial feature vector to an embedded feature vector according
    to the formula

    .. math::
       EMB(v_i)=v_iZ

    Where Z is a learnable set of weights with dimensions (M x N) where M is the number of input features and N 
    is the number of output features in the embedded space

    Attributes
        :input_dim (int): An integer describing the initial dimension of the node features 
        :output_dim (int): An integer describing the desired output dimension of the node features
        :bias (opt, bool): A boolean (standard False) that enables or disables the inclusion of a bias term in the construction
                          of the embedding vector
    """
    def __init__(self,
                 input_dim,
                 output_dim,
                 bias=False):
        super(Emb, self).__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.bias=bias
        self.embedding = torch.nn.Linear(input_dim, output_dim, bias=bias)
                
    def forward(self, input_tensor):
        return self.embedding(input_tensor)
    
    def meta(self):
        """
        Takes the input arguments of the class and formats them in a dictionary format which can be used in
        creating an overarching meta file
        """
        Emb_dict = {}
        Emb_dict["Model type"]="Embedding"
        Emb_dict["Layer configuration"]=[self.input_dim, self.output_dim]
        Emb_dict["Bias"]=self.bias
        return Emb_dict


class Gauss_Emb(torch.nn.Module):
    """
    A module that performs the Gaussian embedding procedure for a single continuous node feature.
    The layer consists of 2 specific components
       1) Gaussian expansion layer
       2) Embedding layer
    The Gaussian expansion layer consist of a set of Gaussians where neighbouring Gaussians are equidistant 
    and each gaussian has the same width. Let F be the function that performs the Gaussian expansion then
    F consists of K elements 

    .. math::
        F(x) = [f_1(x), f_2(x), ..., f_K(x)]

    where f_i(x) is defined as 

    .. math::
        f_i(x) = exp^{\\frac{-(x-m_i)^2}{2s^2}}

    where m_i is the mean/center of the Gaussian and s is the variance of the Gaussian. Subsequently this
    expanded vector is fed to an embedding layer that subsequently transforms it through a linear combination

       G_EMB(v_i)=F(v_i)Z

    Where Z is a learnable matrix of dimension (K x N) with K the number of Gaussians in the expansion layer
    and N the embedding dimension

    Attributes
       :lower (float): The lower limit of the interval from which the means of the Gaussians are generated
       :upper (float): The upper limit of the interval from which the means of the Gaussians are generated
       :num_gaussians (int): The number of equidistant Gaussians that are generated in the interval specified
                            by the lower and upper argument
       :output_dim (int): The output dimension of the embedded feature vector
       :variance (opt) (float/None): Controls the width of the Gaussians and is standarly computed so that
                                    neighbouring Gaussians intersect at 0.5 (FWHM) as to maintain resolution.
                                    If the standard None value is changed to a float this float will be utilized instead.
       :bias (opt, bool): A boolean that controls whether to include a bias term in the generation of the embedding.
                          This value is standardly set to False and will not include a bias.
    """

    def __init__(self,
                 lower,
                 upper,
                 num_gaussians,
                 output_dim,
                 variance=None,
                 bias=False):
        super(Gauss_Emb, self).__init__()
        self.lower = lower
        self.upper = upper
        self.num_gaussians = num_gaussians
        self.output_dim = output_dim
        self.variance = variance
        self.bias = bias
        self.gauss = layers.GaussianEmbedding(lower, upper, num_gaussians, output_dim,
                                              variance=variance, emb_bias=bias)

    def forward(self, input_tensor):
        return self.gauss(input_tensor)

    def meta(self):
        Emb_dict={}
        Emb_dict["Model type"]="Gaussian Embedding"
        Emb_dict["Continuous interval"]=[self.lower, self.upper]
        Emb_dict["Number of Gaussians"]=self.num_gaussians
        Emb_dict["Embedding dimension"]=self.output_dim
        if self.variance is None:
            Emb_dict["Variance"]="FWHM"
        else:
            Emb_dict["Variance"]=self.variance
        Emb_dict["Bias"]=self.bias
        return Emb_dict
    
class GraphConv_model(torch.nn.Module):
    """
    A standard graph convolution model constructor

    Attributes
        :node_embedding_nn (torch.nn.Module): A torch.nn.Module that processes the initial node features. This torch module
                                             takes a tensor with dimensions (B x N x f)  and should return a tensor with
                                             dimensions (B x N x F) where B is the batch size, N is the number of nodes in
                                             the graphs, f is the initial number of node features and F is the number of node features
                                             associated with each node in the graph. F should be equal to the node_input_dim
                                             parameter of the GraphConv layers.
        :GC_dimensions (list): A list of integers describing the consecutive node embedding dimensions that go into the graph
                              convolution layers and are subsequently returned. 
        :activation_function (torch.nn): The activation function used non-linear transformation of the aggregated neighbourhood
                                        information.
        :node_prop_nn (torch.nn.Module): A torch.nn.Module that processes the transformed node features after the application
                                        of the graph convolution operators. The network takes the node features with dimension
                                        (B x N x F) where B is the batch size, N is the number of nodes in the graph and F
                                        the number of features associated with each node in the graphs. The output of the network
                                        is a tensor that has the dimensions (B x N x 1) where the resulting features are
                                        mapped to a single node property.
    """

    def __init__(self,
                 node_embedding_nn,
                 GC_dimensions,
                 activation_function,
                 node_prop_nn,
                 bias=True):
        super(GraphConv_model, self).__init__()
        self.node_embedding = node_embedding_nn
        self.activation_function = activation_function
        #Construct a list of tuples that determine the number of input features for each node and the
        #number of output features from the graph convolution layer
        self.layer_configs = [(GC_dimensions[idx], GC_dimensions[idx+1])
                              for idx in range(len(GC_dimensions)-1)]
        self.GC_layers = torch.nn.ModuleList([layers.GraphConv(layer_config[0],
                                                               layer_config[1],
                                                               self.activation_function,
                                                               bias=bias)
                                              for layer_config in self.layer_configs])

    def forward(self, node_feat, adj_matrix):
        """
        Forward propagation phase of the graph conv model

        Arguments
            :node_feat (torch.Tensor): The initial node feature tensor with the dimensions (B x N x f) where B is the batch
                                        size, N is the number of nodes in each graph and f is the number of node features
                                        associated with each node in the graphs.
            :adj_matrix (torch.Tensor): The weighted adjacency tensor with the dimensions (B x N x N) where B is the batch
                                        size and N is the number of nodes in each graph.
        Returns
        :output (torch.Tensor): The graph property tensor with dimensions (B x 1) where B is the batch
                                size. The graph property is computed as the sum of the node properties obtained through the
                                site_prop_nn
        """
        # Transform the initial node features
        node_emb = self.node_embedding(node_feat)
        # Aggregate neighbourhood information of each node
        for GC_layer in self.GC_layers:
            node_emb = GC_layer(node_emb, adj_matrix)
        # Transform the aggregated features into site properties
        node_prop = self.node_properties(node_emb)
        # Sum all the node properties in each graph
        return torch.sum(node_prop, 1)

    def site_properties(self, node_feat, adj_matrix):
        """
        Site property function utilized to return the site properties, i.e. the output of the layer before the final pooling step

        Arguments
            :node_feat (torch.Tensor): The initial node feature tensor with the dimensions (B x N x f) where B is the batch
                                        size, N is the number of nodes in each graph and f is the number of node features
                                        associated with each node in the graphs.
            :adj_matrix (torch.Tensor): The weighted adjacency tensor with the dimensions (B x N x N) where B is the batch
                                        size and N is the number of nodes in each graph.
        Returns
        :node properties(torch.Tensor): The site properties tensor with dimensions (B x N x1) where B is the batch
                                        size and N is the number of nodes in each graph.
        """
        # Transform the initial node features
        node_emb = self.activation_function(self.node_embedding(node_feat))
        # Aggregate neighbourhood information of each node
        for GC_layer in self.GC_layers:
            node_emb = GC_layer(node_emb, adj_matrix)
        # Transform the aggregated features into site properties
        node_prop = self.node_properties(node_emb)
        return site_prop

    def meta(self):
        GraphConv_dict={}
        GraphConv_dict["Embedding"]=self.node_embedding.meta()
        GraphConv_dict["Graph Convolution"]={"Graph Conv configuration":self.layer_configs,
                                             "Number of filter layers per GC layer":self.nmb_filter_dlayers,
                                             "Activation function":str(self.activation_function)}
        GraphConv_dict["Node property"]=self.node_properties.meta()
        return GraphConv_dict
