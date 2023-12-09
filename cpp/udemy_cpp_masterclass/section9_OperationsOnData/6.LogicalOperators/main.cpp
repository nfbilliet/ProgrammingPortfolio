#include <iostream>
using namespace std;
/*
Logical operators
    - AND &&
    - OR ||
    - NOT !

Work on boolean expressions 
    - AND -> both expressions need to be TRUE in order to evaluate to TRUE
        TRUE && TRUE = TRUE
    - OR -> one of the expressions needs to evaluate to TRUE in order to evaluate to TRUE
        TRUE || FALSE = TRUE
        FALSE || TRUE = TRUE
        TRUE || TRUE = TRUE
    - NOT -> invert the bool value to the opposite
        !FALSE = TRUE
        !TRUE = FALSE
*/
int main(){
    bool a {true};
    bool b {false};
    bool c {true};
    int d{4};
    int e{6};
    int f{10};

    cout << boolalpha;
    cout << "The following boolean variables are defined" << endl;
    cout << "a = " << a << endl;
    cout << "b = " << b << endl;
    cout << "c = " << c << endl;
    cout << "-----AND logical table-----" << endl;
    cout << "a && a = " << (a&&a) << endl;
    cout << "a && b = " << (a&&b) << endl;
    cout << "a && c = " << (a&&c) << endl;
    cout << "a && b && c = " << (a&&b&&c) << endl;
    cout << "-----OR logical table-----" << endl;
    cout << "a || a = " << (a||a) << endl;
    cout << "a || b = " << (a||b) << endl;
    cout << "b || b = " << (b||b) << endl;
    cout << "a || c = " << (a||c) << endl;
    cout << "a || b || c = " << (a||b||c) << endl;
    cout << "-----NOT logical table-----" << endl;
    cout << "!a = " << (!a) << endl;
    cout << "!b = " << (!b) << endl;
    cout << "!c = " << (!c) << endl;
    cout << "-----Combing different logical expression together-----" << endl;
    cout << "!(a&&b) = " << (!(a&&b)) << endl;
    cout << "!(a && b) || c = " << (!(a&&b)||c) << endl;
    cout << "(a && b) || (a && c) = " << ((a&&b)||(a&&c)) << endl;
    cout << "-----Combining logical operators with relational operators-----" << endl;
    cout << "d : " << d << endl;
    cout << "e : " << e << endl;
    cout << "f : " << f << endl;
    cout << "(d<e) && (d<f) = " << ((d<e)&&(d<f)) << endl;
    cout << "(d>e) && (d<f) = " << ((d>e)&&(d<f)) << endl;
    cout << "(d>e) || (d<f) = " << ((d<e)||(d<f)) << endl;
    cout << "!a && (d>=e) = " << (!a && (d>=e)) << endl;
    return 0;
}