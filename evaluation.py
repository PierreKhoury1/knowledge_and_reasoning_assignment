#this is where the evaluation function will be implemented

from game_state import BLACK_PAWN, WHITE_PAWN, BLACK_KING, WHITE_KING


def evaluate_state(state):

    # this will evaluate the board position from BLACK's perspective 

    # a positive socre means the position is good for BLACK.
    # a negetive score means the position is good for WHITE
    board = state.board_layout # get the 8x8 board array from the state 
    score = 0 # this will be the score that will accumalate


    # loop across all 64 squares on the board
    for row in range(8):
        for col in range(8):

            piece = board[row][col] # get the piece on this square

            # if its a BLACK PAWN , add +3 points

            if piece == BLACK_PAWN:
                score += 3

            # if its a BLACK KING, add +5 points (kings are more valuable)

            elif piece == BLACK_KING:
                score +=5

            # if its a WHITE PAWN, subtract 3 points
            elif piece == WHITE_PAWN:
                score -= 3

            # if its a WHITE KING, subtract 5 points

            elif piece == WHITE_KING:
                score -=5

    # return the final evaluation value for this board


    return score


