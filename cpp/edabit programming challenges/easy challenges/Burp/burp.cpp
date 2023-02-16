/*
=Task=
Create a function that returns the string "Burp" with the amount of "r's" determined 
by the input parameters of the function.

EXAMPLES

longBurp(3) ➞ "Burrrp"

longBurp(5) ➞ "Burrrrrp"

longBurp(9) ➞ "Burrrrrrrrrp"
*/

#include <iostream>
#include <string>

using namespace std;

string longBurp(int nmb_r){
    string burp = "Bu";
    for (int i=0; i<nmb_r; i++){
        burp += "r";
    }
    burp += "p";
    return burp;
}

int main(){
    int input_int;
    cout << "How many r's do you want?\n";
    cin >> input_int;
    cout << longBurp(input_int);
}