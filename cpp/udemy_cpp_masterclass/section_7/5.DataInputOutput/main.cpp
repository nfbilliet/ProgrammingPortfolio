#include <iostream>
#include <string>

/*
Data output using the different std functions
    1) std::cout -> Stream out data from the program to the terminal
    2) std::cin -> Stream data in from the terminal to the program
    3) std::cerr -> Stream out error logs from the program to the terminal
    4) std::clog -> Stream out log messages from the program to the terminal

When using these input and output stream we use the i(nput)o(utput)stream library
These functions work using the '<<' and '>>' operators
'std::cout <<' where the '<<' operator refers to the direction of the datastream, i.e. everything after it gets streamed outward to the terminal
'std::cin >>' where the '>>' operator refers to the direction of the datastream from the terminal to the program 
*/

int main(){
    /*
    //Printing data from the program to tne terminal
    std::cout << "This text goes to the terminal" << std::endl;

    //Variables can be printed to the terminal
    int age = 30;
    std::cout << "The value stored in the variable 'age' is " << age << std::endl;

    //Error message printing
    std::cerr << "This is a error message" << std::endl;

    //Log message printing 
    std::clog << "This is a log message" << std::endl;

    //Obtaining data from the terminal 
    // In order to stream data from the terminal to the program we need to declare uninitialized variables that can receive data
    std::string name; //Unitiliazed string variable is a empty string equivalent to ''
    int age2; //Uninitialized int variabel is a 0
    std::cout << "The variable 'name'  contains the following value : " << name << std::endl;
    std::cout << "The variable 'age2' contains the following value: " << age2 << std::endl;

    std::cout << "Please enter the name and age separated by a space : " << std::endl;
    std::cin >> name >> age2; // equivalent to two consecutive cin statements
    std::cin.clear();

    std::cout << "After the cin statements the 'name' variable contains the following value : " << name << std::endl;
    std::cout << "After the cin statements the 'age2' variable contains the following value : " << age2 << std::endl;

    //In order to grab data that is separated by spaces we need to utilize the getline function 
    std::string full_name;
    int age3;

    std::cout << "Enter your full name and age separated by a space : " << std::endl;
    std::cin >> full_name >> age3;
    std::cout << "The value stored in the 'full_name' variable is : " << full_name << std::endl;
    std::cout << "The value stored in the 'age3' variable is : " << age3 << std::endl;
    
    std::cin.clear(); //Input stream needs to be cleared in order to use getline
    */
    std::string full_name2;
    int age4;
    std::cout << "Enter your full name and age separated by a space again : " << std::endl;
    std::getline(std::cin, full_name2); //getline function takes 2 input parameters (inputStream, receivingVariable) 
    
    std::cin >> age4;
    std::cout << "The value stored in the 'full_name_2' variable using std::getline is : " << full_name2 << std::endl;
    std::cout << "The value stored in the 'age4' variable using std::getline is : " << age4 << std::endl;
    return 0;
}