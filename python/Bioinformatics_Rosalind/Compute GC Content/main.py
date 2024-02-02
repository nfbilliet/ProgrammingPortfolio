"""
Identifying Unknown DNA Quickly

Problem
The GC-content of a DNA string is given by the percentage of symbols in the string that are 'C' or 'G'. 
For example, the GC-content of "AGCTATAG" is 37.5%. 
Note that the reverse complement of any DNA string has the same GC-content.

DNA strings must be labeled when they are consolidated into a database. 
A commonly used method of string labeling is called FASTA format. 
In this format, the string is introduced by a line that begins with '>', followed by some labeling information. 
Subsequent lines contain the string itself; the first line to begin with '>' indicates the label of the next string.

In Rosalind's implementation, a string in FASTA format will be labeled by the ID "Rosalind_xxxx", where "xxxx" denotes a four-digit code between 0000 and 9999.

Given: At most 10 DNA strings in FASTA format (of length at most 1 kbp each).

Return: The ID of the string having the highest GC-content, followed by the GC-content of that string. Rosalind allows for a default error of 0.001 in all decimal answers unless otherwise stated; please see the note on absolute error below.

Sample Dataset
>Rosalind_6404
CCTGCGGAAGATCGGCACTAGAATAGCCAGAACCGTTTCTCTGAGGCTTCCGGCCTTCCC
TCCCACTAATAATTCTGAGG
>Rosalind_5959
CCATCGGTAGCGCATCCTTAGTCCAATTAAGTCCCTATCCAGGCGCTCCGCCGAAGGTCT
ATATCCATTTGTCAGCAGACACGC
>Rosalind_0808
CCACCCTCGTGGTATGGCTAGGCATTCAGGAACCGGAGAACGCTTCAGACCAGCCCGGACTGGGAACCTGCGGGCAGTAGGTGGAAT
CCACCCTCGTGGTATGGCTAGGCATTCAGGAACCGGAGAACGCTTCAGACCAGCCCGGACTGGGAACCTGCGGGCAGTAGGTGGAAT
Sample Output
Rosalind_0808
60.919540

Note on Absolute Error

We say that a number x is within an absolute error of y to a correct solution if x is within y of the correct solution. 
For example, if an exact solution is 6.157892, then for x to be within an absolute error of 0.001, we must have that |x−6.157892|<0.001, or 6.156892<x<6.158892
.

Error bounding is a vital practical tool because of the inherent round-off error in representing decimals in a computer, where only a finite number of decimal places are allotted to any number. After being compounded over a number of operations, this round-off error can become evident. As a result, rather than testing whether two numbers are equal with x=z
, you may wish to simply verify that |x−z| is very small.

The mathematical field of numerical analysis is devoted to rigorously studying the nature of computational approximation.
"""

#fastaFile = open("rosalind_gc.txt", "r")
#print([line.split("\n")[:-1] for line in fastaFile.read().split(">")[1:]])


def formatFastaFile(fname):
    with open(fname, "r") as fastaFile:
        #The first element in the list after the initial split is an empty char after using the split function
        fastaLines = [line.split("\n") for line in fastaFile.read().split(">")[1:]]
        #The resulting sublists are fragmented DNA strings and must be joined together to form the complete string
        fastaLines = [[line[0], ("").join(line[1:])] for line in fastaLines]
        #Return a list containing lists that each represent a FASTA line where the first element is the ID and the second is the DNA string
        return fastaLines

def calculateGCcontent(DNAstr, decimal=6):
    GCcounter = 0
    for nucleotide in DNAstr:
        if nucleotide=="C" or nucleotide=="G":
            GCcounter+=1
    #Round the percentage to a decimal of choice 
    return round(GCcounter/len(DNAstr)*100, decimal)

def selectHighGC(fname):
    fastaLines = formatFastaFile(fname)
    GCcontent = [calculateGCcontent(fastaLine[1]) for fastaLine in fastaLines]
    #Force print up to 6 decimal points
    print(fastaLines[GCcontent.index(max(GCcontent))][0]+"\n"+"%.6f" % max(GCcontent))

selectHighGC("rosalind_gc.txt")
#"""