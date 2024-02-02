"""
Given two strings s and t of equal length, the Hamming distance between s and t, denoted dH(s,t), 
is the number of corresponding symbols that differ in s and t. See Figure 2.

Given: Two DNA strings s
 and t
 of equal length (not exceeding 1 kbp).

Return: The Hamming distance dH(s,t)

Sample Dataset

GAGCCTACTAACGGGAT
CATCGTAATGACGGCCT

Sample Output
7
"""
import os

#Extract current directory
cwd = os.path.dirname(__file__)

def HammingDistance(DNAstr_1, DNAstr_2):
    distance = 0
    for idx in range(len(DNAstr_1)):
        if DNAstr_1[idx]!=DNAstr_2[idx]:
            distance += 1
    return distance

def extractStr(fname):
    with open(cwd+"\\"+fname, "r") as myFile:
        DNAstrings = myFile.read().splitlines()
    return DNAstrings

def computeDistance(fname):
    DNAstrings = extractStr(fname)
    return HammingDistance(DNAstrings[0], DNAstrings[1])

print(computeDistance("rosalind_hamm.txt"))