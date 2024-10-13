import chess
import random

class ChessEngine:
    def get_best_move(self, board):
        legal_moves = list(board.legal_moves)
        return random.choice(legal_moves)
