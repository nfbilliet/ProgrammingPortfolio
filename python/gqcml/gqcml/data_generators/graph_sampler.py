import numpy as np
from itertools import permutations, combinations

class graph_sampler():
    """
    An object used in the generation of randomly sampled chemical structures
    using the adjacency matrix as a representation of the molecular structure

    Attributes
        :sites (int): An integer denoting the amount of sites present in the system(s) which will sampled  
    """
    def __init__(self, sites):
        self.sites = sites

    def generate_diagonal_vector(self, nmb_el_type):
        """
        A function that generates a set of vectors that specifies all possible combinations of the diagonal elements of the adjacency matrix. 
        
        Arguments
            :nmb_el_type (list): A list that contains the number of occurence of each unique element, 
                                   e.g. suppose we have a diagonal of length 4 with 2 unique elements in equal occurence then this would 
                                   correspond with [2,2]
        Returns
            :List of lists: A set of vectors that contain all possible permutations of a vector that has the 
                            specified ratios of these elements. E.g. for 2 unique elements in a diagonal of length 4 (equal ratios)
                            this would return [[1,1,2,2],[1,2,1,2], [2,1,1,2] 
        """
        diagonals = []
        for idx, nmb in enumerate(nmb_el_type):
            diagonals += [idx+1]*nmb
        #Generate all permutations of the starting diagonal and filter out the redundant set using the set data type
        diagonals = set(list(permutations(diagonals)))
        return [list(diagonal) for diagonal in diagonals]

    def convert_triu_to_mat(self, triu_vector):
        """
        Converts the upper triangle representation of a graph to the full matrix form

        Arguments
            :triu_vector (np.array): An upper triangle vector corresponding to the graph of interest
        Returns
            :adjacency_matrix (np.array): The matrix form of the input triu
        """
        adjacency_matrix = np.zeros((self.sites, self.sites))
        adjacency_matrix[np.triu_indices(self.sites,0)]=triu_vector
        adjacency_matrix.T[np.triu_indices(self.sites,0)]=triu_vector
        return adjacency_matrix

    def permutate_matrix(self, matrix, permutations):
        """
        Generates all possible permutations of a matrix where the permutation changes the order of the rows
        and columns in the same way

        Arguments
            :matrix (np.array): The matrix that is to be permutated
            :permutations (list): A list of lists where each sublist contains the order of the rows and columns
        Returns
            :permutated_matrices (list): A list of all the permutated matrices
        """
        permutated_matrices = []
        for perm in permutations:
            permutated_matrices.append(np.take(np.take(matrix, perm, axis=0), perm, axis=1))
        return permutated_matrices

    def sample_homogeneous_matrix(self, triu_vector, amount_samples,
                                  diagonal_interval=[-5,0.001], off_diagonal_interval=[-5,-0.001]):
        """        
        A function that takes a upper triangle of a homogeneous systems, i.e. a graph consisting of a single
        vertex type, and generates an amount of samples within the specified sampling ranges

        Arguments
            :triu_vector (np array): A upper triangle np array that describes the structure of the system
                                     The array consists of 0's and 1's where the 1 signifies a weight.
            :amount_samples (int): An integer that determines how many samples need to be generated
            :diagonal_interval (opt, list): A list of floats that determines the lower and upper range 
                                            of the uniform random distribution used in the generation of the samples
                                            for the diagonal elements of the adjacency matrix
            :off_diagonal_interval (opt, list): A list of floats that determines the lower and upper range
                                                of the uniform random distribution used in the generation of the samples
                                                for the off-diagonal elements of the adjacency matrix
        Returns
            :sampled_trius (list): A list of numpy arrays containing the upper triangle vector sampled randomly
        """
        diagonal_distribution=np.random.uniform(diagonal_interval[0], diagonal_interval[1], amount_samples)
        off_diagonal_distribution=np.random.uniform(off_diagonal_interval[0], off_diagonal_interval[1], amount_samples)
        adjacency_matrix = self.convert_triu_to_mat(triu_vector)
        sampled_trius=[]
        for diagonal_el, off_diagonal_el in zip(diagonal_distribution, off_diagonal_distribution):
            sampled_matrix = np.copy(adjacency_matrix)
            sampled_matrix = np.where(sampled_matrix==1, off_diagonal_el, sampled_matrix)
            sampled_matrix[np.diag_indices(self.sites)]=diagonal_el
            sampled_trius.append(sampled_matrix[np.triu_indices(self.sites,0)])
        return sampled_trius

    def sample_inhomogeneous_matrix(self, diagonal_vector, triu_vector, amount_samples,
                      diagonal_interval=[-5,0.001], off_diagonal_interval=[-5,-0.001]):
        """
        Constructs a weighted adjacency matrix sampled uniformly based on the symbolic assignment of the elements
            - The diagonal elements are assigned symbolic through integers. These integers will be replaced by random values
            - Off diagonal elements are sampled based on the the diagonal indices
        
        This function will thus generate an adjacency matrix that has unique weights for every type of bond.
        A type of bond is considered to be the edge between a pair of diagonal weihgts.

        Arguments
            :diagonal_vector (np array): A np array of integers that symbolic denotes the type of vertex.
            :triu_vector (np array): A upper triangle np array that describes the structure of the system
                                           The array consists of 0's and 1's where the 1 signifies a weight.
            :amount_samples (int): An integer that determines how many samples need to be generated
            :diagonal_interval (opt, list): A list of floats that determines the lower and upper range
                                                  of the uniform random distribution used in the generation of the samples
                                                  for the diagonal elements of the adjacency matrix
            :off_diagonal_interval (opt, list): A list of floats that determines the lower and upper range
                                                      of the uniform random distribution used in the generation of the samples
                                                      for the off-diagonal elements of the adjacency matrix
        Returns
            :sampled_trius (list): A list of numpy arrays containing the upper triangle vector sampled randomly
        """
        #We repeat the symbolic diagonal along the row axis
        row_matrix = np.repeat(np.array([diagonal_vector]), self.sites, 0)
        adjacency_matrix = self.convert_triu_to_mat(triu_vector)
        #Converts the row matrix into a sparse matrix based on the adjacency_matrix
        row_matrix = np.multiply(adjacency_matrix, row_matrix)
        
        number_distributions = max(diagonal_vector)
        sampled_adjacency_matrices=[]
        off_diagonal_samples = np.random.uniform(off_diagonal_interval[0], off_diagonal_interval[1], (number_distributions, amount_samples))
        for rand_idx in range(amount_samples):
            sampled_row_matrix =np.copy(row_matrix)
            for	idx in range(number_distributions):
                sampled_row_matrix=np.where(sampled_row_matrix==idx+1, off_diagonal_samples[idx][rand_idx],sampled_row_matrix)
            #We average the sampled row matrix with its transposed form. When doing this we ensure that sites that describe the same type
            #i.e those that have the same integer in the diagonal have the a different value than the coupling between two vertices with different
            #integers.
            sampled_adjacency_matrices.append(0.5*(sampled_row_matrix+sampled_row_matrix.T))

        diagonal_samples = np.random.uniform(diagonal_interval[0], diagonal_interval[1], (number_distributions, amount_samples))
        sampled_diagonals = []
        for rand_idx in range(amount_samples):
            sampled_diagonal = np.array(diagonal_vector)
            for idx in range(number_distributions):
                sampled_diagonal=np.where(sampled_diagonal==idx+1, diagonal_samples[idx][rand_idx],sampled_diagonal) 
            sampled_diagonals.append(sampled_diagonal)

        sampled_trius = []
        for diagonal, adjacency in zip(sampled_diagonals, sampled_adjacency_matrices):
            adjacency[np.diag_indices(self.sites)]=diagonal
            sampled_trius.append(adjacency[np.triu_indices(self.sites, 0)])
        return sampled_trius
