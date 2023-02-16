/*
=Task=

Create a function that counts the number of syllables a word has. 
Each syllable is separated with a dash -
*/

#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

int main(){
    // Create input stream to obtain word that needs to be parsed
    cout << "Please enter a word that has been parsed by '-' after every syllable\n";
    string word;
    cin >> word;

    // Create a word stream from the input word
    stringstream word_stream(word);

    // Create temporary variable where the syllable segments can be stored
    string syllable;

    // Create storage vector to store the string that has been split up in different parts
    vector<string> split_string;

    // Iterator over the word_stream and split it over the '-' character, store the segment in the syllable variable
    while (getline(word_stream, syllable, '-'))
    {
        split_string.push_back(syllable);
    }

    /* Verify if the code above properly parses the input word
    for (int i=0; i<split_string.size(); i++){
        cout << split_string[i] << "\n";
    }
    */
    
    cout << "The word has " << split_string.size() << "number of syllables.";
    
    /*
    "on-o-mat-o-poe-ia" should have 6 syllables
    */
}