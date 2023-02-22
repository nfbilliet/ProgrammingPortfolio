/*
Create a function that takes an array of numbers and returns a new array, sorted in ascending order (smallest to biggest).

    Sort numbers array in ascending order.
    If the function's argument is null, an empty array, or undefined; return an empty array.
    Return a new array of sorted numbers.

Examples

sortNumsAscending([1, 2, 10, 50, 5]) ➞ [1, 2, 5, 10, 50]

sortNumsAscending([80, 29, 4, -95, -24, 85]) ➞ [-95, -24, 4, 29, 80, 85]

sortNumsAscending([]) ➞ []

Notes

Test input can be positive or negative.
*/

#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

// Pass a reference to an array of unspecificied size to the function (more efficient)
// The function is classified as void as we change the array itself and will not return anything
template <typename T>

// Use the general template T in order to print any vector
void printVec(vector<T> &vec){
    for (int i=0; i<vec.size(); i++){
        cout << vec[i] << " ";
    }
    cout << "\n";
}

void sortNumsAscending(vector<int> &integer_array){
    sort(integer_array.begin(), integer_array.end());
}

int main(){
    vector<int> test_array_1 = {1, 2, 10, 50, 5};
    vector<int> test_array_2 = {80, 29, 4, -95, -24, 85};
    vector<int> test_array_3 = {};
    
    printVec(test_array_1);
    sortNumsAscending(test_array_1);
    printVec(test_array_1);

    printVec(test_array_2);
    sortNumsAscending(test_array_2);
    printVec(test_array_2);
    
    printVec(test_array_3);
    sortNumsAscending(test_array_3);
    printVec(test_array_3);   
}