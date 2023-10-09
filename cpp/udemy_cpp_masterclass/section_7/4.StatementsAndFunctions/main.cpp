#include <iostream>
/*
A statement is a basic unit of computation in  a C++ program
Every C++ program is a collection of statements organized in a certain way to achieve some goal
Statements end with a ; in C++

Order of executation of statements is from top to bottom
Executation keeps going until there is a statement causing the program to terminate, or run another sequence of statements 
*/

/*
Funtions are a sequence of statements that can be repeated with different input parameters

The general form of functions can be described as 

    returnType functionName(inputParameter1,...){
        ...
        functionbody - statements that need to be executed using the inputParameters
        ...
        ...
        return outputVariable; 
    }

Where the outputVariable is of the type returnType

Functions need to be defined before they can be called within the main function 
*/

int addNumbers(int first_number, int second_number){
    // The function addNumbers takes 2 inputs in the form of first_number and second_number and returns a int which is the sum of both input parameters
    return first_number + second_number;
}

int main(){
    //Three statements that are meant to initialize 3 different 
    int firstNumber = 12;
    int secondNumber = 9;
    int sum = firstNumber + secondNumber;
    int sumFunction = addNumbers(firstNumber, secondNumber);
    std::cout << "The first number is " << firstNumber << " and the second number is " << secondNumber << std::endl;
    std::cout << "The sum of the two numbers using the '+' operator is : " << sum << std::endl;
    std::cout << "The sum of the two numbers using the function addNumbers is : " << sumFunction << std::endl;
    return 0;
}