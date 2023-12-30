#include <iostream>

/*
Numeric limits

Controlled by the standard library <limits>
    - numeric_limits<T>::min()
        Represents the smallest possible value for the float data type , i.e. the closest to 0
        Represents the largest possible negative value for the integer data type
    - numeric_limits<T>::max()
        Represents the largest possible value for the given data type T, i.e. the largest positive number
    - numeric_limits<T>::lowest()
        Represents the largest possible negative value for the given data type T, i.e. the largest negative number

<T> denotes a template data type which can be filled in with any of the existing data types present in cpp
    e.g. numeric_limits<int>::min() works specific on integer type

https://en.cppreference.com/w/cpp/types/numeric_limits
*/
#include <limits>
#include <iomanip>
#include <ios>

using namespace std;
int main(){
    cout << "========================================================================" << endl;
    cout << "The min limit for the short data type is " << numeric_limits<short>::min() << endl;
    cout << "The max limit for the short data type is " << numeric_limits<short>::max() << endl;
    cout << "The lowest limit for the short data type is " << numeric_limits<short>::lowest() << endl;

    cout << "========================================================================" << endl;
    cout << "The min limit for the unsigned short data type is " << numeric_limits<unsigned short>::min() << endl;
    cout << "The max limit for the unsigned short data type is " << numeric_limits<unsigned short>::max() << endl;
    cout << "The lowest limit for the unsigned short data type is " << numeric_limits<unsigned short>::lowest() << endl;

    cout << "========================================================================" << endl;
    cout << "The min limit for the long data type is " << numeric_limits<long>::min() << endl;
    cout << "The max limit for the long data type is " << numeric_limits<long>::max() << endl;
    cout << "The lowest limit for the long data type is " << numeric_limits<long>::lowest() << endl;

    cout << "========================================================================" << endl;
    cout << "The min limit for the unsigned long data type is " << numeric_limits<unsigned long>::min() << endl;
    cout << "The max limit for the unsigned long data type is " << numeric_limits<unsigned long>::max() << endl;
    cout << "The lowest limit for the unsigned long data type is " << numeric_limits<unsigned long>::lowest() << endl;

    cout << "========================================================================" << endl;
    cout << "The min limit for the long long data type is " << numeric_limits<long long>::min() << endl;
    cout << "The max limit for the long long data type is " << numeric_limits<long long>::max() << endl;
    cout << "The lowest limit for the long long data type is " << numeric_limits<long long>::lowest() << endl;

    cout << "========================================================================" << endl;
    cout << "The min limit for the unsigned long long data type is " << numeric_limits<unsigned int>::min() << endl;
    cout << "The max limit for the unsigned long long data type is " << numeric_limits<unsigned int>::max() << endl;
    cout << "The lowest limit for the unsigned long long data type is " << numeric_limits<unsigned int>::lowest() << endl;

    cout << "========================================================================" << endl;
    cout << "The min limit for the int data type is " << numeric_limits<int>::min() << endl;
    cout << "The max limit for the int data type is " << numeric_limits<int>::max() << endl;
    cout << "The lowest limit for the int data type is " << numeric_limits<int>::lowest() << endl;

    cout << "========================================================================" << endl;
    cout << "The min limit for the unsigned int data type is " << numeric_limits<unsigned int>::min() << endl;
    cout << "The max limit for the unsigned int data type is " << numeric_limits<unsigned int>::max() << endl;
    cout << "The lowest limit for the unsigned int data type is " << numeric_limits<unsigned int>::lowest() << endl;

    cout << "========================================================================" << endl;
    cout << "The min limit for the long int data type is " << numeric_limits<long int>::min() << endl;
    cout << "The max limit for the long int data type is " << numeric_limits<long int>::max() << endl;
    cout << "The lowest limit for the long int data type is " << numeric_limits<long int>::lowest() << endl;

    cout << "========================================================================" << endl;
    cout << "The min limit for the float data type is " << numeric_limits<float>::min() << endl;
    cout << "The max limit for the float data type is " << numeric_limits<float>::max() << endl;
    cout << "The lowest limit for the float data type is " << numeric_limits<float>::lowest() << endl;

    cout << "========================================================================" << endl;
    cout << "The min limit for the double data type is " << numeric_limits<double>::min() << endl;
    cout << "The max limit for the double data type is " << numeric_limits<double>::max() << endl;
    cout << "The lowest limit for the double data type is " << numeric_limits<double>::lowest() << endl;

    cout << "========================================================================" << endl;
    cout << "The min limit for the long double data type is " << numeric_limits<long double>::min() << endl;
    cout << "The max limit for the long double data type is " << numeric_limits<long double>::max() << endl;
    cout << "The lowest limit for the long double data type is " << numeric_limits<long double>::lowest() << endl;
    return 0;
}