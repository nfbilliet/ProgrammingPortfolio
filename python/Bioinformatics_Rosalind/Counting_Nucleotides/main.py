"""
***Counting nucleotides problem***

A string is simply an ordered collection of symbols selected from some alphabet and formed into a word; the length of a string is the number of symbols that it contains.

An example of a length 21 DNA string (whose alphabet contains the symbols 'A', 'C', 'G', and 'T') is "ATGCTTCAGAAAGGTCTTACG."

Given: A DNA string s
 of length at most 1000 nt.

Return: Four integers (separated by spaces) counting the respective number of times that the symbols 'A', 'C', 'G', and 'T' occur in s.

Sample Dataset
AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC
Sample Output
20 12 17 21
"""
import time 
import collections
import random

DNAstr = open("rosalind_dna.txt", 'r').readline()[:-1]

print([DNAstr.count("A"), DNAstr.count("C"), DNAstr.count("G"), DNAstr.count("T")])

#Make a large test string to be more representative of an actual genome sequence
# Chromosomal DNA ranges from 50.10^6 to 250.10^6 bp
"""
nmb_BP = 1
testNucleotideStr = ["A"]*nmb_BP+["C"]*nmb_BP+["G"]*nmb_BP+["T"]*nmb_BP
random.shuffle(testNucleotideStr)
testNucleotideStr = "".join(testNucleotideStr)
"""
#Method 1: Built in count functionality

def nucleotideCount(inpStr):
    nucleotideCount = [inpStr.count("A"), 
                       inpStr.count("C"),
                       inpStr.count("G"),
                       inpStr.count("T")]
    
    return(" ".join([str(el) for el in nucleotideCount]))

#Method 2: Dictionary method

def nucleotideDictCount(inpStr):
    nucleotideDict = dict(zip(["A", "C", "G", "T"], [0]*4))
    for nucleotide in inpStr:
        nucleotideDict[nucleotide] += 1
    return(" ".join([str(el) for el in nucleotideDict.values()]))

#Method 3: collections.Counter

def nucleotideCollections(inpStr):
    nucleotideCounter = collections.Counter(DNAstr)
    return(" ".join([str(nucleotideCounter["A"]), str(nucleotideCounter["C"]), str(nucleotideCounter["G"]), str(nucleotideCounter["T"])]))

print(nucleotideCount(DNAstr))
print(nucleotideDictCount(DNAstr))
print(nucleotideCollections(DNAstr))