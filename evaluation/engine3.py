import chess

class ChessEngine:
    eval_info = "rewarding: piece counting, central pawn control, king safety, mobility"
    search_info = "minimax search with depth 3."

    def __init__(self):
        self.depth = 3  
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
        Evaluates the board using material counting, positional factors, 
        and additional penalties to avoid repetitive moves.
        """
        if board.is_checkmate():
            return 1000 if board.turn == chess.BLACK else -1000
        elif board.is_stalemate() or board.is_insufficient_material():
            return 0 

        value = self.evaluate_material(board)
        value += self.evaluate_piece_positioning(board)
        value += self.evaluate_king_safety(board)
        value += self.evaluate_mobility(board)

        repetition_count = self.previous_boards.count(board)
        if repetition_count > 1:
            value -= repetition_count * 0.5  

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

    def evaluate_piece_positioning(self, board):
        """
        Evaluates the piece activity using bitmaps for each piece
        """
        piece_square_table = {
            chess.PAWN: [
                0, 0, 0, 0, 0, 0, 0, 0,
                5, 10, 10, -20, -20, 10, 10, 5,
                5, -5, -10, 0, 0, -10, -5, 5,
                0, 0, 0, 20, 20, 0, 0, 0,
                5, 5, 10, 25, 25, 10, 5, 5,
                10, 10, 20, 30, 30, 20, 10, 10,
                50, 50, 50, 50, 50, 50, 50, 50,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
            # TODO for other pieces
        }
        position_value = 0
        for piece_type in piece_square_table:
            for square in board.pieces(piece_type, chess.WHITE):
                position_value += piece_square_table[piece_type][square]
            for square in board.pieces(piece_type, chess.BLACK):
                position_value -= piece_square_table[piece_type][square]
        return position_value

    def evaluate_king_safety(self, board):
        """
        Punishment for being in check
        """
        safety_value = 0
        if board.is_check():
            safety_value -= 50 if board.turn == chess.WHITE else -50
        return safety_value

    def evaluate_mobility(self, board):
        """
        Rewarding for having more legal moves available
        """
        mobility_value = len(list(board.legal_moves))
        return mobility_value if board.turn == chess.WHITE else -mobility_value