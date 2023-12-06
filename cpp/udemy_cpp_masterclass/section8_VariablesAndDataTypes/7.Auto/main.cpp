#include <iostream>
/*
Auto -> Keyword that lets the compiler deduce the variable type from the declaration
    - When to use? When the type name is long and complex and prone to error
*/
int main(){
    auto int_var {12};
    auto dfloat_var {13.0};
    auto sfloat_var {14.0f}; // Cpp standardly assign the double type to a floating point. Explicitly define a single with the f at the end
    auto long_dfloat_var {15.0l};
    auto u_int_var {16u};
    auto ul_int_var {17ul};
    auto ll_int_var {18ll};
    auto char_var {'e'};
    auto str_var {"e"};

    std::cout << "The compiler deduced the following type for int_var " << sizeof(int_var) << std::endl;
    std::cout << "The compiler deduced the following type for dfloat_var " << sizeof(dfloat_var) << std::endl;
    std::cout << "The compiler deduced the following type for sfloat_var " << sizeof(sfloat_var) << std::endl;
    std::cout << "The compiler deduced the following type for long_dfloat_var " << sizeof(long_dfloat_var) << std::endl;
    std::cout << "The compiler deduced the following type for u_int_var " << sizeof(u_int_var) << std::endl;
    std::cout << "The compiler deduced the following type for ul_int_var " << sizeof(ul_int_var) << std::endl;
    std::cout << "The compiler deduced the following type for ll_int_var " << sizeof(ll_int_var) << std::endl;
    std::cout << "The compiler deduced the following type for char_var " << sizeof(char_var) << std::endl;
    std::cout << "The compiler deduced the following type for str_var " << sizeof(str_var) << std::endl;
    return 0;
}