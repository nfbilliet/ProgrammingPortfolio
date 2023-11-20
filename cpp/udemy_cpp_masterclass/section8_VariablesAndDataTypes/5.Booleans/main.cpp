#include <iostream>

/*
Booleans

Variable type that can store up to 2 different values
    * True or 1
    * False or 0

Represented with the prefix 'bool'

 Printing the value of the boolean variable will output the integer representation of the boolean
 -> Can be changed in the outputstream by including the 'std::cout << std::boolalpha;' statement in the program

A boolean is stored in memory using 8 bits or 1 byte of data
    * 1 byte is too large to store a data type that can only take up too 2 different values
        -> 1 byte = 8 bits => 2^8 different values = 256 different values
    * There are techniques to store more data into a byte which can be necessary when working on embedded devices
*/

int main(){
    bool green_light {true};
    bool red_light {false};

    std::cout << "The green_light variable contains the true boolean value represented with: " << green_light << std::endl;
    std::cout << "The red_light variable contains the false boolean value represented with: " << red_light << std::endl;

    // Changing output format of the boolean data type
    std::cout << std::boolalpha;
    std::cout << "boolalpha option enabled for the output stream of the program" << std::endl;
    std::cout << "The green_light variable contains the true boolean value represented with: " << green_light << std::endl;
    std::cout << "The red_light variable contains the false boolean value represented with: " << red_light << std::endl;

    // Verifying the size of the bool data type
    std::cout << "The size of boolean in memory is: " << sizeof(bool) << std::endl;
    return 0;
}