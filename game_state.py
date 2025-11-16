
EMPTY      =  0
BLACK_PAWN  =  1
BLACK_KING =  2
WHITE_PAWN  = -1
WHITE_KING = -2

BLACK = 1   # black to move
WHITE = -1  # white to move

class gamestate:

    def __init__(self, board_layout, current_player):
        self.board_layout = board_layout
        self.current_player = current_player

    def copy(self):
        new_board = [row[:] for row in self.board_layout]
        return gamestate(new_board ,self.current_player)
    


