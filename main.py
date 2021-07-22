import random
import pygame
import pyinputplus as pyip
import os
import sys

os.system('cls')

WIDTH = 600
HEIGHT = 600

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

current_player = True
game_ongoing = True
draw = False
ai_turn_count = 0

matrix = [["[ ]" for col in range(3)] for row in range(3)]
directions  = [(0, 1), (1, 0), (1, 1), (-1, 0), (0, -1), (-1, -1)]

def empty_board():
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = "[ ]"
        
def display_board():
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

def handle_player_turn():
    position = pyip.inputCustom(validateInput, "Choose a position (1-9) ") # number on board
    coord = convert_position(position) # coordinate on board
    handle_turn(coord)

def handle_turn(coord):
    global matrix
    matrix[coord[1]][coord[0]] = "[X]" if current_player else "[O]"
    os.system('cls')
    display_board()
    return

def get_square_occupied(coord):
    square = matrix[coord[1]][coord[0]]
    return True if square == "[X]" or square == "[O]" else False

def get_board_full():
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if get_square_occupied((i, j)) == False:
                return False
    return True

def flip_player():
    global current_player 
    current_player = not current_player

def get_random_square():
    square_occupied = True
    while square_occupied:
        choice = random.randrange(1, 9)
        square_occupied = get_square_occupied(convert_position(choice))
    return convert_position(choice)

def get_empty_squares():
    empty_squares = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if get_square_occupied((i, j)) == False:
                empty_squares.append((i, j))
    return empty_squares

def validateInput(input):
    if int(input) not in range(1, 10):
        raise Exception("Input not in Range!")
    
    if get_square_occupied(convert_position(int(input))):
        raise Exception("Pick an empty square!")
    return int(input)

def check_winner(board):
    # check rows
    row1 = board[0][0] == board[0][1] == board[0][2] != "[ ]"
    row2 = board[1][0] == board[1][1] == board[1][2] != "[ ]"
    row3 = board[2][0] == board[2][1] == board[2][2] != "[ ]"
    #check columns
    column1 = board[0][0] == board[1][0] == board[2][0] != "[ ]"
    column2 = board[0][1] == board[1][1] == board[2][1] != "[ ]"
    column3 = board[0][2] == board[1][2] == board[2][2] != "[ ]"
    #check diagonals
    diagonal1 = board[0][0] == board[1][1] == board[2][2] != "[ ]"
    diagonal2 = board[2][0] == board[1][1] == board[0][2] != "[ ]"    

    if (row1 or row2 or row3 or 
        column1 or column2 or column3
        or diagonal1 or diagonal2):
        return True
    else:
        return False

def copy_board(board):
    newBoard = []
    for i in board:
        newBoard.append(i)
    return newBoard

def handle_ai_turn():
    if not get_board_full():
        possible_turns = get_empty_squares()
        # Check for win conditions in rows
        for let in ["[O]", "[X]"]:
            for i in range(len(matrix)):
                if matrix[i].count(let) == 2 and "[ ]" in matrix[i]:
                    pos = (matrix[i].index("[ ]"), i)
                    handle_turn(pos)
                    return
        # Check for win conditions in columns
        for let in ["[O]", "[X]"]:
            flipped_list = list(zip(*matrix.copy()))
            for i in range(len(flipped_list)):
                if flipped_list[i].count(let) == 2 and "[ ]" in flipped_list[i]:
                    pos = (i, flipped_list[i].index("[ ]"))
                    handle_turn(pos)
                    return
        # Check for win conditions in diagonals
        diagonal1 = [[0, 0], [1, 1], [2, 2]]
        diagonal2 = [[2, 0], [1, 1], [0, 2]]
        diagonals = [diagonal1, diagonal2]
        for let in ["[O]", "[X]"]:
            for diagonal in diagonals:
                occupied = 0
                vacant = 0
                vacant_coord = []
                
                for i in diagonal:
                    if matrix[i[1]][i[0]] == let:
                        occupied += 1
                    elif matrix[i[1]][i[0]] == "[ ]":
                        vacant += 1
                        vacant_coord = i
                if occupied == 2 and vacant == 1:
                    handle_turn(vacant_coord)
                    return

        corners_open = [i for i in possible_turns if i in [(0, 0), (0, 2), (2, 0), (2, 2)]]       
        if len(corners_open) > 0:
            handle_turn(random.choice(corners_open))
            return 
        
        if bool(random.getrandbits(1)): 
            if not get_square_occupied((1, 1)):
                handle_turn((1, 1))
                return 

        edges_open = [i for i in possible_turns if i in [(0, 1), (1, 0), (1, 2), (2, 1)]]
        if len(corners_open) > 0:
            handle_turn(random.choice(edges_open))
            return 
 
        handle_turn(random.choice(possible_turns))

def handle_game_over():
    global game_ongoing
    global draw
    global ai_turn_count
    if draw:
        print("It's a draw!")
    else:
        player_name = "Player 1" if current_player else "Player 2"
        print(player_name + " wins!")
    if pyip.inputYesNo("Do you want to play again? ") == "yes":
        game_ongoing = True
        draw = False
        ai_turn_count = 0
        empty_board()
        os.system("cls")
        display_board()
    else:
        sys.exit()

def check_game_over():
    global draw
    if check_winner(matrix):
        handle_game_over()
        return True
    elif get_board_full():
        draw = True
        handle_game_over()
        return True
    return False

def play_game(player):
    display_board()

    while game_ongoing:    
        handle_player_turn()
        if check_game_over(): continue
        flip_player()
        handle_ai_turn()
        check_game_over()
        flip_player()        

play_game(current_player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()