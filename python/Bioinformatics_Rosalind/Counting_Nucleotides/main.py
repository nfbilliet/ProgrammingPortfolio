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

#Make a large test string to be more representative of an actual genome sequence
# Chromosomal DNA ranges from 50.10^6 to 250.10^6 bp
nmb_BP = 1000000
testNucleotideStr = ["A"]*nmb_BP+["C"]*nmb_BP+["G"]*nmb_BP+["T"]*nmb_BP
random.shuffle(testNucleotideStr)
testNucleotideStr = "".join(testNucleotideStr)

#Method 1: Built in count functionality

method1_beginTime = time.time()
nucleotideCount = [testNucleotideStr.count("A"), 
                   testNucleotideStr.count("C"),
                   testNucleotideStr.count("G"),
                   testNucleotideStr.count("T")]
method1_endTime = time.time()

print(nucleotideCount)
print("Time of execution of method 1: %s sec" % (method1_endTime-method1_beginTime))

#Method 2: Dictionary method

nucleotideDict = dict(zip(["A", "C", "G", "T"], [0]*4))

method2_beginTime = time.time()
for nucleotide in testNucleotideStr:
    nucleotideDict[nucleotide] += 1
method2_endTime = time.time()

print(nucleotideDict)
print("Time of execution of method 2: %s sec" % (method2_endTime-method2_beginTime))

#Method 3: collections.Counter

method3_beginTime = time.time()
nucleotideCounter = collections.Counter(testNucleotideStr)
method3_endTime = time.time()
print(nucleotideCounter)
print("Time of execution of method 3: %s sec" % (method3_endTime - method3_beginTime))
