#include <iostream>
using namespace std;
/*
Basic Operations

5 standard operations that are defined as basic operations
    1) add (+)
    2) subtract (-)
    3) multiply (*)
    4) divide (/)
    5) modulus (%)
*/

int main(){
    int nmb_1 {10};
    int nmb_2 {3};
    float nmb_3 {3.0};
    int nmb_4 {5};

    int uni_nmb_sum {nmb_1 + nmb_2};
    int copy_nmb_sum = nmb_1 + nmb_2 + nmb_1;
    auto int_float_sum (nmb_1+nmb_3);
    cout << "Sum using  uniform initialization: " << uni_nmb_sum << endl;
    cout << "Sum using copy initialization: " << copy_nmb_sum << endl;
    cout << "Sum of int and float: " << int_float_sum << endl;

    cout << "---------------"<<endl;

    int uni_nmb_diff {nmb_1 - nmb_2};
    int copy_nmb_diff = nmb_1 - nmb_2 - nmb_1;
    auto int_float_diff (nmb_1-nmb_3);
    cout << "Difference using  uniform initialization: " << uni_nmb_diff << endl;
    cout << "Difference using copy initialization: " << copy_nmb_diff << endl;
    cout << "Difference of int and float: " << int_float_diff << endl;

    cout << "---------------"<<endl;

    int uni_nmb_mul {nmb_1 * nmb_2};
    int copy_nmb_mul = nmb_1 * nmb_2 * nmb_1;
    auto int_float_mul (nmb_1*nmb_3);
    cout << "Multiplication using  uniform initialization: " << uni_nmb_mul << endl;
    cout << "Multiplication using copy initialization: " << copy_nmb_mul << endl;
    cout << "Multiplication of int and float: " << int_float_mul << endl;
 
    cout << "---------------"<<endl;
 
    int uni_nmb_div {nmb_1 / nmb_2};
    int copy_nmb_div = nmb_1 / nmb_2 / nmb_1;
    auto int_float_div (nmb_1/nmb_3);
    auto float_int_div (nmb_3/nmb_1);
    int remain_div {nmb_4/nmb_2}; // Will return how many times we can fit the denominator into the numerator
    cout << "Division using  uniform initialization: " << uni_nmb_div << endl;
    cout << "Division using copy initialization: " << copy_nmb_div << endl;
    cout << "Division of int and float: " << int_float_div << endl;
    cout << "Division of float and int: " << float_int_div << endl;
    cout << "Division with remainder: " << remain_div << endl;
    cout << "---------------"<<endl;
 
    int uni_nmb_mod {nmb_1 % nmb_2};
    int copy_nmb_mod = nmb_2 % nmb_2;
    //auto int_float_mod (nmb_1%nmb_3); Results in a comppile error
    cout << "Modulo using  uniform initialization: " << uni_nmb_mod << endl;
    cout << "Modulo using copy initialization: " << copy_nmb_mod << endl;
    return 0;
}