import torch
import numpy as np

class GraphConv(torch.nn.Module):
    """GraphConv

    The standard graph convolution operator defined in the paper [Semi-Supervised Classification with Graph Convolutional
    Networks](https://arxiv.org/abs/1609.02907).
    
    .. math::
        n_{i+1} = h\\left(An_{i}.W_{i+1}\\right)

    Where the current node features are aggregated according to the adjacency matrix A and subsequently weighted by a (set of)
    weight matrix/matrices. We include the option for a  residual connection by adding the transformed node features to the current
    state

    Attributes
        :node_input_dim (int): The number of features present on the nodes of the graph G when entering the layer 
        :node_output_dim (int): The number of features present in the layer output
        :activation_function (torch.nn): The activation function to be used for the filter layer(s) after message construction
        :bias (opt, bool): A boolean that enables or disables the bias term in the filter application. In the standard settings
                           this value is True
    """
    
    def __init__(self,
                 node_input_dim,
                 node_output_dim,
                 activation_function,
                 bias=True):
        super(GraphConv, self).__init__()
        self.activation_function = activation_function
        self.weights = torch.nn.Parameter(torch.Tensor(node_input_dim,
                                                       node_output_dim))
        if bias:
            self.bias = torch.nn.Parameter(torch.Tensor(node_output_dim))
        else:
            self.register_parameter('bias', None)
            self.bias=None
        self.reset_parameters()

    def reset_parameters(self):
        """
        A function that initializes the weights and biases of the learnable layer
        """
        torch.nn.init.xavier_uniform_(self.weights)
        if self.bias is not None:
            torch.nn.init.zeros_(self.bias)
        
    def forward(self, node_feat, adj_matrix):
        """
        Function that calls the forward pass of the layer
        
        Arguments
            :node_feat (torch.Tensor): The current node features, this tensor should have the dimensions (B x N x F) where
                                          B is the batch size, N is the number of nodes and F is the number of features
            :adj_matrix (torch.Tensor): The adjacency matrices by which the node features need to be aggregated, this tensor
                                           should have the dimensions (B x N x N) where B is the batch size and N the number of nodes
        Returns
            :transf_node_emb (torch.Tensor): The updated node features with the aggregated features according to the adjacency
                                                 matrix. This tensor has the same dimensions as
        """
        node_message = torch.matmul(node_feat, self.weights)
        output = torch.matmul(adj_matrix, node_message)
        if self.bias is not None:
            output += self.bias
        return self.activation_function(output)
    
class GaussianExpansion(torch.nn.Module):
    """
    A layer that takes an input tensor and expands it into a gaussian basis.
    The layer takes a tensor consisting of single descriptors and bins this descriptor.
    The descriptor is fed to a function that computes the output value of a series of gaussians
    that are equidistantly spaced using a linear space of means and a single variance parameter.
    The output of this function thus maps a scalar value to a vector with the dimension equal to the
    number of gaussians that we have chosen to span the linear space of means.

    .. math::
        \\phi(\\nu_i)=\\nu_i \\rightarrow \\vec{\\nu_i}: \\mathbb{R} \\mapsto \\mathbb{R}^N
        
    .. math::
        \\phi(\\nu_i)=\\begin{bmatrix} e^{\\frac{\\nu_i-\\mu_1}{2\\sigma^2}} & e^{\\frac{\\nu_i-\\mu_2}{2\\sigma^2}} & \dots & e^{\\frac{\\nu_i-\\mu_N}{2\\sigma^2}} \\end{bmatrix}

    Attributes
        :lower (float): A float that bounds the linear space from which the means are generated.
                             The space spans the interval [lower, upper]
        :upper (float): A float that bounds the linear space from which the means are generated.
                             The space spans the interval [lower, upper]
        :num_gaussians (int): The number of gaussian functions that we place within the linear space.
        :variance (opt, float): Standardly this is not defined. When this optional parameter is not
                                      defined we compute the variance so that the FWHM of neighbouring
                                      overlaps. If a float is given the variance as defined will be used.
    """
    def __init__(self, lower, upper, num_gaussians, variance=None):
        super(GaussianExpansion, self).__init__()
        self.means = torch.nn.parameter.Parameter(torch.from_numpy(np.linspace(lower, upper, num_gaussians)),
                                                  requires_grad=False)
        if variance:
            self.precision = torch.nn.parameter.Parameter(torch.tensor(1/(2*variance)), requires_grad=False)
        else:
            diff = np.linspace(lower, upper, num_gaussians)[1]-np.linspace(lower, upper, num_gaussians)[0]
            variance = -(diff)**2/(2*np.log(0.5))
            self.precision = torch.nn.parameter.Parameter(torch.tensor(1/(2*variance)), requires_grad=False)
        self.num_gaussians = num_gaussians
        self.lower = lower
        self.upper = upper
        
    def forward(self, inp):
        """
        Forward phase of the layer

        Arguments
            :inp (torch.Tensor: A (B x N x 1) tensor, where B is the batch size and N is the number of nodes,
                                  that should be expaned in a Gaussian basis 
        Returns
            :expanded tensor (torch.Tensor): A (B x N x M) tensor where M is the number of Gaussians
        """
        return torch.exp(-1*self.precision*torch.pow(inp-self.means,2)).double()

    def meta(self):
        """
        A function that extracts the meta data from the layer
        """
        meta_dict={}
        meta_dict["Layer"]="Gaussian Expansion"
        meta_dict["Number of Gaussians"]=self.num_gaussians
        meta_dict["Lower bound"]=self.lower
        meta_dict["Upper bound"]=self.upper
        meta_dict["Precision"]=self.precision.data.item()
        return meta_dict
    
