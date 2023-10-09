#include <iostream>
using namespace std;

int main(){
    // Exercise at the end of the lecture
    //Make a program that prints out your name 10 times

    // Method 1: The sloppy way - repeat line 10 times
    cout << "Method 1 - The Sloppy way" << endl;
    cout << "Niels" << endl;
    cout << "Niels" << endl;
    cout << "Niels" << endl;
    cout << "Niels" << endl;
    cout << "Niels" << endl;
    cout << "Niels" << endl;
    cout << "Niels" << endl;
    cout << "Niels" << endl;
    cout << "Niels" << endl;
    cout << "Niels" << endl;

    //Method 2: for loop 
    cout << "Method 2 - For loop" << endl;
    //Initialise counter variable at 0 and add increments of 1 while counter is less then 10
    for(int counter=0; counter<10; counter++){
        cout << "Niels" << endl;
    }

    //Return 0 at the end of the main funtion is used to verify if the executable gets to the end of the main function
    return 0;
}