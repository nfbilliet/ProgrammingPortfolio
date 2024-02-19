"""
Recall the definition of the Fibonacci numbers from “Rabbits and Recurrence Relations”, which followed the 
recurrence relation Fn=Fn−1+Fn−2 and assumed that each pair of rabbits reaches maturity in one month and produces 
a single pair of offspring (one male, one female) each subsequent month.

Our aim is to somehow modify this recurrence relation to achieve a dynamic programming solution in the case that 
all rabbits die out after a fixed number of months. See Figure 4 for a depiction of a rabbit tree in which rabbits 
live for three months (meaning that they reproduce only twice before dying).

Given: Positive integers n≤100 and m≤20.

Return: The total number of pairs of rabbits that will remain after the n-th month if all rabbits live for m months.

Sample Dataset

6 3

Sample Output

4
"""

"""
New recursion relationship for the Fibonacci Rabbits
    * Each pair produces a new pair of rabbits
    * A newly produced pair of rabbits starts reproducing after 1 month
    * A pair of rabbits dies after m months

n_0(1) [1]
n_0(2) [2]
n_0(3)+n_1(1) [3, 1]
n_1(2) + n_2(1) [2,1]
n_1(3) + n_2(2) + n_3(1)  [3,2,1]
n_2(3) + n_3(2) + n_4(1) + n_5(1) [3, 2, 1, 1]  
"""

def MortalFibonacciRabbits(n,m, starting_pop = 1):
    rabbitPopulation = [1]*starting_pop
    counter = 1
    while counter<n:
        newRabbitPopulation = []
        for rabbitPair in rabbitPopulation:
            if rabbitPair == 1:
                newRabbitPopulation.append(2)
            elif rabbitPair > 1 and rabbitPair < m:
                newRabbitPopulation += [rabbitPair+1,1]
            else:
                newRabbitPopulation += [1]
        rabbitPopulation = newRabbitPopulation
        counter += 1
    return len(rabbitPopulation)

print(MortalFibonacciRabbits(100,20))

"""
1 -> 2 -> 3,1 -> 2,1 -> 3,2,1 -> 3,2,1,1 -> 3,2,2,1,1
"""