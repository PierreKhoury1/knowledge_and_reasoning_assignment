from game_state import gamestate, BLACK
from board_game import create_initial_board, print_board_game
from board_moves import get_simple_moves

def create_initial_state():

    board_game = create_initial_board()
    return gamestate(board_game, BLACK)





if __name__ == "__main__":

    print("Creating intial board environment...")
    state = create_initial_state()

    print("Printing board game environment...")
    print_board_game(state)

    print("\nCurrent player:", state.current_player)

    simple_moves = get_simple_moves(state)
    print("\nSimple moves for current player:")
    for move in simple_moves:
        print(move)