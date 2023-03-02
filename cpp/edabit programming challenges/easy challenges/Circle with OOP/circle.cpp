#include "circle.hpp"
#include <cmath>
#include <iostream>

// Defining the constructor for the Circle object
Circle::Circle(float input_radius){
    radius = input_radius;
}

float Circle::getRadius(){
    return radius;
}

float Circle::getPerimeter(){
    return 2*M_PI*radius;
}

float Circle::getArea(){
    return M_PI*pow(radius, 2);
}