/*
=Task=

Take an array of integers (positive or negative or both) 
and return the sum of the absolute value of each element.

*/

#include <iostream>
#include <sstream>
#include <vector>

using namespace std;

int main(){
    // create uninitialized array that takes integers 
    vector<int> int_arr;
    cout << "Please enter a sequence of numbers (positive or negative) of which you wish to calculate the absolute sum of.\n";

    string input_line;
    // Extract the characters from the input stream
    getline(cin, input_line);

    // Use stringstream to iterate over the input line
    stringstream input_stream(input_line);

    // Create a temporary variable that can be used to store the different numbers when iterating over the string
    int temp;

    // While the entries come from the stream store them into the temp variable and add them to the int_arr
    while (input_stream >> temp){
        int_arr.push_back(temp);
    }

    /* Verify with a test input if the code properly reads in positive and negative integers
    for (int i=0; i<int_arr.size(); i++){
        cout << int_arr[i] << "\n";
    }
    */

    int abs_sum = 0;

    for (int i=0; i<int_arr.size(); i++){
        abs_sum += abs(int_arr[i]);
    }

    cout << "The absolute sum of the integers is " << abs_sum;
}