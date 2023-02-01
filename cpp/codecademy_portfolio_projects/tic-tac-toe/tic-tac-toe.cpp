#include <iostream>
#include <string.h>
#include <vector>
#include "ttt_functions.hpp"

// Tic-Tac-Toe game

int main() {
    std::cout << "===============================================\n";
    std::cout << "=                                             =\n";
    std::cout << "=               TIC - TAC - TOE               =\n";
    std::cout << "=                                             =\n";
    std::cout << "===============================================\n\n";
    std::vector<std::string> player_names;
    std::cout << "Welcome to tic-tac-toe!\n\nPlayer 1 please enter your name: ";
    std::string name_placeholder;
    std::cin >> name_placeholder;
    player_names.push_back(name_placeholder);
    std::cout << "\nPlayer 2 please enter your name: ";
    std::cin >> name_placeholder;
    player_names.push_back(name_placeholder);
    std::cout << "\n\nPlayer 1 will use the 'o' symbol as his/her/their token. Player 2 will use the 'x' symbol as his/her/their token.\n\n";
    
    std::string game_grid[3][3] = { {" ", " ", " "}, {" ", " ", " "}, {" ", " ", " "}};
    
    std::string need_instruction;
    std::cout << "Do you require instructions regarding how to play the game? [y/n]\n";
    std::cin >> need_instruction;
    if (need_instruction=="y"){
        instruction(game_grid);
    }
    
    std::vector<int> turn_order = determine_player_order();

    // The game can last up to 9 turns. 
    int nmb_turns = 0;

    // The bool indicates if someone has won the game or if no one has won. 
    bool victory = false;

    while (nmb_turns<9 && victory==false){
        int current_player;
        for (int i=0;i<turn_order.size();i++){
            current_player = turn_order[i];
            display_board(game_grid);
            std::cout << "Player " << turn_order[i]+1 << " (" << player_names[turn_order[i]] << ") take your turn.\n\n";
            update_board(game_grid, turn_order[i]);
            victory = check_victory(game_grid);
            if (victory==true){
                break;
            }
        }
        if (victory==true){
            std::cout << "Player " << turn_order[current_player]+1 << " has won the game!\n\n";
            display_board(game_grid);
            }   
        nmb_turns++;
    }
}
