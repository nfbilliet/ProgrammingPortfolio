#include <iostream>
/*
---Celsius to Fahrenheit conversion---

Write a C++ program that reads in Celsius degree data from the terminal with std::cin and stores that in a double variable. 
The program then converts that to Fahrenheit and prints out a message like 50.2 Celsius is 122.36 Fahrenheit . 
The formula to convert from Celsius to Fahrenheit is fahrenheit = (9.0 / 5) * celsius + 32 .

Please note that we are doing (9.0 / 5)  and not (9/ 5) . (9 / 5) would do integer division and we would loose fractional
 data that we need for the conversion to work properly. 
--------------------------------------

---Area and Volume of a Box---
Write a program that reads in the length and width and height of a box and 
computes the base area and volume using the following formulas
------------------------------
*/
using namespace std;

int main(){
    //C to F conversion
    double degreeCelsius {};
    cout << "Enter the temperature in C that you wish to convert into Fahrenheit: ";
    cin >> degreeCelsius; 
    auto degreeFahrenheit = (9.0/5)*degreeCelsius + 32;
    cout << degreeCelsius << " C = " << degreeFahrenheit << " F" << endl;

    //Area and Volume of a Box
    double length {};
    double width {};
    double height {};

    cout << "Please enter the values (m) for the length, width and height of the box of which you wish to know the base area and volume" << endl;
    cout << "Length : ";
    cin >> length;
    cout << "Width : ";
    cin >> width;
    cout << "Height : ";
    cin >> height;

    double area = length*width;
    double volume = area*height;

    cout << "The base area of the box is " << area << " square meter" << endl;
    cout << "The volume of the box is " << volume << " cubed meter" << endl; 
    return 0;
}