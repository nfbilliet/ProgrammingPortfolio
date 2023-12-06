#include <iostream>

/*
Characters
    - Data type to represent distinct string characters such as letters, symbols or numbers
    - use of single quotation to denote char nature i.e. ''
    - occupies 1 byte(8bits) in memory, has 2^8 or 256 different possible entries
        - ASCII table
    - Letters can also be represented through their ASCII code
    e.g. char letter_a {'a'}; stores the character a in the letter_a var
*/

int main(){
    char letter_a {'a'};
    char letter_r {'r'};
    char letter_o {'o'};
    char letter_w {'w'};

    std::cout << "Using the quotation style definition of the variables" << std::endl;
    std::cout << letter_a << std::endl;
    std::cout << "The decimal representation of the letter 'a' is " << int(letter_a) << std::endl;
    std::cout << "The letter a occupies " << sizeof(letter_a) << " bytes in memory" << std::endl;
    std::cout << letter_r << std::endl;
    std::cout << "The integer representation of the letter 'r' is " << int(letter_r) << std::endl;
    std::cout << "The letter r occupies " << sizeof(letter_r) << " bytes in memory" << std::endl;
    std::cout << letter_o << std::endl;
    std::cout << "The integer representation of the letter 'o' is " << int(letter_o) << std::endl;
    std::cout << "The letter o occupies " << sizeof(letter_o) << " bytes in memory" << std::endl;
    std::cout << letter_w << std::endl;
    std::cout << "The integer representation of the letter 'w' is " << int(letter_w) << std::endl;
    std::cout << "The letter w occupies " << sizeof(letter_w) << " bytes in memory" << std::endl;

    char dec_a {97};
    char dec_r {114};
    char dec_o {111};
    char dec_w {119};

    std::cout << "Using decimal representation of 'a', 'r', 'o' and 'w' " << std::endl;
    std::cout << dec_a << std::endl;
    // static_cast<type> -> Converts between types using a combination of implicit and user-defined conversions.
    std::cout << "The value of the character extracted with static_cast<int>(dec_a) is " << static_cast<int>(dec_a) << std::endl;
    std::cout << dec_r << std::endl;
    std::cout << "The value of the character extracted with static_cast<int>(dec_r) is " << static_cast<int>(dec_r) << std::endl;
    std::cout << dec_o << std::endl;
    std::cout << "The value of the character extracted with static_cast<int>(dec_o) is " << static_cast<int>(dec_o) << std::endl;
    std::cout << dec_w << std::endl;
    std::cout << "The value of the character extracted with static_cast<int>(dec_w) is " << static_cast<int>(dec_w) << std::endl;
    return 0;
}