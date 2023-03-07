/*
Quadratic Equation

Create a function to find only the root value of x in any quadratic equation ax^2 + bx + c. The function will take three arguments:

    a as the coefficient of x^2
    b as the coefficient of x
    c as the constant term

Examples

quadraticEquation(1, 2, -3) ➞ 1

quadraticEquation(2, -7, 3) ➞ 3

quadraticEquation(1, -12, -28) ➞ 14
*/

#include <iostream>
#include <cmath>
#include <vector>
#include <complex>
using namespace std;

vector<float> quadraticEquation(float a, float b, float c){
    float discriminant = pow(b, 2) - 4*a*c;
    if (discriminant>0){
        vector<float> roots = {(-b+sqrt(discriminant))/(2*a), (-b-sqrt(discriminant))/(2*a)};
        return roots;
    }
    /*
    This will result in a type error with the predefined function output

    else if (discriminant<0){
        vector<complex<float> roots = {complex<float>(-b/(2*a), sqrt(-discriminant)/(2*a)),
                                       complex<float>(-b/(2*a), -sqrt(-discriminant)/(2*a))};
        return roots;
    }
    */
    else {
        vector<float> root = {-b/(2*a)};
        return root;
    }
}

int main(){
    vector<float> solutions_1 = quadraticEquation(1, 2, -3);
    vector<float> solutions_2 = quadraticEquation(2, -7, 3);
    vector<float> solutions_3 = quadraticEquation(1, -12, -28);
    cout << "The solutions are vectors of size: " << solutions_1.size() << ", " << solutions_2.size() << ", " << solutions_3.size() <<"\n";
    cout << "The solutions of the first equation are: " << solutions_1[0] << ", " << solutions_1[1] << "\n";
    cout << "The solutions of the second equation are: " << solutions_2[0] << ", " << solutions_2[1] << "\n";
    cout << "The solutions of the third equation are: " << solutions_3[0] << ", " << solutions_3[1] << "\n";
}