#include <iostream>
/*
Weird Integral Types

Weird?
    Integral types less than 4 bytes in size dont support arithmetic operations
        - addition, subtraction, multiplacation, ...
    
    e.g. char (1byte), short int (2bytes)

    Why dont they support these operations?
        -> processor design has chosen the int as the smallest unit on which operations can be executed
        -> compiler will enforce type conversion to allow operations to occur
*/
int main(){
    short int var1 {10}; // 2 bytes
	short int var2 {20};
	
	char var3 {40}; //1
	char var4 {50};
	
	std::cout << "size of var1 : " << sizeof(var1) << std::endl;
	std::cout << "size of var2 : " << sizeof(var2) << std::endl;
	std::cout << "size of var3 : " << sizeof(var3) << std::endl;
	std::cout << "size of var4 : " << sizeof(var4) << std::endl;
	
    std::cout << "type of var1 : " << typeid(var1).name() << std::endl;
    std::cout << "type of var2 : " << typeid(var2).name() << std::endl;
    std::cout << "type of var3 : " << typeid(var3).name() << std::endl;
    std::cout << "type of var4 : " << typeid(var4).name() << std::endl;

	auto result1 = var1 + var2; // result1 is assigned the int type
	auto result2 = var3 + var4;
	
	std::cout << "size of result1 : " << sizeof(result1) << std::endl; // 4
	std::cout << "size of result2 : " << sizeof(result2) << std::endl; // 4
    std::cout << "type of result1 : " << typeid(result1).name() << std::endl;
    std::cout << "type of result2 : " << typeid(result2).name() << std::endl;
    return 0;
}