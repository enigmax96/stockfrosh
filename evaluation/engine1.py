import chess
import random

class ChessEngine:
    eval_info = "plays a random legal move."
    search_info = "no search used."
    def get_best_move(self, board):
        '''
        Play a random legal move
        '''
        legal_moves = list(board.legal_moves)
        return random.choice(legal_moves)
