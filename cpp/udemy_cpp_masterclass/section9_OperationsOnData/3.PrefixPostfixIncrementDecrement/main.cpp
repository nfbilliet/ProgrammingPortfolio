#include <iostream>
using namespace std;
/*
Prefix and suffix addition and subtraction

What is the difference between prefix and suffix incrementation/decrementation

    ++value -> addition of one preceeds the return of the value
    value++ -> return of the value preceeds the addition of one

If both result in the same value in the end what is the difference between these 2 expressions?
-> Their is a difference in operator precedence between these two
    -> suffix incrementation/decrementation has a higher precedence than prefix incrementation/decrementation
*/

int main(){
    int value {5};
    cout << "The initial value is " << value << endl;
    value = value + 1; 
    cout << "The value after incrementing (copy assignment) is " << value << endl;
    value = 5;
    value++; // Suffix increment with 1
    cout << "The value after incrementing (suffix style) " << value << endl;
    value = 5;
    ++value; // Prefix increment with 1
    cout << "The value after incrementing (prefix style) " << value << endl;
    
    value = 5;
    value = value - 1;
    cout << "The value after decrementing (copy assignment) is " << value << endl;
    value = 5;
    value--; // Suffix decrement with one
    cout << "The value after decrementing (suffix style) is " << value << endl;
    value = 5;
    --value; // Prefix decrement with one
    cout << "The value after decrementing (prefix style) is " << value << endl;
    return 0;
}