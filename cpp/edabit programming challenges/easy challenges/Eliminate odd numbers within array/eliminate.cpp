/*
Create a function that takes an array of numbers and returns only the even values.
Examples

noOdds([1, 2, 3, 4, 5, 6, 7, 8]) ➞ [2, 4, 6, 8]

noOdds([43, 65, 23, 89, 53, 9, 6]) ➞ [6]

noOdds([718, 991, 449, 644, 380, 440]) ➞ [718, 644, 380, 440]

Notes

    Return all even numbers in the order they were given.
    All test cases contain valid numbers ranging from 1 to 3000.
*/

#include <iostream>
#include <vector>
#include <string>

using namespace std;

vector<int> noOdds(vector<int> int_arr){
    vector<int> withoutOdds;
    for (int i=0; i<int_arr.size(); i++){
        if ((int_arr[i]%2)==0){
            withoutOdds.push_back(int_arr[i]);
        }
    }
    return withoutOdds;
}

void printVector(vector<int> int_arr){
    string stringified_vec;
    stringified_vec+="[";
    for (int i=0; i<int_arr.size(); i++){
        if (i<int_arr.size()-1){
            stringified_vec+= to_string(int_arr[i]);
            stringified_vec+= ",";
        }
        else {
            stringified_vec+=to_string(int_arr[i]);
            stringified_vec+="]";
        }
    }
    cout << stringified_vec << "\n";
}

int main(){
    printVector(noOdds({1, 2, 3, 4, 5, 6, 7, 8}));
    printVector(noOdds({43, 65, 23, 89, 53, 9, 6})); 
    printVector(noOdds({718, 991, 449, 644, 380, 440}));
}