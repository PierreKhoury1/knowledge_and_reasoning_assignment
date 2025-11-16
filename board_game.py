from game_state import *

def create_initial_board():
    board = [[EMPTY for _ in range(8)] for _ in range(8)]

    def dark_square(row, col):
        return (row + col) % 2 == 1
    
    #black pieces on rows 0, 1, 2
    for row in range(3):
        for col in range(8):
            if dark_square(row, col):
                board[row][col] = BLACK_PAWN

    #white pieces on rows 5,6,7
    for row in range(5, 8):
        for col in range(8):
            if dark_square(row, col):
                board[row][col] = WHITE_PAWN

    return board 

def print_board_game(state):
    symbols = {
                EMPTY: ".",
        BLACK_PAWN: "b",
        BLACK_KING: "B",
        WHITE_PAWN: "w",
        WHITE_KING: "W",
    }

    for row in range(8):
        line = ""
        for col in range(8):
            line  += symbols[state.board_layout[row][col]] + " "
        print(line)


def is_opponents_turn(piece, player):

    # Return True if the piece belongs to the opponent player
    # this function checks if the peice is for the player or the opponent
    if piece == EMPTY:
        return False
    if player == BLACK:
        return piece in (WHITE_PAWN, WHITE_KING)
    else:
        return piece in (BLACK_PAWN, BLACK_KING)
    
