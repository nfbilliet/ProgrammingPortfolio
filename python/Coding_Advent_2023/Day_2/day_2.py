import numpy as np
import pandas as pd

def format_line(game_line):
    """
    Take a line that represents a game and transform it into a list that saves the individual draw as list items
    e.g. "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
         -> [[[3,"blue"],[4,"red"]], [[1,"red"],[2,"green"],[6,"blue"]], [[2, "green"]]]
    """
    game_list = game_line.split(":")
    game_list = game_list[1].split(";")
    game_list = [game_draw.split(",") for game_draw in game_list]
    game_list = [[nmb_cubes.split(" ")[1:] for nmb_cubes in game_draw]for game_draw in game_list]    
    return game_list

idx_dict = dict(zip(["blue", "green", "red"],[0,1,2]))
def format_draw(inp_draw):
    """
    Transform a string of numbers with colours into a list of lists where the number of cubes and colour 
    are listed seperately
    e.g. "[['3', 'blue'], ['4', 'red']]"
         -> [3,0,4] (implicit 0 green)
         -> ordering according to [nmb_blue, nmb_green, nmb_red]
    """
    output_row = [0,0,0]
    for draw_item in inp_draw:
        output_row[idx_dict[draw_item[1]]] += int(draw_item[0])
    return output_row

def gameMatrix_constructor(game_line):
    return np.array([format_draw(draw) for draw in format_line(game_line)])

print(gameMatrix_constructor("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"))

def constraint_checker(gameMatrix, nmb_constrains=[14,13,12]):
    """
    Check if the game and its consisting draws adhere to the predefined constraint on the number of cubes of each color
    e.g. (1) [[3,0,4], -> 1
              [6,2,1],
              [0,2,0]]
             No column entry exceeds the predefined maximum
         (2) [[6,1,3],  -> 0
              [0,3,6],
              [15,0,14]]
             In the last row both the blue and red value exceed the predefined maximum
    """
    nmb_rows = gameMatrix.shape[0]
    for col_idx in  [0,1,2]:
        bool_array = gameMatrix[:,col_idx] <= nmb_constrains[col_idx]
        if False in bool_array:
            return 0
    return 1

"""
test_array_1 = np.array([[3,0,4],[6,2,1],[0,2,0]])
test_array_2 = np.array([[6,1,3],[0,3,6],[15,0,14]])
print(constraint_checker(test_array_1))
print(constraint_checker(test_array_2))
"""

def id_sum(fname, nmb_constrains=[14,13,12]):
    """
    Take an input file containing a number of games and determine which games are possible given the predefined constraint.
    Isolate the game id number for these and return the sum of their id's
    e.g. game 1 and game 2 are valid -> 3
    """
    with open(fname, "r") as myFile:
        game_data = myFile.read().splitlines()
    id_array = np.array([[id+1] for id in range(len(game_data))])
    valid_array = np.array([constraint_checker(gameMatrix_constructor(game_line), nmb_constrains=nmb_constrains) 
                            for game_line in game_data])
    return np.dot(valid_array, id_array)[0]
#test_input_p1.txt should result in 8
#id_sum("test_input_p1.txt")
print(id_sum("puzzle_input.txt"))

def power_sum(fname):
    with open(fname, "r") as myFile:
        game_data = myFile.read().splitlines()
    game_matrices = [gameMatrix_constructor(game_line) for game_line in game_data]
    fewest_number = [np.amax(game_matrix, axis=0) for game_matrix in game_matrices]  
    power_array = [np.prod(game_array) for game_array in fewest_number]  
    return np.sum(power_array)

print(power_sum("puzzle_input.txt"))