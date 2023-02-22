/*
Your job is to create a function, that takes 3 numbers: a, b, c
and returns true if the last digit of a * b = the last digit of c. 
Check the examples below for an explanation.

Examples

lastDig(25, 21, 125) ➞ true
// The last digit of 25 is 5, the last digit of 21 is 1, and the last
// digit of 125 is 5, and the last digit of 5*1 = 5, which is equal
// to the last digit of 125(5).

lastDig(55, 226, 5190) ➞ true
// The last digit of 55 is 5, the last digit of 226 is 6, and the last
// digit of 5190 is 0, and the last digit of 5*6 = 30 is 0, which is
// equal to the last digit of 5190(0).

lastDig(12, 215, 2142) ➞ false
// The last digit of 12 is 2, the last digit of 215 is 5, and the last
// digit of 2142 is 2, and the last digit of 2*5 = 10 is 0, which is
// not equal to the last digit of 2142(2).

Notes

Numbers can be negative.
*/

#include <iostream>
 using namespace std;

bool lastDig(int a, int b, int c){
    // The last digit of an integer can be computed through the modulo operator.
    // When diving any number by 10 then the remainder of the division is the last digit.
    int last_a = a%10;
    int last_b = b%10;
    int last_c = c%10;
    // the product of the last digits must be divided by 10 as well to obtain a single digit result
    if ((last_a*last_b)%10==last_c){
        return true;
    }
    else {
        return false;
    }
}

int main(){
    cout << lastDig(25, 21, 125) << "\n";
    cout << lastDig(55, 226, 5190) << "\n";
    cout << lastDig(12, 215, 2142) << "\n";
}