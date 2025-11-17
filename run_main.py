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


def choose_AI_difficulty():

    # this function decides the difficutly of the AI agent, difficulty is based on the depth of which the search algorithm would go within a tree

    print("\n Select AI Difficulty:")
    print("1) East (Depth 2)")
    print("2) Medium (Depth 4)")
    print("3) Hard (Depth 6)")

    while True:
        choice = input("Enter choice of AI difficulty (1-3):").strip()

        if choice == "1":
            return 2
        elif choice == "2":
            return 4
        
        elif choice == "3":
            return 6
        
        else:
            print("invalid AI difficulty choice, Please enter either 1, 2, or 3.")


def show_help_menu():

    print("\n ==================================== HELP MENU ==================================== ")
    print(" BASIC RULES OF CHECKERS (Assignment Version): ")
    print("   -----------------------------------------------------------------------------------")
    print("1) Checkers is played on an 8x8 board, using only the dark squares")
    print("2) the bottom right square must be a light square")
    print("3) each player starts with 12 pieces placed on the dark squares of the")
    print("first three rows on their side ")
    print("4) black always moves first in this version (maximizer)")
    print("5) a simple move is one diagonal step to an empty square")
    print()
    print("CAPTURING RULES:")
    print("6) captures are made by jumping diagonally over an opponent piece")
    print("  into the empty square directly behind it.")
    print("7) captures can only move forward for pawns.")
    print("8) if a capture is available, you MUST take it (forced capture rule).")
    print("9) if more captures are available after a jump, you must continue jumping.")
    print("10) you may choose any capture path if more than one is available.")
    print()
    print("KING PIECES:")
    print("11) a pawn becomes a king when it reaches the opponent's back row.")
    print("12) kings move diagonally in all four directions (forward and backward).")
    print("13) kings can also capture in any diagonal direction.")
    print("14) IMPORTANT: if a pawn reaches the king row DURING a capture sequence,")
    print("  the capturing ends immediately (no more jumps).")
    print()
    print("REGICIDE RULE (Assignment Rule):")
    print("15) if a pawn captures an opponent king, it becomes a king instantly.")
    print("16) this promotion happens during the jump, not at the end of the turn.")
    print("17) once regicide happens, the turn ends immediately (no additional captures).")
    print()
    print("HOW TO ENTER MOVES:")
    print("----------------------------------------------")
    print("enter moves using pairs of coordinates like this:")
    print("   r1 c1 r2 c2")
    print("example simple move:")
    print("   2 1 3 2")
    print("example multi-jump capture:")
    print("   2 1 4 3 6 5")
    print("18) you can chain as many coordinate pairs as needed for multi-jumps.")
    print()
    print("\n ==================================== HELP MENU ==================================== ")



if __name__ == "__main__":

    ai_depth = choose_AI_difficulty()


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
            best_move = get_best_move(state, depth=ai_depth)

            print("AI chooses:", best_move)

            # apply the AI move
            state = apply_move(state, best_move)
            continue    # this will skip to the next turn


    # ==============================================================
    # HUMAN TURN (WHITE)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        else:
            print("Your turn (WHITE). Enter move as: r1 c1 r2 c2 ....")
            print("Or type 'hint' to get a recommended move \n")

            input_string = input("ENTER your move: ").strip()

            human_move = parse_human_move(input_string)

            #hinting logic to be implemented below:

            if input_string.lower() == "hint":
                print("Calculating the best move for WHITE...")

                hint_move = get_best_move(state, depth = ai_depth)

                print("Suggested move: ", hint_move)
                continue

            elif input_string.lower() == "help":
                show_help_menu()


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


    