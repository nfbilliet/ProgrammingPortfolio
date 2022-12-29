#include <iostream>

int main() {
    /*This program is a choose your own adventure text based game*/
    std::cout<<"You live in the quiet hamlet of Vanillaville where you help your mother and father work the field and earn a modest living. But oh no, from over the fields a horde of nasty looking fairies approaches the village and are looking to pillage, loot and be fabulous!\n\nAs you see the fairies approaching to your house you have a fraction of a second to react\n\n";
    std::cout<<"1) You yell to your family to get inside quickly before it is too late.\n2) You run away from your house without looking out for your family.\n3) You pretend to be a scarecrow by standing completely still and motionless.\n\nMake your choice: ";
    int choice=0;
    while ((choice !=1) && (choice != 2) && (choice != 3)) {
        std::cin >> choice;
        if(std::cin.fail()) { 
            std::cout << "You entered something that is not a number. Please enter a number.\n\nMake your choice: ";
            // Clear fail state
            std::cin.clear();
            // discard the current awnser from the cin buffer to prevent the loop from continuing
            std::cin.ignore();
        }
        //In order not to get stuck in an infinite while loop the input stream needs to be cleared so that we can enter a different choice
        std::cin.clear();
    }
}