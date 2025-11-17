from game_state import *
from board_game import is_opponents_turn

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

            # Landing square (two steps away)
            land_row = row + 2 * delta_row
            land_col = col + 2 * delta_col

            # check if the dimensions of the middle square are accesible
            if middle_row < 0 or middle_row >= 8:
                continue
            if middle_col < 0 or middle_col >= 8:
                continue

            # check if the dimensions of the landing square are accesible
            if land_row < 0 or land_row >= 8:
                continue
            if land_col < 0 or land_col >= 8:
                continue


            middle_piece = board_state[middle_row][middle_col]

            landing_piece = board_state[land_row][land_col]

            # to jump:

            # -- middle square must hold an opponent
            # landing square must be empty
            

            if is_opponents_turn(middle_piece, player) and landing_piece == EMPTY:
                found_jump = True

                if piece == BLACK_PAWN and land_row == 7:
                    capture_sequences.append(path + [(land_row, land_col)])
                    continue

                if piece == WHITE_PAWN and land_row == 0:
                    capture_sequences.append(path + [(land_row, land_col)])
                    continue 

                #simulate the jump on a copy of the board (so that we can print later)
                new_board = [row_copy[:] for row_copy in board_state]

                #remove from original position
                new_board[row][col] = EMPTY

                # remove the captured opponent
                new_board[middle_row][middle_col] = EMPTY

                #place players piece at the landing position
                new_board[land_row][land_col] = piece

                # continue to explore further jumps from the new position
                new_path = path + [(land_row, land_col)]
                dfs(new_path, land_row, land_col, new_board)


        # if no more jumps have been found from here, and we actually moved at least once, then 
        # this path is fully discovered
        if not found_jump and len(path) > 1:
            capture_sequences.append(path)


    # we start DFS from the original position
    dfs([(row, col)], row, col, board)

    return capture_sequences


def get_capture_moves(state):
    board = state.board_layout
    player = state.current_player

    # return a list of all capture sequences availble to the current player

    all_captures = []

    for row in range(8):
        for col in range(8):
            piece = board[row][col]


            # only search capture moves in pieces that belong to the current player
            if player == BLACK and piece in (BLACK_PAWN, BLACK_KING):
                all_captures.extend(capture_moves_for_piece(board, row, col, piece, player))

            elif player == WHITE and piece in (WHITE_PAWN, WHITE_KING):
                all_captures.extend(capture_moves_for_piece(board, row, col, piece, player))

    return all_captures


def get_legal_moves(state):

    # this returns all legal moves for the current player.

    #RULE:

    # if any "capture" is available --> you MUST "capture"
    # Otherwise, normal simple moves are allowed.


    captures = get_capture_moves(state)

    if captures:
        return captures # you are forced to capture
    
    else:
        return get_simple_moves(state) # you are allowed to make a decision
    
# the following function will allow the player to apply moves to the board

def apply_move(state, move):

    # apply a move to the board, and return a NEW gamestate object

    #move = [(r1, c1), (r2, c2), ... ] (rn, cn)

    # simple moves (2 coordinates)

    # multijump capture sequences (3+ coordinates)


    board = [row[:] for row in state.board_layout] # take a deepcopy of the environment

    player = state.current_player #this selectes the current player

    start_row, start_col = move[0] # the starting square of the piece
    piece = board[start_row][start_col] #identify the moving piece 

    board[start_row][start_col] = EMPTY #remove the piece fom its starting square


    # flag for immediate king promotion (regicide)
    regicide_trigger = False


    #process all segments of the move
    # handle captures for jumps

    for i in range(len(move) - 1): # loop through each step in the move
        row1, col1 = move[i] # current position
        row2, col2 = move[i + 1] # next position

        # if it's a jump (difference of 2 rows), then a capture happened

        if abs(row2 - row1) == 2: # jumps always move 2 squares 
            middle_row = (row1 + row2) // 2 #middle square row (piece being captured) 
            middle_col = (col1 + col2) // 2 #middle square column for piece being captured

            captured_piece = board[middle_row][middle_col]

            board[middle_row][middle_col] = EMPTY # remove the captured opponent piece


            # this is the regicide rule's logic, where if a pawn captures a king --> becomes king immediately
            if captured_piece in (BLACK_KING, WHITE_KING):
                if piece in (BLACK_PAWN, WHITE_PAWN):
                    regicide_trigger = True 


        # move the piece to the next square in the sequence

        board[row2][col2] = piece
        board[row1][col1] = EMPTY

        # if a regicide has happened, no further jumps are allowed
        if regicide_trigger:
            break


    # at this point the move path is finished (or stopped early because of regicide)
    final_row, final_col = move[i + 1]


    # if a pawn captured a king --> promote instantly
    if regicide_trigger:

        print("REGICIDE ACTIVATED!")
        
        if piece == BLACK_PAWN:
            piece = BLACK_KING

        elif piece == WHITE_PAWN:
            piece = WHITE_KING

        board[final_row][final_col] = piece


    else:
        # normal end-of-turn promotion (the back row)
        if piece == BLACK_PAWN and final_row == 7:
            piece = BLACK_KING

        elif piece == WHITE_PAWN and final_row == 0:
            piece = WHITE_KING

        board[final_row][final_col] = piece


    # switch the active player
    next_player = WHITE if player == BLACK else BLACK

    # return the new GameState object, to progress the game
    return gamestate(board, next_player)
