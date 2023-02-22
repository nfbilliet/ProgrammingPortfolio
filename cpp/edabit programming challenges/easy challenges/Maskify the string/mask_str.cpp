/*
Usually when you sign up for an account to buy something, your credit card number, phone number
or answer to a secret question is partially obscured in some way. Since someone could look 
over your shoulder, you don't want that shown on your screen. Hence, the website masks these strings.

Your task is to create a function that takes a string, transforms all but the last four characters into "#" 
and returns the new masked string.

Examples

maskify("4556364607935616") ➞ "############5616"

maskify("64607935616") ➞ "#######5616"

maskify("1") ➞ "1"

maskify("") ➞ ""

Notes

    The maskify function must accept a string of any length.
    An empty string should return an empty string (fourth example above).
*/

#include <iostream>
#include <string>

using namespace std;

string maskify(string input_str){
    int string_size = input_str.size();
    if (string_size<=4){
        return input_str;
    }
    else {
        // Utilize the string constructor to initialize the masked string with the appropriate amount of '#'
        string masked_str = string(string_size-4, '#');
        // Extract the last four digits from a string, indexing starts at zero hence -5 and -1
        string remainder = input_str.substr(string_size-4, string_size-1);
        return masked_str+remainder;
    }
}

int main(){
    cout << maskify("4556364607935616") << "\n";

    cout << maskify("64607935616") << "\n";

    cout << maskify("1") << "\n";

    cout << maskify("") << "\n";
}

