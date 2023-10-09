#include <iostream>

/*
    3 different kinds of errors
    Compiler requires code to fulfill specific requirements in order to be compiled to an executable
        1) Compile time error
            -Something in the code prevents the compiler from creating the binary executable
        2) Runtime errors
            -Something goes wrong in the execution of the compiled code and produces a results that is not wanted
        3) Warnings
*/

int main(){
    //Compile Time error
    /*
    std::cout << "Hello World!" << std::endl
    Due to the lacking ; at the end of line 15
    error: expected ';' before 'return'
    */

    //Runtime error
    /*
    int value = 7/0; 
    std::cout << value << std::endl;
    Nothing will be printed to the terminal
    warning: division by zero [-Wdiv-by-zero]
    */
   
    return 0;
}