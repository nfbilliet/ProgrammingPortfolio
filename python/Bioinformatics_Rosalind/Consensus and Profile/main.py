"""
A matrix is a rectangular table of values divided into rows and columns. An m×n matrix has m rows and n columns. 
Given a matrix A, we write Ai,j to indicate the value found at the intersection of row i and column j.

Say that we have a collection of DNA strings, all having the same length n. 
Their profile matrix is a 4×n matrix P in which P1,j represents the number of times that 'A' occurs in the jth 
position of one of the strings, P2,j represents the number of times that C occurs in the j
th position, and so on (see below).

A consensus string c is a string of length n formed from our collection by taking the most common symbol at each position; 
the jth symbol of c therefore corresponds to the symbol having the maximum value in the j-th column of the profile matrix. 
Of course, there may be more than one most common symbol, leading to multiple possible consensus strings.

Given: A collection of at most 10 DNA strings of equal length (at most 1 kbp) in FASTA format.

Return: A consensus string and profile matrix for the collection. (If several possible consensus strings exist, then you may return any one of them.)

Sample Dataset
>Rosalind_1
ATCCAGCT
>Rosalind_2
GGGCAACT
>Rosalind_3
ATGGATCT
>Rosalind_4
AAGCAACC
>Rosalind_5
TTGGAACT
>Rosalind_6
ATGCCATT
>Rosalind_7
ATGGCACT

Sample Output
ATGCAACT
A: 5 1 0 0 5 5 0 0
C: 0 0 1 4 2 0 6 1
G: 1 1 6 3 0 1 0 0
T: 1 5 0 0 0 1 1 6
"""
import numpy as np

def fastaToNucleotides(fname):
    with open(fname, "r") as myFile:
        DNAstrings = ["".join(DNAstring.split("\n")[1:]) for DNAstring in myFile.read().split(">")[1:]]
        #Unpack the concatenated string into individual characters using the * operator
        return [[*DNAstring] for DNAstring in DNAstrings]

#print([[*el] for el in ["".join(DNAstring) for DNAstring in DNAstrings]])
nucleotides = ["A", "C", "G", "T"]
ohEncodedNucleotides = [[1,0,0,0], 
                        [0,1,0,0],
                        [0,0,1,0],
                        [0,0,0,1]]

nucleotideToVec = dict(zip(nucleotides, ohEncodedNucleotides))
vecToNucleotide = dict(zip([0,1,2,3],["A","C","G","T"]))

def consensusDNA(DNAstrings):
    """
    Convert the nucleotides to their 4D vector representation
        A = [1,0,0,0]
        C = [0,1,0,0]
        G = [0,0,1,0]
        T = [0,0,0,1]
    Convert the string to a row of vectors

    The consensus string is the obtained by taking the sum of the rows and projecting out the component that has the largest contribution
    The summary of the individual nucleotides can be obtained by summing up the rows and projecting out the component of interest
    """
    vectorizedStrings = np.array([[nucleotideToVec[nucleotide] for nucleotide in DNAstring] for DNAstring in DNAstrings])
    #The profile matrix is the sum of the rows
    profileMatrix = np.sum(vectorizedStrings, axis=0)
    consensusDNAStr = "".join([vecToNucleotide[idx] for idx in np.argmax(profileMatrix, axis=1)])
    print(consensusDNAStr)
    for row, nucleotide in zip(profileMatrix.T, ["A", "C", "G", "T"]):
        print(nucleotide + ": " + " ".join([str(rowEl) for rowEl in row]))

DNAstrings = fastaToNucleotides("rosalind_cons.txt")
consensusDNA(DNAstrings)