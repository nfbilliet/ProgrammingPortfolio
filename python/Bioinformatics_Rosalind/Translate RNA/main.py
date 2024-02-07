"""
Problem
The 20 commonly occurring amino acids are abbreviated by using 20 letters from the English alphabet (all letters except for B, J, O, U, X, and Z). Protein strings are constructed from these 20 symbols. Henceforth, the term genetic string will incorporate protein strings along with DNA strings and RNA strings.

The RNA codon table dictates the details regarding the encoding of specific codons into the amino acid alphabet.

Given: An RNA string s
 corresponding to a strand of mRNA (of length at most 10 kbp).

Return: The protein string encoded by s
.

Sample Dataset
AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA
Sample Output
MAMAPRTEINSTRING
"""
import re 

def readInp(fname):
    with open(fname, "r") as myFile:
        inpLine = myFile.readline()
        return inpLine


def constructCodonTable(codonTableFname):
    """
    Read in the txt file with the codon amino acid pairs
    The file is structured as a series of lines where the codon pair is followed by the amino acid seperated by a space
    """
    with open(codonTableFname, "r") as myFile:
        dictLines = myFile.read()
        #Substitute all newline and space characters with a comma
        dictLines = re.sub("\n|\s", ",", dictLines)
        #Split the string based on the comma character and only keep the elements that are not empty strings
        dictLines = [strEl for strEl in dictLines.split(",") if strEl]
        dictKeys = []
        dictVals = []
        for idx in range(len(dictLines)):
            #Seperate the entries in the file into keys and values
            #Alternating from triplet to AA
            #all even index elements in the list are codon triplets, i.e. idx%2 == 0
            #all odd index elements in the list are AA, i.e. idx%2 == 1
            if idx%2 == 0:
                dictKeys.append(dictLines[idx])
            else:
                dictVals.append(dictLines[idx])
    return dict(zip(dictKeys, dictVals))

codonDict = constructCodonTable("codonTable.txt")
stopKeys = [key for key, val in codonDict.items() if val == "Stop"]
[codonDict.pop(stopKey, None) for stopKey in stopKeys]

def translateRNA(RNAstring, codonDict=codonDict, stopKeys=stopKeys):
    #Split RNAstring into triplet structure
    tripletRNA = re.findall("...?", RNAstring)
    #Generate a list that contain all non stop codons that can be transcribed
    translatableRNA = [triplet for triplet in tripletRNA if triplet not in stopKeys]
    return ("").join([codonDict[triplet] for triplet in translatableRNA])
    #Locate the stop codon 
    #translatedProtein = [dict[triplet] for triplet in tripletRNA if ]

RNAstr = readInp("rosalind_prot.txt")
print(translateRNA(RNAstr))