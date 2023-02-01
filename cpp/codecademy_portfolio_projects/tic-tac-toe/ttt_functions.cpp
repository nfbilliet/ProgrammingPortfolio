#include <iostream>
#include <string.h>
#include <vector>

std::vector<int> determine_player_order(){
    std::cout << "A coin toss will determine who will take the first turn. Heads means that player 1 will go first, tails means that player 2 will go first.\n\n";
    std::cout << "Flipping coin...The coin landed on "; 
    int random_coin = std::rand() % 2 + 1;
    std::vector<int> turn_order; 
    if (random_coin == 1){
        std::cout << "heads. Player 1 will make the first move!";
        turn_order.push_back(0);
        turn_order.push_back(1);
    }
    else {
        std::cout << "tails. Player 2 will make the first move!";
        turn_order.push_back(1);
        turn_order.push_back(0);
    }
    std::cout << "\n\n";
    return turn_order;
}

void display_board(std::string grid[3][3]) {
    std::cout << "         |         |         |         |\n";
    std::cout << "         |   (0)   |   (1)   |   (2)   |\n";
    std::cout << "         |         |         |         |\n";
    for (int row_idx=0; row_idx<3; row_idx++){
        std::cout << "----------------------------------------\n";
        std::cout << "         |         |         |         |\n";
        std::cout << "   (" <<row_idx << ")   |";
        for (int col_idx=0; col_idx<3; col_idx++){
            std::cout << "    " << grid[row_idx][col_idx] << "    |";
        }
        std::cout << "\n         |         |         |         |\n";
    }
    std::cout << "----------------------------------------\n";
}

void instruction(std::string grid[3][3]){
    std::cout << "\n===== Tic-Tac-Toe: A short guide to play =====\n\n";
    std::cout << "Welcome to a game of tic-tac-toe. In order to play this you will need 2 players.\n";
    std::cout << "The game board consists of 9 squares that can be identified through the numbers indicated to the left of the grid and on top of the grid.\n\n";
    display_board(grid);
    std::cout << "\nWhile playing you will be asked to enter two numbers separated by a space.\nIf we wish to place our token in the upper left corner for example we would enter '0 0' which indicates the zeroth row and the zeroth column.\n";
    std::cout << "The game continues until a player manages to place 3 of his/hers/theirs tokens in a line.\nAs such there are 3 modes of winning:\n\n";
    std::cout << "1) Row victory\n\n";
    std::string example_row_victory[3][3] = {{"x", "x", "x"},{" ", " ", " "},{" ", " ", " "}};
    display_board(example_row_victory);
    std::cout << "\n2) Column victory\n\n";
    std::string example_col_victory[3][3] = {{"o", " ", " "},{"o", " ", " "},{"o", " ", " "}};
    display_board(example_col_victory);
    std::cout << "\n3) Diagonal victory\n\n";
    std::string example_diag_victory[3][3] = {{"x", " ", " "},{" ", "x", " "},{" ", " ", "x"}};
    display_board(example_diag_victory);
    std::cout << "\n\nIf the game does not have a victor after 9 turns the game will end in a stalemate.\n\n";
    std::cout << "==============================================\n\n";
}

std::vector<int> player_input(){
    std::cout << "Enter the row index followed by the column index of the square where you wish to place your token (seperated by a space)\n\n";
    std::vector<int> target_square;
    int temp_storage;
    for (int i=0; i<2; i++){
        std::cin >> temp_storage;
        target_square.push_back(temp_storage);
    }
    return target_square;
}

void update_board(std::string grid[3][3], int player_number){
    std::vector<int> target_square;
    bool is_empty=false;
    while (is_empty==false){
        target_square = player_input();
        if (grid[target_square[0]][target_square[1]]==" "){
            is_empty=true;
            if (player_number==0){
                grid[target_square[0]][target_square[1]] = "o";
            }
            else if (player_number==1) {
                grid[target_square[0]][target_square[1]] = "x";
            }
        }
        else {
            std::cout << "The square you have selected is not empty. Please choose make another choice \n\n";
        }
    }
}

bool check_row_victory(std::string grid[3][3]){
    bool victory_condition = false;
    for (int row_idx=0; row_idx<3; row_idx++){
        if (grid[row_idx][0]==grid[row_idx][1] && grid[row_idx][0]==grid[row_idx][2] && grid[row_idx][0]!= " "){
            victory_condition = true;
        }
    }
    return victory_condition;
}

bool check_col_victory(std::string grid[3][3]){
    bool victory_condition = false;
    for (int col_idx=0; col_idx<3; col_idx++){
        if (grid[0][col_idx]==grid[1][col_idx] && grid[0][col_idx]==grid[2][col_idx] && grid[0][col_idx]!= " "){
            victory_condition = true;
        }
    }
    return victory_condition;
}

bool check_diag_victory(std::string grid[3][3]){
    bool victory_condition = false;
    if (grid[0][0]==grid[1][1] && grid[0][0]==grid[2][2] && grid[0][0]!=" "){
        victory_condition = true;
    }
    else if (grid[0][2]==grid[1][1] && grid[0][2]==grid[2][0] && grid[0][2]!=" "){
        victory_condition = true;
    }
    return victory_condition;
}

bool check_victory(std::string grid[3][3]){  
    std::vector<bool> victory_check = {check_row_victory(grid), check_col_victory(grid), check_diag_victory(grid)}; 
    for (int i = 0; i<victory_check.size(); i++){
        if (victory_check[i]==true){
            return true;
        }
    }
    return false;
}