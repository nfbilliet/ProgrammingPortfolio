#include <iostream>
using namespace std;
/*
Precedence and associativity

Precedence = Which operation do we apply first?
Associativity = Which direction do we apply operations?

The set of rules to follow when we combine a set of different operations with each other
    - multiplication and division get precedence over addition and substraction
    - What happens when we get an expression that consists of operations that all get the same precedence?
        e.g. an expression that consists of additions and subtractions?
        -> Associativity 
            - Can differ depending on the operations that are applied in C++
    - C++ Operator Precedence Table (https://en.cppreference.com/w/cpp/language/operator_precedence)
        -> Orders all different operations according to precendence and mentions the associativity rules that they follow
            * multiplication, division, remainder > subtraction, addition in precedence and follow left-to-right associativity
*/
int main(){
    int a {6};
    int b {3};
    int c {8};
    int d {9};
    int e {3};
    int f {2};
    int g {5};

    /*
    * and / get precedence 
        - (b*c)=24 and (d/e)=3
        - addition and subtraction have same precedence and follow left to right
         -> ((((6 + 24) - 3) - 2) +5) 
         -> 30 - 3 = 27
         -> 27 - 2 = 25
         -> 25 + 5 = 30
    */
    int result = a + b * c - d / e - f + g;
    cout << result << endl;

    /*
    1) a/b*c gets precedence
        -> left to right associativity
        -> a/b = 6/3 = 2
        -> (a/b)*c = 2*8 = 16
    2) left to right associativity for addition and subtraction
        -> [(a/b)*c] + d = 16 + 9 = 25
        -> -e = 25 - 3 = 22
        -> +f = 22 + 2 = 24 
    */
    result = a / b * c + d - e + f; 
    cout << result << endl;
    return 0;
}