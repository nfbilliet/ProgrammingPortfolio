#include <iostream>
using namespace std;
/*
Compound Assignment Operators

Number operators
1) *= ->Multiply the value of the first operand by the value of the second operand; 
        store the result in the object specified by the first operand.
2) /= ->Divide the value of the first operand by the value of the second operand; 
        store the result in the object specified by the first operand.
3) %= ->Take modulus of the first operand specified by the value of the second operand; 
        store the result in the object specified by the first operand.
4) += ->Add the value of the second operand to the value of the first operand; 
        store the result in the object specified by the first operand.
5) -= ->Subtract the value of the second operand from the value of the first operand; 
        store the result in the object specified by the first operand.

Bit operators
6) <<= ->Shift the value of the first operand left the number of bits specified by the value of the second operand; 
         store the result in the object specified by the first operand
7) >>= ->Shift the value of the first operand right the number of bits specified by the value of the second operand; 
         store the result in the object specified by the first operand.

Logical operators
8) &= -> Obtain the bitwise AND of the first and second operands; 
         store the result in the object specified by the first operand.
9) ^= -> Obtain the bitwise EXCLUSIVE OR of the first and second operands; 
         store the result in the object specified by the first operand.
10) |= -> Obtain the bitwise INCLUSIVE OR of the first and second operands; 
          store the result in the object specified by the first operand.
*/
int main(){
    int value {45};
    cout << "The initial value is " << value << endl;

    value += 5;
    cout << "The value after compound addition (+=5) is " << value << endl;

    value = 45;
    value -= 5;
    cout << "The value after compound subtraction (-=5) is " << value << endl;

    value = 45;
    value *= 5;
    cout << "The value after compound multiplication (*= 5) is " << value << endl;

    value = 45;
    value /= 5;
    cout << "The value after compound division (/= 5) is " << value << endl;

    value = 45;
    value %= 2;
    cout << "The value after compound modulo (%= 2) is " << value << endl;    
    return 0;
}