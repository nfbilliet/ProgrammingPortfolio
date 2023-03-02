/*
Your task is to create a Circle constructor that creates a circle with a radius provided by an argument. The circles constructed must have two getters getArea() (PI *r^2) and getPerimeter() (2*PI*r) which give both respective areas and perimeter (circumference).

For help with this class, I have provided you with a Rectangle constructor which you can use as a base example.
Examples

Circle circy(11);
circy.getArea();

// Should return 379.94

Circle circy(4.44);
circy.getPerimeter();

// Should return 27.8832
*/

#include <iostream>
#include "circle.hpp"

using namespace std;

int main(){
    Circle circy(11);
    cout << "The radius is " << circy.getRadius() << "\n";
    cout << "The perimeter is " << circy.getPerimeter() << "\n";
    cout << "The area is " << circy.getArea() << "\n";
}
