"""
Problem
In DNA strings, symbols 'A' and 'T' are complements of each other, as are 'C' and 'G'.

The reverse complement of a DNA string s
 is the string sc
 formed by reversing the symbols of s
, then taking the complement of each symbol (e.g., the reverse complement of "GTCA" is "TGAC").

Given: A DNA string s
 of length at most 1000 bp.

Return: The reverse complement sc
 of s
.

Sample Dataset
AAAACCCGGT
Sample Output
ACCGGGTTTT
"""

import re

sampleDNA = "AAAACCCGGT"
sampleOutput = "ACCGGGTTTT"

def reverseComplement(DNAstr):
    complementDict = dict(zip(["A", "C", "G", "T"], ["T", "G", "C", "A"]))
    rcDNA = ""
    for nucleotide in DNAstr[::-1]:
        rcDNA += complementDict[nucleotide]
    return rcDNA


def reverseComplement_rec(DNAstr):
    #Using the '|' char in the re Pattern we indicate that either of these char's are valid pattern that can be matched in the recursive expression
    #The replacement can be a str or function. When using a function we pass a Match obj to this function
    complementDict = dict(zip(["A", "C", "G", "T"], ["T", "G", "C", "A"]))
    return re.sub("A|C|G|T", lambda x: complementDict[x.group()], DNAstr[::-1])

print("The output of method 1 is equal to the expected output: %s" % (reverseComplement(sampleDNA)==sampleOutput))
print("The output of method 2 is equal to the expected output: %s" % (reverseComplement_rec(sampleDNA)==sampleOutput))


testStr = open("rosalind_revc.txt", "r").readline()[:-1]
print(reverseComplement(testStr))
print(reverseComplement_rec(testStr))