/*
=Task=
Create a function which validates whether a 
bridge is safe to walk on (i.e. has no gaps in it to fall through).

EXAMPLES

isSafeBridge("####") ➞ true

isSafeBridge("## ####") ➞ false

isSafeBridge("#") ➞ true
*/

#include <iostream>
#include <string>

using namespace std;

bool isSafeBridge(string bridge_str){
    bool isSafe = true;
    for (int i=0; i<bridge_str.size(); i++){
       // Check for as long the string has a 'non-empty' character, i.e. whitespace
       if (bridge_str[i]==' '){
        isSafe = false;
        break;
       } 
    }
    return isSafe;
}

int main(){
    cout << isSafeBridge("####") << "\n";
    cout << isSafeBridge("## ####") << "\n";
    cout << isSafeBridge("#") << "\n";
}