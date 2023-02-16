/*
=Task=
This Triangular Number Sequence is generated from a pattern of dots that form a triangle. 
The first 5 numbers of the sequence, or dots, are:

1, 3, 6, 10, 15

This means that the first triangle has just one dot, the second one has three dots, 
the third one has 6 dots and so on.

Write a function that returns the number of dots when given its corresponding triangle number of the sequence.

EXAMPLES

triangle(1) ➞ 1

triangle(6) ➞ 21

triangle(215) ➞ 23220
*/

#include <iostream>
using namespace std;

/*
The triangle number of any integer n can be calculated  using the binomial coefficient binom(n+1,2)

T_n = [n(n+1)]/2
*/

int triangle(int n){
    return (n*(n+1))/2;
}

int main(){
    cout << triangle(1) << "\n";
    cout << triangle(6) << "\n";
    cout << triangle(215) << "\n";
}