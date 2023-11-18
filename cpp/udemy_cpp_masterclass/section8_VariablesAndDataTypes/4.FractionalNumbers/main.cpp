#include <iostream>
#include <iomanip>
/*
Fractional numbers -> Floating point numbers

3 different types of floating point numbers
    - single floating point 
        * Has a size of 4 bytes (or 32 bits)
        * Has a precision of 7 numbers
    - double floating point 
        * has a size of 8 bytes (or 64 bits)
        * Has a precision of 15 numbers
    - long double floating point
        * has a size of 16 bytes (or 96 bits)
        * has a precision of >15 numbers after the comma

Precision is defined as the total numbers which are considered to be accurate
    e.g. 1.23456700001 with a 7 number precision can be considered accurate for the 1.234567 part
            - a single point is not sufficient to completely represent the number accurately
            - a double will completely represent it

floating points are not represented in the same way as integers in memory.
They use a specific memory format in the form of IEEE_754

Difference between integers and floating point numbers
    * Can be divided by 0 resulting in a + or - infinity depending on the sign of the floating point
    * 0 can be divided by 0 resulting in a NaN value (Not a Number)
    * Cannot be used in computation, i.e. adding infinity or NaN to an other number will not work
    * Can be compiled

Suffixes need to be included at the initialization step in order to specify a float or a long double
    * the number ending with f will be interpreted as a single floating point
    * the number ending with L will be interpreted as a long double floating point
*/

int main(){
    // Declare and initialize the variables
    float number1 {1.2345678901234567890f};
    double number2 {1.2345678901234567890};
    long double number3 {1.2345678901234567890L};

    // Print out the sizes
    std::cout << "sizeof float: " << sizeof(float) << std::endl;
    std::cout << "sizeof double: " << sizeof(double) << std::endl;
    std::cout << "sizeof long double: " << sizeof(long double) << std::endl;

    // Print out the variable contents
    std::cout << std::setprecision(20); // Control the precision of the cout stream
    std::cout << "Number 1: " << number1 << std::endl;
    std::cout << "Number 2: " << number2 << std::endl;
    std::cout << "Number 3: " << number3 << std::endl;

    // Print out the difference between the different numbers 
    std::cout << "The difference between the numbers 3 (most accurate) and 1 is: " << number3-number1 << std::endl;
    std::cout << "The difference between the numbers 3 (most accurate) and 2 is: " << number3-number2 << std::endl;

    // Precision gone wrong in the compiler
    //float number4 {192400023}; // A number that consists of 9 numbers which will not be able to be captured precisely
    /*
    error: narrowing conversion of '192400023' from 'int' to 'float' [-Wnarrowing]
       47 |     float number4 {192400023}; // A number that consists of 9 numbers which will not be able to be captured precisel
    This is due to braced initialization and can be circumvented with functional initialization or by declaring f as a suffix
    */
    float number4 {192400023.0f}; // Will be compiled but after 7 number the compiler will inject garbage into number
    float number5 (192400023); // Functional initialization
    double number6 (192400023); 
    std::cout << "Number 4: " << number4 << std::endl;
    std::cout << "Number 5: " << number5 << std::endl;
    std::cout << "Number 6: " << number6 << std::endl;
    std::cout << "Incrementing number 4 with 1: " << number4+1 << std::endl;
    std::cout << "Incrementing number 5 with 1: " << number5+1 << std::endl;
    // Incrementing the functional initialized value with 1 will reproduce the same number as the beginning
    std::cout << "The difference between number 4 and number 6: " << number6 - number4 << std::endl;
    std::cout << "The difference between number 4 and number 6: " << number6 - number5 << std::endl; 
    return 0;
}