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
    if (choice == 1) {
        std::cout << "As your family runs inside you remain outside in the field you were previously working on. In the panic of it all you dropped the shovel you were using to dig holes. In the distance you see the fairies encroaching ever closer.\n\n";
        std::cout << "1) You pick up the shovel and prepare to attack the fairies.\n2) You taunt the fairies to follow you and run away.\n\nMake your choice:";
        choice=0;
        while ((choice !=1) && (choice != 2)) {
        std::cin >> choice;
        if(std::cin.fail()) { 
            std::cout << "You entered something that is not a number. Please enter a number.\n\nMake your choice: ";
            std::cin.clear();
            std::cin.ignore();
        }
        std::cin.clear();
        if (choice==1){
            std::cout << "Armed with a shovel in hand you storm up to the fairies. However, you imagined this going a lot smoother in your head as you are easily cut down by the fairies. Despite iminent death, you died trying and will be remembered as brave yet incredibly dumb.";
        }
        else if (choice==2){
            std::cout << "Taunting the fairies, you manage to distract them enough away from your house leaving ample oppurtunity for you family to escape. As the fairies chase after you, you eventually falter and are caught by the fairies. Quickly after this you are disposed of by the fairies. Your death was not for nothing as your family managed to escape complete extermination. From this point onward you will be remembered as a family hero.";
        }
    }
    }
    else if (choice == 2) {
        std::cout << "In the distance you hear the cries of your family meeting their end due to the attacking fairies.<\n\n";
        std::cout << "1) The cries put you in a state of shock and you collapse down.\n2) The cries cause you to panic even further and you run even faster towards the woods.\n3) Enraged by the death of your family you run towards the fairies responsible for their death.\n\nMake your choice:";
        choice=0;
        while ((choice !=1) && (choice != 2) && (choice != 3)) {
        std::cin >> choice;
        if(std::cin.fail()) { 
            std::cout << "You entered something that is not a number. Please enter a number.\n\nMake your choice: ";
            std::cin.clear();
            std::cin.ignore();
        }
        std::cin.clear();
        if (choice==1){
            std::cout << "The shock causes you to halt your escape and are easily apprehended and succesively executed. Your death is pointless and quite shameful to be honest.";
        }
        else if (choice==2){
            std::cout << "Fueled by panic you sprint into the forest and succesively escape the roving band of faeries. Upon returning to the village the next day you see that everything is destroyed and no survivors remain. The shame and trauma causes you to live out your live in isolation in the forest as a hermit.";
        }
        else if (choice==3){
            std::cout << "You charge the faeries in blind rage while not holding a weapon and are cut down immediately. Your death was very meaningless indeed.";
        }
    }    
    }
    else if (choice == 3) {
        std::cout << "Completely still, you assume the pose of your favourite scarecrow when growing up. The fairies running completely past you and killing your family in the process.\n\n";
        std::cout << "1) You are the scarecrow, you have always been a scarecrow. The death of your family does not move you as you watch everything unfold glassy-eyed and emotionless.\n2) Unable to control your emotions you break your act of the family scarecrow as you try to help them in the onslaught.\n\nMake your choice:";
        choice=0;
        while ((choice !=1) && (choice != 2)) {
        std::cin >> choice;
        if(std::cin.fail()) { 
            std::cout << "You entered something that is not a number. Please enter a number.\n\nMake your choice: ";
            std::cin.clear();
            std::cin.ignore();
        }
        std::cin.clear();
        if (choice==1){
            std::cout << "You made your choice and are commited to the act. As everything around you get destroyed you watch completely still and are unmoved by the flights of everyone you knew since the beginning of your life. After the destruction you remain motionless and assume your role as a scarecrow for the rest of your life.";
        }
        else if (choice==2){
            std::cout << "You charge the faeries in blind rage while not holding a weapon and are cut down immediately. Your death was very meaningless indeed.";
        }
    }
    }
}