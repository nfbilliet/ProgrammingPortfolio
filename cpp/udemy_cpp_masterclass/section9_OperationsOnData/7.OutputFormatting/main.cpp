#include <iostream>
#include <ios>
#include <iomanip>

using namespace std;
/*
---Output formatting---

Control how we wish the information that is streamed out from the code to the terminal to be displayed to the user
    - <ios> library
    - <iomanip> library

The complete reference for all the input and output manipulators can be found at

    https://en.cppreference.com/w/cpp/io/manip

Overview of the different operators that we wish to use
    1) std::endl 
        -> equivalent to ending the ouput stream with the new line character '\n'
    2) std::flush 
        -> Immediately send the data that is stored in the output buffer to the output stream          
        -> A buffer flush is the transfer of computer data from a temporary storage area to the computer’s permanent memory.
        -> In C++, we can explicitly be flushed to force the buffer to be written. 
           Generally, the std::endl function works the same by inserting a new-line character and flushes the stream. 
           stdout/cout is line-buffered that is the output doesn’t get sent to the OS until you write a newline or explicitly flush the buffer.
        -> An output buffer is a memory or cache location where data is held until an output device or file is ready to receive it. 
           More plainly, it's a temporary storage area that holds data before sending it to a specific destination.
           The output buffer manages the data flow between different system components, ensuring the data is transmitted efficiently and effectively. 
           Essentially, buffers help smooth variations in data rates, prevent bottlenecks, and allow for better coordination between different parts of a computing system.
    3) std::setw(int_value) [setwidth]
        -> changes the width of the next input/output field
    
*/

