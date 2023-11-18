#include <iostream>

/*
====Integer modifiers====

How can we change the behavior of our integer variables?

1) Positieve versus negative integers 

        int value1 {10};
        int value2 {-300};
   
   These assignments work automatically and will not result in any compilation error
   However we can explicitly state that the integers we use in the initialization of the variable will be possible signed, i.e. positive or negative using the 'signed' prefix

        signed int value1 {10};
        signed int value2 {-300};

    The inverse is also possible. If we are sure that the integers will be positive only, i.e. we know that the sign will always be positive we can use the 'unsigned' prefix

        unsigned int value1 {10};
        unsigned int value2 {-300}; => Will result in a compilation error due to the negative sign in front of the 300

    Why would we differentiate between the signed and unsigned integers?
        * Using the formula from the number system we know that in general n bits can encode into 2^n different numbers
        * When we declare integers without the prefix signed or unsigned we need to take the possibility that our number can be both negative or positive 
          The range of possible value will then be halved because we need to take the negative possibilities into account as well

            unsigned range => [0 , (2^n - 1)]
            signed range => [-2^(n-1)) , 2^(n-1)-1]

2) Short versus long integers

    The prefix short and long differentiate between integers that take up
        * 2 bytes of memory for the 'short' prefix
        * 4 or 8 bytes of memory for the 'long' prefix
        * 8 bytes of memory for the 'long long' prefix

    Combining these prefixes with the signed and unsigned prefixes allows of to manipulate the range of possible values even more
        * short signed int => [-2^(15), 2^(15)-1] => [-32768 , 32767]
        * short unsigned => [0, 2^(16)-1] => [0 , 65535]
        * long signed int => [-2^(31), 2^(31)-1] => [-2 147 483 648 , 2 147 483 647]
        * long unsigned => [0, 2^(32)-1] => [0 , 4 294 967 295]
        * long long signed int => [-2^(63), 2^(63)-1] => [-9 223 372 036 854 775 808 , 9 223 372 036 854 775 807]
        * long long unsigned => [0, 2^(64)-1] => [0 , 18 446 744 073 709 551 615]
    
    Only works for decimal numbers not fractional numbers
*/

int main(){
    int val1 {10};
    int val2 {-300};

    std::cout << "Value 1 : " << val1 << std::endl;
    std::cout << "Size of value 1 : " << sizeof(val1) << std::endl;
    std::cout << "Value 2 : " << val2 << std::endl;
    std::cout << "Size of value 2 : " << sizeof(val2) << std::endl;

    unsigned int val3 {10};
    // unsigned int val4 {-300}; Compile error negative number in unsigned int variable

    std::cout << "Unsigned Value 3 : " << val3 << std::endl;
    std::cout << "Size of unsigned value 3 : " << sizeof(val3) << std::endl;


    signed int val5 {10};
    signed int val6 {-300};

    std::cout << "Signed Value 5 : " << val5 << std::endl;
    std::cout << "Size of signed value 5 : " << sizeof(val5) << std::endl;
    std::cout << "Signed Value 6 : " << val6 << std::endl;
    std::cout << "Size of signed value 6 : " << sizeof(val6) << std::endl;

    short int val7 {10};
    short int val8 {-300};

    std::cout << "Short Value 7 : " << val7 << std::endl;
    std::cout << "Size of short value 7 : " << sizeof(val7) << std::endl;
    std::cout << "Short Value 8 : " << val8 << std::endl;
    std::cout << "Size of short value 8 : " << sizeof(val8) << std::endl;
    
    long int val9 {10};
    long int val10 {-300};

    std::cout << "Long Value 9 : " << val9 << std::endl;
    std::cout << "Size of long value 9 : " << sizeof(val9) << std::endl;
    std::cout << "Long Value 10 : " << val10 << std::endl;
    std::cout << "Size of long value 10 : " << sizeof(val10) << std::endl;

    long long int val11 {10};
    long long int val12 {-300};

    std::cout << "Long long Value 11 : " << val11 << std::endl;
    std::cout << "Size of long long value 11 : " << sizeof(val11) << std::endl;
    std::cout << "Long long Value 12 : " << val12 << std::endl;
    std::cout << "Size of long long value 12 : " << sizeof(val12) << std::endl;

    return 0;
}