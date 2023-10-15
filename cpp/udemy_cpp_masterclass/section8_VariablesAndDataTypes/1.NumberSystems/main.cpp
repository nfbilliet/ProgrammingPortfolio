#include <iostream>

/*
Number systems

How can we efficiently store and describe data to the hardware?

Humans use a decimal number system to describe everything

    e.g. 2715 = 2000 + 700 + 10 + 5
              = 2.1000 + 7.100 + 1.10 + 5.1
              = 2.10.10.10 + 7.10.10 + 1.10 + 5.1
              = 2.10^3 + 7.10^2 + 1.10^1 + 5.10^0
         The entire number can be decomposed into factors of 10

Computers store data in a binary format, i.e. 0 and 1, and thus requires us to convert our method in it.
The way we can achieve this for the binary system is by writing everything in terms of powers of 2

    e.g. 100101 -> is a binary of length 6 -> 2^5 to 2^0 (6 factors of 2)
                -> 1.2^5 + 0.2^4 + 0.2^3 + 1*2^2 + 0.2^1 + 1.2^0
                -> 32 + 0 + 0 + 4 + 0 + 1
                -> 37 (base ten number of 100101 binary number)
                
Using the binary system we can enconde for decimal numbers based on the number of bits, i.e. the number of 0/1 states that we write down.

    n bits => encodes from 0 to (2^n - 1) numbers
    1 bit => 0 to 1
    2 bits => 0 to 3
    3 bits => 0 to 7
    ...
    8 bits => 0 to 255
    ...
    16 bits => 0 to 65 535
    ...
    32 bits => 0 to 4 294 967 295
    ...
    64 bits => 0 to 1.8446744e+19
    ...

In computer science a system that is often used is the hexadecimal system to group 4 bits (nibbles) together
    Binary  Hexadecimal
    0000    0
    0001    1
    0010    2
    0011    3
    0100    4
    0101    5
    0110    6
    0111    7
    1000    8
    1001    9
    1010    A (10)
    1011    B (11)
    1100    C (12)
    1101    D (13)
    1110    E (14)
    1111    F (15)

This allows us to convert long strings of bits into a human friendly way to read them.
In C and in C++ the conversion of such strings of bits is always preceded by 0x prefix

    e.g.   01101110001100001111000100111111
           0110 1110 0011 0000 1111 0001 0011 1111 (group 4 bits)
           6    E    3    0    F    1    3    F
           0x6E30F13F

If a binary number can not be parsed into groups of 4 the remaining bits on the left will be padded by 0's until a quartet of bits can be achieved

    e.g. 100100100100010111010
         1 0010 0100 1000 1011 1010 (split into quartets where a single bit is left ungrouped)
         0001 0010 0100 1000 1011 1010 (pad with 3 0's until a quartet is reached)
         1    2    4    8    B    A (convert to hexadecimal numbers)
         0x1248BA

The octal system can be used in a similar way to the decimal system. In this case, instead of ordering bits into quartets 
we order them into triplets

    Binary  Octal
    000     0
    001     1
    010     2
    011     3
    100     4
    101     5
    110     6
    111     7

A similar algorithm is followed when converting binary to octal. The main difference between the octal
and hexadecimal notation in C/C++ is that octal formatting starts with a 0 instead of 0x
*/

int main(){
    /*
    A byte is the smallest unit of uniformation and is standardly defined as a collection of 8 bits
    Using the formula from above we can compute how many numbers we can represent using 8 bits as
    (2^8-1) which results in 255 different numbers. Because negative numbers are included the range of integers
    is between [-127, 127]. In the example we will use 15 as our example which falls within this range.
    */
    int number = 15;
    // Octal numbers are represented using a 0 at the front
    // grouping in triplets results in 000 001 111 == 017
    int octal_number = 017;
    // Hexadecimal numbers are represented using 0x at the front
    // in hexadecimal 1111 is f and 0000 is 0
    int hexa_number = 0x0f;
    // Binary numbers are represented using 0b at the front
    // 8 bits mean 128, 64, 32, 16, 8, 4, 2, 1
    // 15 = 8+4+2+1 -> 00001111 
    int bin_number = 0b00001111;

    std::cout << "The number is " << number << std::endl;
    std::cout << "The octal number is " << octal_number << std::endl;
    std::cout << "The hexadecimal number is " << hexa_number << std::endl;
    std::cout << "The binary number is " << bin_number << std::endl;
    return 0;
}