int main(){
    /*
    std::endl demonstration
    */

    // Without any delimiter character
    cout << "Hello";
    cout << "World";
    cout << "\n---------" << endl;
    // Result will be 'HelloWorld' in the terminal

    // With the '\n' at the end
    cout << "Hello\n";
    cout << "World\n";
    cout << "---------" << endl;
    // Will produce Hello (new line) World

    // With std::endl at the end of the cout statement
    cout << "Hello" << endl;
    cout << "World" << endl;
    cout << "---------" << endl;

    /*
    std:flush demonstration
    */
 
    cout << "This is a message" << endl << flush;

    //std::setw() : Adjusts the field with for the item about to be printed. 
    //The setw() manipulator only affects the next value to be printed.
    
    std::cout << "Unformatted table : " << std::endl;
    std::cout << "Daniel" << " " << "Gray" << " 25" << std::endl;
    std::cout << "Stanley" <<" "  << "Woods" << " 33" << std::endl;
    std::cout << "Jordan" << " "  << "Parker" << " 45" << std::endl;
    std::cout << "Joe" << " " << "Ball" << " 21" << std::endl;
    std::cout << "Josh" << " " << "Carr" << " 27" << std::endl;
    std::cout << "Izaiah" << " " << "Robinson" << " 29" << std::endl;
    
    std::cout << std::endl;
    std::cout << "Formatted table  (width 10): " << std::endl;
    
    std::cout << std::setw(10) <<  "Lastname"  << std::setw(10) << "Firstname" << std::setw(10) << "Age" << std::endl;
    std::cout << std::setw(10) << "Daniel"  << std::setw(10) << "Gray" << std::setw(10) << "25" << std::endl;
    std::cout << std::setw(10) << "Stanley" << std::setw(10)  << "Woods" << std::setw(10) <<  "33" << std::endl;
    std::cout << std::setw(10) <<  "Jordan" << std::setw(10)  << "Parker" << std::setw(10) << "45" << std::endl;
    std::cout << std::setw(10) <<  "Joe" << std::setw(10) << "Ball" << std::setw(10) << "21" << std::endl;
    std::cout << std::setw(10) << "Josh" << std::setw(10) << "Carr" << std::setw(10) <<"27" << std::endl;
    std::cout << std::setw(10) << "Izaiah" << std::setw(10) << "Robinson" << std::setw(10) << "29" << std::endl;

    std::cout << std::endl;
    std::cout << "Formatted table  (width 8): " << std::endl;
    
    std::cout << std::setw(8) <<  "Lastname"  << std::setw(8) << "Firstname" << std::setw(8) << "Age" << std::endl;
    std::cout << std::setw(8) << "Daniel"  << std::setw(8) << "Gray" << std::setw(8) << "25" << std::endl;
    std::cout << std::setw(8) << "Stanley" << std::setw(8)  << "Woods" << std::setw(8) <<  "33" << std::endl;
    std::cout << std::setw(8) <<  "Jordan" << std::setw(8)  << "Parker" << std::setw(8) << "45" << std::endl;
    std::cout << std::setw(8) <<  "Joe" << std::setw(8) << "Ball" << std::setw(8) << "21" << std::endl;
    std::cout << std::setw(8) << "Josh" << std::setw(8) << "Carr" << std::setw(8) <<"27" << std::endl;
    std::cout << std::setw(8) << "Izaiah" << std::setw(8) << "Robinson" << std::setw(8) << "29" << std::endl;

    std::cout << std::endl;
    std::cout << "Formatted table  (width 5): " << std::endl;
    
    std::cout << std::setw(5) <<  "Lastname"  << std::setw(5) << "Firstname" << std::setw(5) << "Age" << std::endl;
    std::cout << std::setw(5) << "Daniel"  << std::setw(5) << "Gray" << std::setw(5) << "25" << std::endl;
    std::cout << std::setw(5) << "Stanley" << std::setw(5)  << "Woods" << std::setw(5) <<  "33" << std::endl;
    std::cout << std::setw(5) <<  "Jordan" << std::setw(5)  << "Parker" << std::setw(5) << "45" << std::endl;
    std::cout << std::setw(5) <<  "Joe" << std::setw(5) << "Ball" << std::setw(5) << "21" << std::endl;
    std::cout << std::setw(5) << "Josh" << std::setw(5) << "Carr" << std::setw(5) <<"27" << std::endl;
    std::cout << std::setw(5) << "Izaiah" << std::setw(5) << "Robinson" << std::setw(5) << "29" << std::endl;

    /*
    The width controls how much each output field for the next item is. If the width is greater than the item than the 
    item gets lined out to the right and the rest is padded with filler characters, i.e. ' ' standard. If the item is greater
    then the specified width it is printed without any outlining and padding characters.
    */

    //===================================================================
    std::cout << std::endl;

    //Justify : Values can be justified in their fields. There are three manipulators
    //          for adjusting the justification: left, right, and internal. 
    
    //right justified
    std::cout << std::endl;
    std::cout << "Right justified table(default) :  " << std::endl;
    
    int col_width = 20;
    
    std::cout << std::right;
    std::cout << std::setw(col_width) <<  "Lastname"  << std::setw(col_width) << "Firstname" << std::setw(col_width/2) << "Age" << std::endl;
    std::cout << std::setw(col_width) << "Daniel"  << std::setw(col_width) << "Gray" << std::setw(col_width/2) << "25" << std::endl;
    std::cout << std::setw(col_width) << "Stanley" << std::setw(col_width)  << "Woods" << std::setw(col_width/2) <<  "33" << std::endl;
    std::cout << std::setw(col_width) <<  "Jordan" << std::setw(col_width)  << "Parker" << std::setw(col_width/2) << "45" << std::endl;
    std::cout << std::setw(col_width) <<  "Joe" << std::setw(col_width) << "Ball" << std::setw(col_width/2) << "21" << std::endl;
    std::cout << std::setw(col_width) << "Josh" << std::setw(col_width) << "Carr" << std::setw(col_width/2) <<"27" << std::endl;
    std::cout << std::setw(col_width) << "Izaiah" << std::setw(col_width) << "Robinson" << std::setw(col_width/2) << "29" << std::endl;
    


    //Left justified
    std::cout << std::endl;
    std::cout << "Left justified table :  " << std::endl;
    
    col_width = 20;
    
    std::cout << std::left;
    std::cout << std::setw(col_width) <<  "Lastname"  << std::setw(col_width) << "Firstname" << std::setw(col_width/2) << "Age" << std::endl;
    std::cout << std::setw(col_width) << "Daniel"  << std::setw(col_width) << "Gray" << std::setw(col_width/2) << "25" << std::endl;
    std::cout << std::setw(col_width) << "Stanley" << std::setw(col_width)  << "Woods" << std::setw(col_width/2) <<  "33" << std::endl;
    std::cout << std::setw(col_width) <<  "Jordan" << std::setw(col_width)  << "Parker" << std::setw(col_width/2) << "45" << std::endl;
    std::cout << std::setw(col_width) <<  "Joe" << std::setw(col_width) << "Ball" << std::setw(col_width/2) << "21" << std::endl;
    std::cout << std::setw(col_width) << "Josh" << std::setw(col_width) << "Carr" << std::setw(col_width/2) <<"27" << std::endl;
    std::cout << std::setw(col_width) << "Izaiah" << std::setw(col_width) << "Robinson" << std::setw(col_width/2) << "29" << std::endl;
    

    //Internal justified : sign is left justified , data is right justified
    std::cout << std::endl;
    std::cout << "Internal justified : " << std::endl;
    std::cout << std::right;
    std::cout << std::setw(10) << -123.45 << std::endl;
    std::cout << std::internal;
    std::cout << std::setw(10) << -123.45 << std::endl;
    
    //===================================================================

    std::cout << std::endl;

    //setfill
    
    std::cout << std::endl;
    std::cout << "Table with fill characters :  " << std::endl;
    
    
    col_width = 20;
    
    std::cout << std::left;
    std::cout << std::setfill('*'); // The fill character
    std::cout << std::setw(col_width) <<  "Lastname"  << std::setw(col_width) << "Firstname" << std::setw(col_width/2) << "Age" << std::endl;
    std::cout << std::setw(col_width) << "Daniel"  << std::setw(col_width) << "Gray" << std::setw(col_width/2) << "25" << std::endl;
    std::cout << std::setw(col_width) << "Stanley" << std::setw(col_width)  << "Woods" << std::setw(col_width/2) <<  "33" << std::endl;
    std::cout << std::setw(col_width) <<  "Jordan" << std::setw(col_width)  << "Parker" << std::setw(col_width/2) << "45" << std::endl;
    std::cout << std::setw(col_width) <<  "Joe" << std::setw(col_width) << "Ball" << std::setw(col_width/2) << "21" << std::endl;
    std::cout << std::setw(col_width) << "Josh" << std::setw(col_width) << "Carr" << std::setw(col_width/2) <<"27" << std::endl;
    std::cout << std::setw(col_width) << "Izaiah" << std::setw(col_width) << "Robinson" << std::setw(col_width/2) << "29" << std::endl;
    
    //===================================================================
    std::cout << std::endl;

    //boolalpha and noboolapha : control bool output format : 1/0 or true/false
    
    bool condition {true};
    bool other_condition {false};
    
    std::cout << "condition : " << condition << std::endl;
    std::cout << "other_condition : " << other_condition << std::endl;
    
    std::cout << std::endl;
    std::cout << std::boolalpha;
    cout << "boolalpha enabled" << endl;
    std::cout << "condition : " << condition << std::endl;
    std::cout << "other_condition : " << other_condition << std::endl;
    
    std::cout << std::endl;
    std::cout << std::noboolalpha;
    cout << "noboolalpha enabled" << endl;
    std::cout << "condition : " << condition << std::endl;
    std::cout << "other_condition : " << other_condition << std::endl;
    
    //===================================================================
    std::cout << std::endl;

    //showpos and noshowpos : show or hide the +  sign for positive numbers
    
    int pos_num {34};
    int neg_num {-45};
    
    std::cout << "pos_num : " << pos_num << std::endl;
    std::cout << "neg_num : " << neg_num << std::endl;
    
    std::cout << std::endl;
    std::cout << std::showpos;
    cout << "showpos enabled" << endl;
    std::cout << "pos_num : " << pos_num << std::endl;
    std::cout << "neg_num : " << neg_num << std::endl; 

    std::cout << std::endl;
    std::cout << std::noshowpos;
    cout << "noshowpos enabled" << endl;
    std::cout << "pos_num : " << pos_num << std::endl;
    std::cout << "neg_num : " << neg_num << std::endl;   


    //===================================================================
    std::cout << std::endl;


    //different number systems : std::dec, std::hex, std::oct
    
    int pos_int {717171};
    int neg_int {-47347};
    double double_var {498.32};
    
    std::cout << std::endl;
    std::cout << "default base format : " << std::endl;
    std::cout << "pos_int : " << pos_int << std::endl;
    std::cout << "neg_int : " << neg_int << std::endl;
    std::cout << "double_var : " << double_var << std::endl;
    
    std::cout << std::endl;
    std::cout << "pos_int in different bases : " << std::endl;
    std::cout << "pos_int (dec) : " << std::dec << pos_int << std::endl;
    std::cout << "pos_int (hex) : " << std::hex << pos_int << std::endl;
    std::cout << "pos_int (oct) : " << std::oct << pos_int << std::endl;
    
    std::cout << std::endl;
    std::cout << "neg_int in different bases : " << std::endl;
    std::cout << "neg_int (dec) : " << std::dec << neg_int << std::endl;
    std::cout << "neg_int (hex) : " << std::hex << neg_int << std::endl;
    std::cout << "neg_int (oct) : " << std::oct << neg_int << std::endl;
    
    std::cout << std::endl;
    std::cout << "double_var in different bases : " << std::endl;
    std::cout << "double_var (dec) : " << std::dec << double_var << std::endl;
    std::cout << "double_var (hex) : " << std::hex << double_var << std::endl;
    std::cout << "double_var (oct) : " << std::oct << double_var << std::endl;
    // floats and doubles are described using a different format. hex and oct has no effect on this
    
    //===================================================================
    std::cout << std::endl;


    //uppercase and nouppercase

    pos_int = 717171;
    
    std::cout << "pos_int (nouppercase : default) : " << std::endl;
    std::cout << "pos_int (dec) : " << std::dec << pos_int << std::endl;
    std::cout << "pos_int (hex) : " << std::hex << pos_int << std::endl;
    std::cout << "pos_int (oct) : " << std::oct << pos_int << std::endl;
    
    std::cout << std::endl;
    std::cout << "pos_int (uppercase) : " << std::endl;
    std::cout << std::uppercase;
    std::cout << "pos_int (dec) : " << std::dec << pos_int << std::endl;
    std::cout << "pos_int (hex) : " << std::hex << pos_int << std::endl;
    std::cout << "pos_int (oct) : " << std::oct << pos_int << std::endl;
    
    
    //===================================================================
    std::cout << std::endl;


    //fixed and scientific : for floating point values
    
    double a{ 3.1415926535897932384626433832795 };
    double b{ 2006.0 };
    double c{ 1.34e-10 };
    
    std::cout << std::endl;
    std::cout << "double values (default : use scientific where necessary) : " << std::endl;
    std::cout << "a : " << a << std::endl;
    std::cout << "b : " << b << std::endl;
    std::cout << "c : " << c << std::endl;
    
    std::cout << std::endl;
    std::cout << "double values (fixed) : " << std::endl;
    std::cout << std::fixed;
    std::cout << "a : " << a << std::endl;
    std::cout << "b : " << b << std::endl;
    std::cout << "c : " << c << std::endl;
    
    std::cout << std::endl;
    std::cout << "double values (scientific) : " << std::endl;
    std::cout << std::scientific;
    std::cout << "a : " << a << std::endl;
    std::cout << "b : " << b << std::endl;
    std::cout << "c : " << c << std::endl;

    std::cout << std::endl;
    std::cout << "double values (back to defaults) : " << std::endl;
    std::cout.unsetf(std::ios::scientific | std::ios::fixed); // Hack
    std::cout << "a : " << a << std::endl;
    std::cout << "b : " << b << std::endl;
    std::cout << "c : " << c << std::endl;
    
    
    //===================================================================
    std::cout << std::endl;

    //setprecision() : the number of digits printed out for a floating point. Default is 6
    
    a = 3.1415926535897932384626433832795;
    
    std::cout << std::endl;
    std::cout << "a (default precision(6)) : " << a <<  std::endl;
    std::cout << std::setprecision(10);
    std::cout << "a (precision(10)) : " << a << std::endl;
    std::cout << std::setprecision(20);
    std::cout << "a (precision(20)) : " << a << std::endl;
    
    //If the precision is bigger than supported by the type, you'll just print garbage.
    
    //===================================================================
    std::cout << std::endl;


    //showpoint and noshowpoint : show trailing zeros if necessary
    //Force output of the decimal point
    
    double d {34.1};
    double e {101.99};
    double f {12.0};
    int    g {45};
    
    std::cout << std::endl;
    std::cout << "noshowpoint (default) : " << std::endl;
    std::cout << "d : " << d << std::endl;
    std::cout << "e : " << e << std::endl;
    std::cout << "f : " << f << std::endl; // 12
    std::cout << "g : " << g << std::endl;
    
    std::cout << std::endl;
    std::cout << "showpoint: " << std::endl;
    std::cout << std::showpoint;
    std::cout << "d : " << d << std::endl;
    std::cout << "e : " << e << std::endl;
    std::cout << "f : " << f << std::endl; // 12.0
    std::cout << "g : " << g << std::endl;
    return 0;
}