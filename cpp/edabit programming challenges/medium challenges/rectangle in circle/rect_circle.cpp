/*
Create a function that takes three numbers — the width and height of a rectangle, and the radius of a circle — and returns true if the rectangle can fit inside the circle, false if it can't.
Examples

rectangleInCircle(8, 6, 5) ➞ true

rectangleInCircle(5, 9, 5) ➞ false

rectangleInCircle(4, 7, 4) ➞ false
*/

/*
A rectangle fits into a circle if the points that are the furthest away from the shared center point
(in this case the origin) is less than or equal to the radius of the circle.

For a given rectangle that shares the same origin as the circle the corner points of the rectangle are 
the furthest away from the origin.

To compute the distance of the corner to the origin we can use the pythagorean theorem.
The line that spans the distance from the origin to the corner is the hypotenuse of the right triangle that can
be constructed with the bisector for either sides of the rectangle.

sqrt[(h/2)**2 + (w/2)**2] <= r
*/

#include <iostream>
#include <cmath>

using namespace std;

bool rectangleInCircle(float h, float w, float r){
    float corner_dist = sqrt(pow((h/2),2) + pow((w/2),2));
    if (corner_dist<=r){
        return true;
    }
    else {
        return false;
    }
}

int main(){
    cout << rectangleInCircle(8, 6, 5) << "\n";

    cout << rectangleInCircle(5, 9, 5) << "\n";

    cout << rectangleInCircle(4, 7, 4) << "\n";
}