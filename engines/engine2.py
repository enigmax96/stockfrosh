import chess

class ChessEngine:
    eval_info = "rewarding: material count and checkmate/ stalemate; punishment for repeated moves."
    search_info = "minimax search with depth 4."

    def __init__(self):
        self.depth = 4  
        self.previous_boards = []  

    def get_best_move(self, board):
        best_move = None
        best_value = -float('inf') if board.turn == chess.WHITE else float('inf')

        for move in board.legal_moves:
            board.push(move)
            board_value = self.minimax(board, self.depth - 1, -float('inf'), float('inf'), not board.turn)
            board.pop()

            if (board.turn == chess.WHITE and board_value > best_value) or (board.turn == chess.BLACK and board_value < best_value):
                best_value = board_value
                best_move = move

        self.previous_boards.append(board.copy())  
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Searches the position tree recursivley until depth == 0.
        Calls evaluation for each found position 
        """
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if maximizing_player:
            max_eval = -float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval_value = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval_value)
                alpha = max(alpha, eval_value)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval_value = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_value)
                beta = min(beta, eval_value)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self, board):
        """
        Evaluates the board using material counting 
        and rewards/punishes for checkmate, stalemate, and repeated moves.
        """
        if board.is_checkmate():
            if board.turn == chess.WHITE:  # Black has checkmated white
                return -1000
            else:  # White has checkmated black
                return 1000
        elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
            return 0  # Stalemate or draw = no value

        value = self.evaluate_material(board)

        if self.previous_boards.count(board) > 1:
            value -= 0.5  

        return value

    def evaluate_material(self, board):
        """
        Material evaluation: positive for white's advantage, negative for black's.
        """
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0  # King has no material value, it's priceless
        }

        value = 0
        for piece_type in piece_values:
            value += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
            value -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

        return value
