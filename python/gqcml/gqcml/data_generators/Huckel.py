import numpy as np
import scipy as sp

class HuckelSolver():
    """
    A class that provides the utilities to solve the Schrödinger equation
    for the Hückel model. This class contains the following objects

    Attributes
        :eigenvals (np.array): An attribute that stores the eigenvalues of the last computed system.
                                     The standard value for this attribute is 0
        :eigenvecs (np.array): An attribute that stores the eigenvectors of the last computed system.
                                     The standard value for this attribute is 0
        :ONV_a (np.array): An attribute that stores the alpha occupation number vector of the last computed system.
                                 The standard value for this attribute is 0
        :ONV_b (np.array): An attribute that stores the beta occuptation number vector of the last computed system.
                                 The standard value for this attribute is 0
        :P_a (np.array): An attribute that stores the alpha density matrix of the last computed system.
                               The standard value for this attribute is 0
        :P_b (np.array): An attribute that stores the beta density matrix of the last computed system.
                               The standard value for this attribute is 0
        :P (np.array): An attribute that stores the total density matrix of the last computed system.
                             The standard value for this attribute is 0
        """
    def __init__(self):
        self.eigenvals=0
        self.eigenvecs=0
        self.ONV_a=0
        self.ONV_b=0
        self.P_a = 0
        self.P_b = 0
        self.P = 0

    def ONV(self, eigenvals, N, N_a, N_b):
        """
        Constructs the occupation number vectors that determines the filling of the electrons in the
        spin orbitals. This functions takes degenerate states into account as well

        Arguments
            :eigenvals (np.array): A 1D array containing the eigenvalues of the system
            :N (int): The amount of spin orbitals in the system, i.e. the maximum number
                            of electrons in the ONV
            :N_a (int): The amount of alpha electrons in the system
            :N_b (int): The amount of beta electrons in the system
        Returns
            :ONV (np.array): The occupation number vector for both alpha and beta are updated
        """
        #Search for the degenerate eigenvalues. This results in blocks in the occuptation matrix
        weight_matrix = np.isclose(np.repeat(eigenvals.reshape(-1,1), N, axis=1),
                                   np.repeat(eigenvals.reshape(1,-1), N, axis=0)).astype(int)
        #Determine the degeneracy of the eigenvalues
        degeneracy = np.diag(1/np.sum(weight_matrix, 0))
        #Weigh the elements of the occupation matrix with the degeneracy factor
        weight_matrix = degeneracy.dot(weight_matrix)
        self.ONV_a= np.array([1]*N_a+[0]*(N-N_a)).dot(weight_matrix)
        self.ONV_b = np.array([1]*N_b+[0]*(N-N_b)).dot(weight_matrix)
        return None

    def solve_ndo(self, H):
        """
        A function that solves the Schrodinger equation working under the assumption of non-differential overlap
        
        Arguments
            :H (np.array): A (N x N) numpy array that represents the system that needs to be computed
        Returns
            :None: The function does computes the eigenvalues and eigenvectors of the given matrix H
                      using the eigh function from numpy. These solutions are stored in the corresponding attributes
        """
        N = H.shape[0]
        self.eigenvals, self.eigenvecs = np.linalg.eigh(H)
        return None

    def solve_general(self, H, S):
        """
        A function that solves the Schrodinger equation working when including a general overlap

        Arguments
            :H (np.array): A (N x N) numpy array that represents the system that needs to be computed
            :S (np.array): A (N x N) numpy array that contains the overlap values associated with the 
                           given H
        Returns
            :None: The function does computes the eigenvalues and eigenvectors of the given matrix H
                    using the eigh function from scipy. These solutions are stored in the corresponding attributes
        """
        self.eigenvals, self.eigenvecs = sp.linalg.eigh(H, S, eigvals_only=False)
        return None

    def compute_energy(self, N_a, N_b):
        """
        Computes the molecular energy in the Huckel model based on the occupation of 
        alpha and beta electrons of the molecular orbitals. This functions assumes that
        the lowest eigenvalues are the first elements 

        Arguments
            :N_a (int): The number of alpha electrons
            :N_b (int): The number of beta electrons
        Returns
            :E (float): A floating point value that corresponds to the total energy of the system
                               when contain N_a and N_b electrons
        """
        N = len(self.eigenvals)
        self.ONV(self.eigenvals, N, N_a, N_b)
        E = self.eigenvals.dot(self.ONV_a)+self.eigenvals.dot(self.ONV_b)
        return E                

    def compute_density_matrix(self, N_a, N_b):
        """
        Computes the groundstate density of based on the ONV
        
        Arguments
            :N_a (int): The number of alpha electrons.
            :N_b (int): The number of beta electrons.
        Returns
            :P (np.array): A (N x N) numpy array that represents the total electron density matrix from the system
                                  when it contains N_a and  N_b electrons
        """
        N = len(self.eigenvals)
        self.ONV(self.eigenvals, N, N_a, N_b)
        P_a = np.zeros((N, N))
        P_b = np.zeros((N, N))
        for eigenvec_idx in range(len(self.eigenvals)):
            #Columns of the eigenvector matrix represent the eigenvectors
            MO = self.eigenvecs[:,eigenvec_idx]
            #Construct the density of the MO
            P_MO = MO.reshape(-1,1)*MO.reshape(1,-1)
            #Compute the spin components of the density
            P_a += self.ONV_a[eigenvec_idx]*P_MO
            P_b += self.ONV_b[eigenvec_idx]*P_MO
        self.P_a = P_a
        self.P_b = P_b
        #The total density is the sum of the spin component densities
        self.P = P_a+P_b
        return P_a+P_b
