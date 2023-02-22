/*
Create a function that takes a string and returns the word count. The string will be a sentence.
Examples

countWords("Just an example here move along") ➞ 6

countWords("This is a test") ➞ 4

countWords("What an easy task, right") ➞ 5
*/

#include <iostream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

int countWords(string sentence){
    // Convert input sentence to an inputstream
    stringstream sentence_stream(sentence);

    // String vector to store the individual words
    vector<string> split_sentence;

    // Temporary variable to store individual words
    string temp;

    // Iterator to stream individual words to the vector variable
    // Individual words are seperated by a ' '
    while(getline(sentence_stream, temp, ' ')){
        split_sentence.push_back(temp);
    }
    return split_sentence.size();
}

int main(){
    cout << countWords("Just an example here move along") << "\n";
    cout << countWords("This is a test") << "\n";
    cout << countWords("What an easy task, right") << "\n";
}