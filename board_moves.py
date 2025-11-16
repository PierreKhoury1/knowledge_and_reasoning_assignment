from game_state import *


def get_simple_moves(state):
    moves = [] # each move will be (start_position, end_position)

    board = state.board_layout
    player = state.current_player

    for row in range(8):
        for col in range(8):


            piece = board[row][col]
            # this points at the current player
            if player == BLACK and piece in (BLACK_PAWN, BLACK_KING):
                moves += simple_moves_for_piece(board, row, col, piece)

            elif player == WHITE and piece in (WHITE_PAWN, WHITE_KING):
                moves += simple_moves_for_piece(board, row, col, piece)


    return moves


def simple_moves_for_piece(board, row, col, piece):
    simple_moves = []

    directions = [] # this will determine  movement directions

    if piece ==  BLACK_PAWN:
        directions = [(1, -1), (1, 1)] #down-left , down-right

    elif piece == WHITE_PAWN:
        directions = [(-1, -1), (-1, 1)] #up-left, up-right
    else:
        directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)] # this is so the king moves in all 4 diagonal directions

    # loop through each possible diagonal, and try all the moves

    for delta_row, delta_col in directions:
        new_row = row + delta_row
        new_col = col + delta_col

        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] == EMPTY:
                simple_moves.append([(row, col), (new_row, new_col)])

    return simple_moves


def capture_moves_for_piece(board, row, col, piece, player):

    capture_sequences = [] # final list of all capture paths for this piece

    #determine which directions this piece is allwed to move/jump 
    # pawns are only allowed to move forward; while kings move in all four diagonals

    if piece == BLACK_PAWN:
        directions = [(1, -1), (1, 1)] #black pawn jumps downward
    elif piece == WHITE_PAWN:
        directions = [(-1, -1), (-1, 1)] #white pawn jumps upward

    else:
        directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)] # king is allowed to go in all diagonal directions

    def dfs(path, row, col, board_state):

        found_jump = False # becomes True if at least one jump is possible 

        for delta_row, delta_col in directions: # this is to try all diagonal jump directions
            
            # square containing the opponent piece (must exist)
            middle_row = row + delta_row
            middle_col =  col + delta_col

            





