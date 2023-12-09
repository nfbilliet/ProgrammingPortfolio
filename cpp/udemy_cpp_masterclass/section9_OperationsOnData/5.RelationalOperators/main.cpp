#include <iostream>
using namespace std;

/*
Relational operators

Operators used when comparing different objects to each other
    - less than, greater than
    - equivalent to or not equivalent to
These expression return a bool value, i.e. true or false

Why do we need to use brackets around our comparisson operators when printing to the terminal?
-> Precedence operator table in cpp
    -> '<<' or '>>' has a higher precedence than the relational operators
    -> It will try to execute these first before the relational operators
    -> '<< nmb_1 < nmb_2 <<' will be compiled as stream nmb_1 to the output followed by the comparisson of nmb_2 to something that is not there
*/
int main(){
    int nmb_1 {45};
    int nmb_2 {60};
    int nmb_3 {60};

    cout << boolalpha; // When return the bool value format it as true or false instead of 1 and 0

    cout << "Number 1 (45) is less than number 2 (60): " << (nmb_1 < nmb_2) << endl;
    cout << "Number 1 (45) is less than or equivalent to number 2 (60): " << (nmb_1<=nmb_2) << endl;
    cout << "Number 2 (60) is less than or equivalent to number 3 (60): " << (nmb_2<=nmb_3) << endl;
    cout << "Number 1 (45) is greater than number 2 (60): " << (nmb_1 > nmb_2) << endl;
    cout << "Number 1 (45) is greater than or equivalent to number 2 (60): " << (nmb_1>=nmb_2) << endl;
    cout << "Number 2 (60) is greater than or equivalent to number 3 (60): " << (nmb_2>=nmb_3) << endl;
    cout << "Number 1 (45) is equivalent to number 2 (60): " << (nmb_1==nmb_2) << endl;
    cout << "Number 2 (60) is equivalent to number 3 (60): " << (nmb_2==nmb_3) << endl;
    cout << "Number 1 (45) is not equivalent to number 2 (60): " << (nmb_1!=nmb_2) << endl;
    cout << "Number 2 (60) is not equivalent to number 3 (60): " << (nmb_2!=nmb_3) << endl;
    return 0;
}