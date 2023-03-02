#include <iostream>
#include <math.h>

class Circle{
    private:
        float radius;

    public:
        // Class constructor
        Circle(float radius);
        float getRadius();
        float getArea();
        float getPerimeter();
};