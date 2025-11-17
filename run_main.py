from game_state import gamestate, BLACK
from board_game import create_initial_board, print_board_game
from board_moves import get_simple_moves, get_capture_moves, get_legal_moves

def create_initial_state():

    board_game = create_initial_board()
    return gamestate(board_game, BLACK)





if __name__ == "__main__":

    print("Creating intial board environment...")
    state = create_initial_state()

    print("Printing board game environment...")
    print_board_game(state)

    print("\nCurrent player:", state.current_player)


    # this gives the simple moves
    simple_moves = get_simple_moves(state)
    print("\nSimple moves for current player:")
    for move in simple_moves:
        print(move) # prints each individual move

    # capture moves 
    captures_moves = get_capture_moves(state)
    print("\nCapture moves for current player:")

    for move in captures_moves:
        print(move)

    # legal moves (forced capture rule)

    legal_moves =get_legal_moves(state)

    print("\nLegal moves for current player (simple or captures depending on rule)")

    for move in legal_moves:
        print(move)


    