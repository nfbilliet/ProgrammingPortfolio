"""
Probability is the mathematical study of randomly occurring phenomena. 
We will model such a phenomenon with a random variable, which is simply a variable that can take a number of 
different distinct outcomes depending on the result of an underlying random process.

For example, say that we have a bag containing 3 red balls and 2 blue balls. If we let X represent the random variable 
corresponding to the color of a drawn ball, then the probability of each of the two outcomes is given by Pr(X=red)=35
and Pr(X=blue)=25.

Random variables can be combined to yield new random variables. Returning to the ball example, let Y model the color of a 
second ball drawn from the bag (without replacing the first ball). The probability of Y being red depends on whether the 
first ball was red or blue. To represent all outcomes of Xand Y, we therefore use a probability tree diagram. 
This branching diagram represents all possible individual probabilities for X and Y, with outcomes at the endpoints 
("leaves") of the tree. The probability of any outcome is given by the product of probabilities along the path from the beginning of the tree; see Figure 2 for an illustrative example.

An event is simply a collection of outcomes. Because outcomes are distinct, the probability of an event can be written as the 
sum of the probabilities of its constituent outcomes. For our colored ball example, let A be the event "Y is blue." 
Pr(A) is equal to the sum of the probabilities of two different outcomes: Pr(X=blue and Y=blue)+Pr(X=red and Y=blue), 
or 310+110=25 (see Figure 2 above).

Given: Three positive integers k, m, and n, representing a population containing k+m+n organisms: k
individuals are homozygous dominant for a factor, m are heterozygous, and n are homozygous recessive.

Return: The probability that two randomly selected mating organisms will produce an individual possessing a dominant 
allele (and thus displaying the dominant phenotype). Assume that any two organisms can mate.

Sample Dataset
2 2 2
Sample Output
0.78333
"""

"""
Homozyous dominant (HoD) => 2 copies of the dominant gene are present (GG)
Heterozygous dominant (HeD) => 1 copy of the dominant gene is present and 1 cop^y of the recessive gene (Gg or gG)
Homozygous recessive (HoR) => 2 copies of the recessive gene are present (gg)

Combining DNA from two organisms means taking 1 half of the each parent and combining them to form another

HoD + HoD => GG + GG + GG + GG => 4/4 dominant
HoD + HeD => GG + GG + Gg + gG => 4/4 dominant
HoD + HoR => Gg + Gg + gG + gG => 4/4 dominant
HeD + HeD => GG + Gg + gG + gg => 3/4 dominant 
HeD + HoR => Gg + gG + gg + gg => 2/4 dominant
HeR + HeR => gg + gg + gg + gg => 0/4 dominant
"""
import numpy as np 

"""
Construct matrices that represent the probabilities of drawing a specific member of the population
Let P(i,S) be the chance that a member i belong to class k,m or n is draw given the population size S
    P(i,S) = s_i/(s_k+s_m+s_n)
where s_k, s_m, s_n and s_i represent the subpopulation sizes.
We construct a matrix that has 3 distinct rows where the probability of each subpopulation is displayed

[
    [P(k,S) P(k,S) P(k,S)],
    [P(m,S) P(m,S) P(m,S)],
    [P(n,S) P(n,S) P(n,S)]
]

After drawing the first mating partner we pick a random partner from the remaining pool and construct a matrix

[
    [P_1(k,S-1) P_1(m,S-1) P_1(n,S-1)],
    [P_2(k,S-1) P_2(m,S-1) P_2(n,S-1)],
    [P_3(k,S-1) P_3(m,S-1) P_3(n,S-1)]
]

where each row represents the situation where a different first partner is drawn
    * P_1 starts from a member from k drawn -> s_k = k-1
    * P_2 starts from a member from m drawn -> s_m = m-1
    * P_3 starts from a member from n drawn -> s_n = n-1

The dominance matrix gives the probability for each pair to result in a dominant fenotype
"""

fenotypeProbability = np.array([[1, 1, 1],[1, 0.75,0.5],[1,0.5,0]])

def probabilityTree(k, m, n, dominanceMatrix = fenotypeProbability):
    populationSize_firstDraw = k+m+n
    probabilityMatrix_firstPartner = np.array([[k,k,k],[m,m,m],[n,n,n]])/populationSize_firstDraw
    #The diagonal elements represent each population group so subtracting the identity matrix gives us the result of picking a member of this group in the first round
    #Normalization can be done by subtracting one from the size from the first round
    probabilityMatrix_secondPartner = (np.array([[k,m,n]]*3) - np.identity(3))/(populationSize_firstDraw-1)
    #Multiplying (Hadamard product) both probability matrices results in a matrix that contains all possible partner combinations and their draw probability
    #Multiplying (Hadamard product) the result from the previous mulitplication with the probability matrix describing the chance of a dominant fenotype gives us the individual chances
    #SUmming up these chances gives us the total probability of obtaining a dominant fenotype
    return np.sum(np.multiply(np.multiply(probabilityMatrix_firstPartner, probabilityMatrix_secondPartner),dominanceMatrix))

def readInp(fname):
    with open(fname, "r") as myFile:
        inpParam = myFile.read().split(" ")
        return [int(param) for param in inpParam]
    
sampleParam = readInp("rosalind_test.txt")
print(probabilityTree(sampleParam[0], sampleParam[1], sampleParam[2]))

testParam = readInp("rosalind_iprb.txt")
print(probabilityTree(testParam[0], testParam[1], testParam[2]))
