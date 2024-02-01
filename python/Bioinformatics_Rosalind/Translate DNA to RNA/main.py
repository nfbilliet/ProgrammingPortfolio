"""
Problem
An RNA string is a string formed from the alphabet containing 'A', 'C', 'G', and 'U'.

Given a DNA string t
 corresponding to a coding strand, its transcribed RNA string u
 is formed by replacing all occurrences of 'T' in t
 with 'U' in u
.

Given: A DNA string t
 having length at most 1000 nt.

Return: The transcribed RNA string of t
.

Sample Dataset
GATGGAACTTGACTACGTAAATT
Sample Output
GAUGGAACUUGACUACGUAAAUU
"""

import re

def translateDNA(DNAstr):
    return DNAstr.replace('T', 'U')

def translateDNA_rec(DNAstr):
    return re.sub("T", "U", DNAstr)


testStr = "GATGGAACTTGACTACGTAAATT"
testOutput = "GAUGGAACUUGACUACGUAAAUU"

translateDNA_1 = translateDNA(testStr)
translateDNA_2 = translateDNA_rec(testStr)

print("Output of translateDNA is equivalent to expected: %s" % (translateDNA_1==testOutput))
print("Output of translateDNA_rec is equivalent to expected: %s" % (translateDNA_2==testOutput))

dataset = open("rosalind_rna.txt", "r").readline()[:-1] #-1 indexing to prevent the inclusion of the newline character
print(translateDNA(dataset))
print(translateDNA_rec(dataset))