class GaussianEmbedding(torch.nn.Module):
    """
    A function that combines the GaussianExpansion layer with the concept of embedding.
    Should the initial features be described by a single continuous variable the problem
    becomes that learning an embedding for this becomes difficult due to the mathematical 
    construct of embedding where

    .. math::
        E(\\nu_i) = Z\\phi(\\nu_i)

    Where Z is a learnable set of weights. In the case of a single node feature v_i
    the dimension of this Z becomes a vector and thus does not contain many learnable parameters.
    When we use the Gaussian expansion layer we convert this continuous variable to "quasi" binned variable
    where our bins consist of the different gaussians within the layer and the layer measures "overlap" with the gaussians.
    Using this expanded representation we provide more freedom to the Z matrix in our embedding due to the increased dimensionality.

    Attributes
        :lower (float): A float that bounds the linear space from which the means are generated.
                             The space spans the interval [lower, upper]
        :upper (float): A float that bounds the linear space from which the means are generated.
                             The space spans the interval [lower, upper]
        :variance (float): A float that controls the width of gaussians that we construct.
        :num_gaussians (int): The number of gaussian functions that we place within the linear space.
        :emb_dim (int): The dimension of the embedded node feature. 
        :emb_bias (opt,bool): A boolean that controls the addition of a learnable bias for the embedding
    """
    def __init__(self, lower, upper, num_gaussians, emb_dim, variance=None, emb_bias=False):
        super(GaussianEmbedding, self).__init__()
        self.GaussExp = GaussianExpansion(lower, upper, num_gaussians, variance=variance)
        self.embedding = torch.nn.Linear(num_gaussians, emb_dim, bias=emb_bias).double()

    def forward(self, inp):
        """
        A function that calls the forward propagation
        
        Arguments
            :inp (torch.Tensor: A (B x N x 1) tensor, where B is the batch size and N is the number of nodes,
                                  that should be expaned in a Gaussian basis
        Returns
            :embedded tensor (torch.Tensor): A (B x N x E) tensor where E is the embedding dimension
        """
        expanded_inp = self.GaussExp(inp)
        return self.embedding(expanded_inp)
    

class ShiftedSoftplus(torch.nn.Module):
    """
    The shifted softplus activation function
    
    .. math::
        ln\\left(\\beta+\\beta e^{x}\\right)

    Attributes
        :beta (opt,float): A shifting factor with standard setting 2
    """
    def __init__(self, beta=2):
        super(ShiftedSoftplus, self).__init__()
        self.shift = torch.log(torch.tensor(beta)).item()

    def forward(self, inp):
        return torch.nn.Softplus(inp) - self.shift
