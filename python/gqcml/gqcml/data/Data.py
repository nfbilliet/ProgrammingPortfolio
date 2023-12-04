import numpy as np

class Preprocessor():
    """
    An objec that contains all the functionalities required in the handling of graph based data.

    Attributes
        :graph_dim (int): An attribute that describes the graph dimension of the set of graphs that will be processed
    """
    def __init__(self, graph_dim):
        self.graph_dim = graph_dim

    def __off_diagonal_format(self, matrix):
        """        
        A function that copies the given matrix and returns a copy of the matrix with
        the diagonal of the initial matrix removed

        this function is a utility function
        """
        off_diagonal_matrix = np.copy(matrix)
        off_diagonal_matrix[np.diag_indices(self.graph_dim)]=0
        return off_diagonal_matrix.reshape(self.graph_dim, self.graph_dim, 1, 1)

    def __diagonal_to_matrix(self, matrix, binary_matrix, repeat_along):
        """
        A function that extracts the diagonal of the matrix and generates a matrix
        where the diagonal is repeated as a row of the matrix. In addition to this
        we multiply this matrix with the binary form to obtain adjacency matrix
        that describes the graph in terms of the vertex self loops

        This function is a utility function that is used in feature construction
        """
        if repeat_along=="row":
            #Repeat the diagonal weight along the row
            #The columns contain the unique weights
            neighbourhood_vertex_weights = np.repeat(np.diag(matrix).reshape(1,-1),
                                                     self.graph_dim, 0).reshape(self.graph_dim, self.graph_dim, 1, 1)
            #Filter out the matrix elements that are not present in the adjacency matrix
            neighbourhood_vertex_weights = binary_matrix*neighbourhood_vertex_weights
            return neighbourhood_vertex_weights
        else:
            #Repeat the diagonal weight along the column
            #The rows contain the unique weights
            neighbourhood_vertex_weights = np.repeat(np.diag(matrix).reshape(1,-1),
                                                     self.graph_dim, 1).reshape(self.graph_dim, self.graph_dim, 1, 1)
            neighbourhood_vertex_weights = binary_matrix*neighbourhood_vertex_weights
            return neighbourhood_vertex_weights

    def __categorical_matrix(self, categorical_features, binary_matrix, num_degrees=3):
        """
        A function that takes the categorical features and constructs a matrix where this 
        feature is repeated as a column. The columns are as such equivalent and the rows are the
        a repetition of the same tensor

        This function is a utility function that is used in feature construction
        """
        cat_degree_matrix = np.repeat(categorical_features.reshape(self.graph_dim,1,num_degrees),
                                      self.graph_dim,1).reshape(self.graph_dim, self.graph_dim, 1, num_degrees)
        cat_degree_matrix = binary_matrix*cat_degree_matrix
        return cat_degree_matrix

    def triu_to_matrix(self, triu):
        """
        Convert a vector of upper triangular values to a full, symmetric matrix.

        Arguments
            :triu (np.array): A 1D numpy array containing the upper triangle values of a symmetric
                                matrix
        Returns
            :matrix (np.array): The matrix form of the upper triangle
        """
        matrix = np.zeros((self.graph_dim, self.graph_dim))
        matrix[np.triu_indices(self.graph_dim, 0)] = triu
        matrix.T[np.triu_indices(self.graph_dim, 0)] = triu
        return matrix

    def binarize_matrix(self, matrix, diagonal=True):
        """
        A function that binarizes a given matrix with the option to exclude the diagonal elements
        
        Arguments
            :matrix (np.array): A 2D numpy array that will be converted to its binary form
            :diagonal (opt,bool): A boolean that indicates whether the diagonal should be 1 or 0
        Returns
            :binary_matrix (np.array): A binary representation of the input matrix
        """
        binary_matrix = np.where(matrix!=0, 1, matrix)
        if diagonal:
            return binary_matrix.reshape(self.graph_dim, self.graph_dim, 1, 1)
        else:
            binary_matrix[np.diag_indices(self.graph_dim)]=0
            return binary_matrix.reshape(self.graph_dim, self.graph_dim, 1, 1)
    
    def adjacency_matrix(self, matrix, diagonal=None, normalize=False,
                         negative_weights=False):
        """
        A function to format the matrix into a adjacency matrix format.
        The function has the capability to change the diagonal elements of the matrix
        according to the argument given to 'diagonal'

        In addition to this we also provide the option to normalize the given adjacency matrix
        using the following formula
        
        .. math::
            Ã=D^{-1/2}AD^{-1/2}

        where the normalized is computed using the absolute value of the adjacency matrix

        Arguments
            :matrix (np.array): A numpy array that represents the graph that is currently being processed
                                  The array has the dimension (N x N) where N is the number of vertices in the graph

            :diagonal (opt,str): An optional parameter that determines the diagonal of this matrix. Standardly
                                     we set this value to None resulting in a diagonal that remains unchanged.
                                     Alternatively we can give the following keywords
        
                                     1) 'ones'-replace the diagonal elements with ones
                                     2) 'zeros'-replace the diagonal elements with zero

            :normalize (opt,bool): A boolean that determines whether the matrix should be normalized using its
                                       degree matrix (computed using the absolute values of the matrix) 

            :negative_weights (opt,bool): A boolean that is used in the determination of the added one to the
                                              diagonal (negative or positive) and how the normalization is
                                              computed
        Returns
            :adjacency_matrix (np.array): The adjacency matrix 
        """
        adjacency_matrix=np.copy(matrix)
        if diagonal=="ones":
            if normalize:
                adjacency_matrix[np.diag_indices(self.graph_dim)]=0
                if negative_weights:
                    normalization_factor = np.diag(1/np.power(np.sum(np.abs(adjacency_matrix),0),0.5))
                    return normalization_factor.dot(adjacency_matrix).dot(normalization_factor)+np.eye(self.graph_dim)
                else:
                    normalization_factor = np.diag(1/np.power(np.sum(adjacency_matrix,0),0.5))
                    return normalization_factor.dot(adjacency_matrix).dot(normalization_factor)+np.eye(self.graph_dim)
            adjacency_matrix[np.diag_indices(self.graph_dim)]=1
        elif diagonal=="zeros":
            adjacency_matrix[np.diag_indices(self.graph_dim)]=0
        if normalize:
            if negative_weights:
                normalization_factor = np.diag(1/np.power(np.sum(np.abs(adjacency_matrix),0),0.5))
                return normalization_factor.dot(adjacency_matrix).dot(normalization_factor)
            else:
                normalization_factor = np.diag(1/np.power(np.sum(adjacency_matrix,0),0.5))
                return normalization_factor.dot(adjacency_matrix).dot(normalization_factor)
        return adjacency_matrix

    def weights_nf(self, matrix, edge_weights=False):
        """
        A function that formats the weighted matrix as node_features using the self loop weight 
        as the node features. In addition to this we also provide to option to include the average
        of the edge weights as an additional feature

        Arguments
            :matrix (np.array): A 2D numpy array that contains diagonal and off-diagonal weights
                                     that parametrize the graph

            :edge_weights (opt, bool): A boolean argument that determines whether the average of the off-diagonal
                                   elements should be included as an additional node feature
        Returns
            :node_features (np.array): Numpy array where the node features are the self loop
                               weights and possibly the average of the edge weights as well
        """
        if edge_weights:
            edge_weights=np.sum(self.adjacency_matrix(matrix, diagonal="zeros"),0).reshape(-1,1)
            count = 1/np.sum(self.binarize_matrix(matrix, diagonal=False),0).reshape(-1,1)
            return np.concatenate([np.diag(matrix).reshape(-1,1),
                                   count*edge_weights],1)
        return np.diag(matrix).reshape(-1,1)
    
    def vdegree_nf(self, matrix, categorical=True, num_degrees=3):
        """
        A funtion that formats the weighted matrix to generate a vertex degree feature based on the 
        weights in the matrix. The degree is computed as the number of weights that each vertex possesses.
        In addition  we standardly enable the conversion of this integer feature to the 
        categorical form.

        Arguments
            :matrix (numpy array): A numpy array that represents the adjacency matrix that represents the
                                     graph. 

            :categorical (opt,bool): Option to convert the degree feature into the categorical format.
                                         Standard value for this argument is True
        Returns
            :vdegree_nf (np.array): A numpy array that describes the vertices in terms of their degree
        """
        vdegree_features = np.copy(matrix)
        vdegree_features = np.where(vdegree_features!=0, 1, vdegree_features)
        vdegree_features = np.sum(vdegree_features, 0)-1
        if categorical:
            return np.array([np.eye(num_degrees)[int(el)-1].flatten().tolist()
                             for el in vdegree_features.flatten()]).reshape(self.graph_dim,-1)
        else:
            return vdegree_features.reshape(self.graph_dim, -1)
        
    def vdegree_weighted_nf(self, matrix, neighbourhood=False, weight_method="average"):
        """
        A vertex degree node feature constructor that weights the categorical vector
        using different weights types. The weight types that we specify are the following options

        If "neighbourhood" is set to true we weight the categorical with the self loops but also weights 2 additional 
        categorical vectors. These 2 vectors take the following weighting into account
            - The edges weights
            - The self loops of the connecting vertices`

        When using the neighbourhood weight type we als can specify how to weight these neighbourhood
        
            1) "average", the off diagonal elements are average and subsequently used to weight
               the degree vector of the central vertex

            2) "linear combination", the off diagonal elements are weighted using the degree vector
               of the connecting vertices which are then subsequently summed and averaged per 
               degree class

        Arguments
            :matrix (numpy.array): A 2D matrix (N X N) representing the graph that is to be processed. This matrix
                                     is a square matrix that contains the weights that will be used in weighting
                                     the generated categorical vectors. The weights can either be the edge weights
                                     or the self loop weights (diagonal repeated as a row)

            :neighbourhood (opt,bool): Boolean that enables the option to include information about the neighbourhood
                                           weights. The edge weights and self loop weights of the neighbouring vertices
                                           are formatted in the categorical format. The method which this is done is 
                                           determined by the weight_method optional argument

            :weight_method (opt,str): Method by which we incorporate neighbourhood information into the node feature
                                          representation. 
                                              1) "average", neighbourhood weights are averaged and then used to weight the 
                                                 the degree vector of the central vertex
                                              2) "linear combination" neighbourhood weights are weighted with the degree vectors
                                                 of the connecting vertex and subsequently summed up and averaged, meaning that
                                                 we count the amount of neighbouring vertices have a specific degree which will be
                                                 used to rescale the summed combination
        Returns
            :vdegree_weighted_nf (numpy.array): a numpy array that describes the vertices as a categorical degree vector weighted
                                                   by its self loop weight
        """
        #Compute the degree vector
        cat_vdegree_features = self.vdegree_nf(matrix)
        #Extract the diagonal weights
        sl_cat_vdegree_features =  np.diag(matrix).reshape(-1,1)*cat_vdegree_features
        if neighbourhood:
            #Compute the binary form
            binary_matrix = self.binarize_matrix(matrix, diagonal=False)
            #Extract the edge weights
            edge_weights = self.__off_diagonal_format(matrix)
            #Construct a categorical tensor where each edge is substituted with its degree vector
            cat_degree_matrix = self.__categorical_matrix(cat_vdegree_features, binary_matrix)
            if weight_method=="average":
                #Construct the matrix where the diagonal is repeated at each row
                neighbourhood_vertex_weights = self.__diagonal_to_matrix(matrix, binary_matrix, "row")
                cat_degree_count = np.sum(cat_degree_matrix, 1)
                nonzero_indices = np.nonzero(cat_degree_count)
                for idx_1, idx_2, idx_3 in zip(nonzero_indices[0], nonzero_indices[1],nonzero_indices[2]):
                    cat_degree_count[idx_1][idx_2][idx_3] = 1/cat_degree_count[idx_1][idx_2][idx_3]
                cat_degree_count = cat_degree_count.squeeze(1)
                edge_weight_sum = np.sum(cat_degree_matrix*edge_weights, 1).squeeze(1)
                neighbour_vertex_sum = np.sum(cat_degree_matrix*neighbourhood_vertex_weights, 1).squeeze(1)
                return np.concatenate([sl_cat_vdegree_features,
                                       cat_degree_count*neighbour_vertex_sum,
                                       cat_degree_count*edge_weight_sum],1)
            elif weight_method=="linear combination":
                cat_degree_count = np.sum(cat_degree_matrix, 0)
                neighbourhood_vertex_weights = self.__diagonal_to_matrix(matrix, binary_matrix, "column")
                nonzero_indices = np.nonzero(cat_degree_count)
                for idx_1, idx_2, idx_3 in zip(nonzero_indices[0], nonzero_indices[1],nonzero_indices[2]):
                    cat_degree_count[idx_1][idx_2][idx_3] = 1/cat_degree_count[idx_1][idx_2][idx_3]
                cat_degree_count=cat_degree_count.squeeze(1)
                edge_weight_sum = np.sum(cat_degree_matrix*edge_weights, 0).squeeze(1)
                neighbour_vertex_sum = np.sum(cat_degree_matrix*neighbourhood_vertex_weights, 0).squeeze(1)
                return np.concatenate([sl_cat_vdegree_features,
                                       cat_degree_count*neighbour_vertex_sum,
                                       cat_degree_count*edge_weight_sum],1)
        return sl_cat_vdegree_features

    def pdegree_weighted_nf(self, matrix, num_degrees):
        """
        Constructs a seperate class representation that characterizes the edges that
        connect to the central vertex. This class representation is constructed as a set of tuples
        where the first element of the tuple describes the central vertex's degree and the second element
        describes the connecting vertex's degree.

        {(1,1), (1,2),..., (2,1), (2,2), ...}.

        as such this class degree will have the dimension (1 X .. math::M^2) where M is the predefined maximum degree number
        (standarly this will be set to 3 when working with organic molecules).

        Arguments
            :matrix (numpy.array): A 2D matrix (N X N) representing the graph that is to be processed. This matrix
                                     is a square matrix that contains the weights that will be used in weighting
                                     the generated categorical vectors. The weights can either be the edge weights
                                     or the self loop weights (diagonal repeated as a row).
            :num_degrees (int): The number of possible degree values
        Returns
            :pdegree_features (np.array): A numpy array containing the pair degree features
        """
        vdegree_features = self.vdegree_nf(matrix, categorical=False)
        cat_vdegree_features = self.vdegree_nf(matrix)
        sl_cat_vdegree_features =  np.diag(matrix).reshape(-1,1)*cat_vdegree_features
        binary_matrix = self.binarize_matrix(matrix, diagonal=False)
        degree_pairs = []
        for central_vertex in range(1, num_degrees+1):
            for neighbour_vertex in range(1, num_degrees+1):
                degree_pairs.append((central_vertex, neighbour_vertex))
        num_degree_pairs = len(degree_pairs)
        degree_dict = dict(zip(degree_pairs, range(1,num_degree_pairs+1)))
        pairs = list(zip(np.repeat(vdegree_features, self.graph_dim, 1).flatten(),
                     np.repeat(vdegree_features.T, self.graph_dim, 0).flatten()))
        pair_matrix = np.array([degree_dict[pair] for pair in pairs]).reshape(self.graph_dim, self.graph_dim)
        pair_matrix = np.multiply(binary_matrix.reshape(self.graph_dim, self.graph_dim), pair_matrix)
        pair_matrix = pair_matrix.flatten()
        cat_pair_matrix = []
        for el in pair_matrix:
            if el==0:
                cat_pair_matrix.append([0]*num_degree_pairs)
            else:
                cat_pair_matrix.append(np.eye(num_degree_pairs)[int(el)-1].flatten().tolist())
        cat_pair_matrix = np.array(cat_pair_matrix).reshape(self.graph_dim,self.graph_dim,-1)
        neighbourhood_vertex_weights = self.__diagonal_to_matrix(matrix, binary_matrix, "row").squeeze(2)
        edge_weights = self.__off_diagonal_format(matrix).squeeze(2)
        cat_pair_count = np.sum(cat_pair_matrix, 1)
        nonzero_indices = np.nonzero(cat_pair_count)
        for idx_1, idx_2 in zip(nonzero_indices[0], nonzero_indices[1]):
            cat_pair_count[idx_1][idx_2] = 1/cat_pair_count[idx_1][idx_2]
        cat_pair_count = cat_pair_count
        edge_weight_sum = np.sum(cat_pair_matrix*edge_weights, 1)
        neighbour_vertex_sum = np.sum(cat_pair_matrix*neighbourhood_vertex_weights, 1)
        return np.concatenate([sl_cat_vdegree_features,
                               cat_pair_count*neighbour_vertex_sum,
                               cat_pair_count*edge_weight_sum],1)
        
