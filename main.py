import random
import pyinputplus as pyip
import os
os.system('cls')

current_player = True
game_ongoing = True

matrix = [["[ ]" for col in range(3)] for row in range(3)]

def empty_board():
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = "[ ]"
        

def display_board():
    print("\n")
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=" ")
        print("\n")

def convert_position(pos):    
    switcher = {
            1: (0, 0),
            2: (1, 0),
            3: (2, 0),
            4: (0, 1),
            5: (1, 1),
            6: (2, 1),
            7: (0, 2),
            8: (1, 2),
            9: (2, 2)}
    return switcher.get(pos)

def handle_turn():
    position = pyip.inputCustom(validateInput, "Choose a position (1-9) ") # index on board
    coord = convert_position(position) # coordinate on board
    matrix[coord[1]][coord[0]] = "[X]" if current_player else "[O]"
    display_board()

def get_square_occupied(coord):
    square = matrix[coord[1]][coord[0]]
    return True if square == "[X]" or square == "[O]" else False

def flip_player():
    global current_player 
    current_player = not current_player

def validateInput(input):
    if int(input) not in range(1, 10):
        raise Exception("Input not in Range!")
    
    if get_square_occupied(convert_position(int(input))):
        raise Exception("Pick an empty square!")
    return int(input)

def check_winner():
    global game_ongoing
    # check rows
    row1 = matrix[0][0] == matrix[0][1] == matrix[0][2] != "[ ]"
    row2 = matrix[1][0] == matrix[1][1] == matrix[1][2] != "[ ]"
    row3 = matrix[2][0] == matrix[2][1] == matrix[2][2] != "[ ]"
    #check columns
    column1 = matrix[0][0] == matrix[1][0] == matrix[2][0] != "[ ]"
    column2 = matrix[0][1] == matrix[1][1] == matrix[2][1] != "[ ]"
    column3 = matrix[0][2] == matrix[1][2] == matrix[2][2] != "[ ]"
    #check diagonals
    diagonal1 = matrix[0][0] == matrix[1][1] == matrix[2][2] != "[ ]"
    diagonal2 = matrix[2][0] == matrix[1][1] == matrix[0][2] != "[ ]"    

    if (row1 or row2 or row3 or 
        column1 or column2 or column3
        or diagonal1 or diagonal2):
        game_ongoing = False
    
def check_game_over():
    check_winner()
    if not game_ongoing: handle_game_over()

def handle_game_over():
    global game_ongoing
    player_name = "Player 1" if current_player else "Player 2"
    print(player_name + " wins!")
    if pyip.inputYesNo("Do you want to play again? ") == "yes":
        game_ongoing = True
        empty_board()
        flip_player()


def play_game(player):
    display_board()

    while game_ongoing:
        #os.system('ls')        
        handle_turn()
        check_game_over()
        flip_player()

play_game(current_player)
