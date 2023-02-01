#include <iostream>
#include <string.h>
#include <vector>

std::vector<int> determine_player_order();
void display_board(std::string grid[3][3]);
bool check_row_victory(std::string grid[3][3]);
bool check_col_victory(std::string grid[3][3]);
bool check_diag_victory(std::string grid[3][3]);
bool check_victory(std::string grid[3][3]);
std::vector<int> player_input();
void update_board(std::string grid[3][3], int player_number);
void instruction(std::string grid[3][3]);

