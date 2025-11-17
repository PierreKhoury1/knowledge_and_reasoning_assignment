# this script will define the minimax search tree algorithm within the checkers game


from math import inf
from board_moves import get_legal_moves, apply_move
from evaluation import evaluate_state


def minimax(state, depth, alpha, beta, maximizing_player):

    # minimax search WITH alpha-beta pruning.
    # will return the evaluation score of the state


    legal_moves = get_legal_moves(state) #terminal condition: depth reached OR no legal moves

    if depth == 0 or len(legal_moves) == 0:
        return evaluate_state(state)
    
    #maximizing player = BLACK (because evaluation is from the BLACK's perspective)
    if maximizing_player:
        max_eval = -inf

        for move in legal_moves:

            #apply the move to generate successor state
            new_state = apply_move(state, move)

            # recursive minimax call (Switch to minimizaing player)
            evaluation_value = minimax(new_state, depth -1, alpha, beta, False)

            #update the best score

            max_eval = max(max_eval, evaluation_value)

            # update alpha
            alpha = max(alpha, evaluation_value)

            # alpha-beta pruning

            if beta<= alpha:
                break
        return max_eval
    
    #minimizing player = WHITE

    else:
        min_eval = inf

        for move in legal_moves:
            new_state = apply_move(state, move)


            #switch back to maximizing
            evaluation_value = minimax(new_state, depth - 1, alpha, beta, True)

            min_eval = min(min_eval, evaluation_value)

            # update beta

            beta = min(beta, evaluation_value)

            # prune 

            if beta <= alpha:
                break

        return min_eval
    


def get_best_move(state, depth):
    # this will return the best move of the current player.

    # if the player is BLACK --> maximizing
    # if the player WHITE --> minimizing

    legal_moves = get_legal_moves(state)

    # no legal moves ? --> game is over

    if len(legal_moves) == 0:
        #print("the game is finished")
        return None
    
    if state.current_player == 1:
        best_score = -inf # we start with a low value
        best_move = None # nothing has been picked yet

        for move in legal_moves:
            new_state = apply_move(state, move) # this will apply the move --> new state
            score = minimax(new_state, depth- 1, -inf, inf, False) # this will evaluate the state using minimax

            # if this move is better, then store it
            if score > best_score:
                best_score = score
                best_move = move

        return best_move
    

    else: # white is minimizing
        best_score = inf # we start with a high value
        best_move = None

        for move in legal_moves:
            new_state = apply_move(state, move)
            score = minimax(new_state, depth-1, -inf, inf, True) # the black maximizes next


            if score < best_score:
                best_score = score
                best_move = move

        return best_move
    

