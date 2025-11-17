from game_state import gamestate, BLACK
from board_game import create_initial_board, print_board_game
from board_moves import get_simple_moves, get_capture_moves, get_legal_moves, apply_move
from minimax_algorithm import get_best_move


def create_initial_state():

    board_game = create_initial_board()
    return gamestate(board_game, BLACK)

def parse_human_move(move_string):
    # this will convert user input like :
    # "2 1 3 2 "
    # 2 1 4 3 6 5 

    # into moves [(2, 1), (3, 2)]
    # [(2, 1), (4, 3), (6, 5)]

    try: 
        numbers = list(map(int, move_string.split())) # split input into integers 

    except ValueError:
        return None # invalid inut such as "r1", letters , symbols


    # A valid move must have:
    # at least 4 numbers, and an even amount of numbers (pairs)

    if len(numbers) < 4 or len(numbers) % 2 !=0:
        return None # invalid format --> returns nothing
    
    
    move = []
    # convert each pair (r, c) into a tuple
    for i in range(0, len(numbers), 2):
        move.append((numbers[i], numbers[i+1]))

    return move #return the move sequence list


def print_legal_moves(moves):
    # pretty prints all available legal moves for the current player

    if len(moves) == 0:
        print("   No legal moves")
        return
    

    print("Legal moves:")

    for m in moves:
        print("   ", m)




if __name__ == "__main__":

    print("Creating intial board environment...")
    state = create_initial_state()

    print("WELCOME TO CHECKERS — HUMAN (WHITE) VS AI (BLACK)")
    print("--------------------------------------------------")


    while True:


        print("Printing board game environment...")
        print_board_game(state)

        legal_moves =get_legal_moves(state)

        if len(legal_moves) ==0:
            print("\nGAME OVER!")

            if state.current_player == BLACK:
                print("WHITE wins!")
            else:
                print("BLACK wins!")

            break # this will exit the loop --> end the game

        print()
        print_legal_moves(legal_moves)
        print()
        
        # if no legal moves --> game is over

        #AI TURN (BLACK)

        if state.current_player == BLACK:
            print("AI (BLACK) is thinking...")

            # run minimax to the best move
            best_move = get_best_move(state, depth=4)

            print("AI chooses:", best_move)

            # apply the AI move
            state = apply_move(state, best_move)
            continue    # this will skip to the next turn


    # ==============================================================
    # HUMAN TURN (WHITE)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        else:
            print("Your turn (WHITE). Enter move as: r1 c1 r2 c2 ....")

            input_string = input("ENTER your move: ")

            human_move = parse_human_move(input_string)

            # validate human input

            if human_move is None:
                print("Invalid format. Try Again!")
                continue

            if human_move not in legal_moves:
                print('Illegal move. Try Again!')
                continue

            # apply the human move:

            state = apply_move(state, human_move)


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


    print("\nLegal moves for current player (simple or captures depending on rule)")

    for move in legal_moves:
        print(move)


    