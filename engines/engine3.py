import chess

#TODO white shuffles, black doesnt
class ChessEngine:
    eval_info = "rewarding: piece counting, piece placement, king safety, mobility"
    search_info = "minimax search with alpha beta pruning, depth 3."

    def __init__(self):
        self.depth = 3    

    def get_best_move(self, board):
        best_move = None
        best_value = -float('inf') if board.turn == chess.WHITE else float('inf')
        self.positions_searched = 0  

        for move in board.legal_moves:
            board.push(move)
            board_value = self.minimax(board, self.depth - 1, -float('inf'), float('inf'), not board.turn)
            board.pop()

            if (board.turn == chess.WHITE and board_value > best_value) or (board.turn == chess.BLACK and board_value < best_value):
                best_value = board_value
                best_move = move

                
        if board.fullmove_number < 7:
            print ("opening")
        elif not is_endgame:
            print ("middlegame")
        else:
            print ("endgame")
        print(f"Best move found for  {'white' if board.turn == chess.WHITE else 'black'}: {best_value}")
        print(f"Positions searched: {self.positions_searched}") 
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Searches the position tree recursively until depth == 0.
        Calls evaluation for each found position 
        """
        if depth == 0 or board.is_game_over():
            self.positions_searched += 1  
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
        #value += self.evaluate_king_safety(board)
        #value += self.evaluate_mobility(board)

        return value

    def evaluate_material(self, board):
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

        value = 0
        for piece_type in piece_values:
            value += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
            value -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

        return value

    def count_material(self, board):
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        material_count = 0

        for piece_type in piece_values:
            material_count += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
            material_count += len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

        return material_count


    def evaluate_piece_positioning(self, board):
        piece_square_table_opening = {
            chess.PAWN: [
                0,  0,  0,  0,  0,  0,  0,  0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5,  5, 10, 25, 25, 10,  5,  5,
                0,  0,  0, 20, 20,  0,  0,  0,
                5, -5,-10,  0,  0,-10, -5,  5,
                5, 10, 10,-20,-20, 10, 10,  5,
                0,  0,  0,  0,  0,  0,  0,  0
            ],
            chess.KNIGHT: [
                -20, -10, -5, -5, -5, -5, -10, -20,
                -10,   0,  5, 10, 10,  5,   0, -10,
                -5,   5, 15, 20, 20, 15,   5,  -5,
                -5,  10, 20, 30, 30, 20,  10,  -5,
                -5,  10, 20, 30, 30, 20,  10,  -5,
                -5,   5, 15, 20, 20, 15,   5,  -5,
                -10,  0,  5, 10, 10,  5,   0, -10,
                -20, -10, -5, -5, -5, -5, -10, -20
            ],
            chess.BISHOP: [
                -10, -5, -5, -5, -5, -5, -5, -10,
                -5,  10,  0,  0,  0,  0, 10,  -5,
                -5,  0, 10, 15, 15, 10,  0,  -5,
                -5,  5, 15, 20, 20, 15,  5,  -5,
                -5, 10, 10, 20, 20, 10, 10,  -5,
                -5, 15, 10, 10, 10, 10, 15,  -5,
                -5,  5,  0,  0,  0,  0,  5,  -5,
                -10, -5, -5, -5, -5, -5, -5, -10,
            ],
            chess.ROOK: [
                0,  0,  5, 10, 10,  5,  0,  0,
                0,  5, 10, 15, 15, 10,  5,  0,
                0,  5, 10, 15, 15, 10,  5,  0,
                0,  5, 10, 15, 15, 10,  5,  0,
                0,  5, 10, 15, 15, 10,  5,  0,
                0,  5, 10, 15, 15, 10,  5,  0,
                0,  0,  5, 10, 10,  5,  0,  0,
                0,  0,  5, 10, 10,  5,  0,  0
            ],
            chess.QUEEN: [
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10,   0,  0,  0,  0,   0,   0, -10,
                -10,   0,  5,  5,  5,   5,   0, -10,
                -5,    0,  5,  5,  5,   5,   0,  -5,
                -5,    0,  5,  5,  5,   5,   0,  -5,
                -10,   5,  5,  5,  5,   5,   0, -10,
                -10,   0,  5,  0,  0,   0,   0, -10,
                -20, -10, -10, -5, -5, -10, -10, -20
            ],
            chess.KING: [
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                20,  30,  10,   0,   0,  10,  30,  20,
                20,  40,  20,   0,   0,  20,  40,  20
            ]
        }

        piece_square_table_middlegame = {
            chess.PAWN: [
                0,  0,  0,  0,  0,  0,  0,  0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5,  5, 10, 25, 25, 10,  5,  5,
                0,  0,  0, 20, 20,  0,  0,  0,
                5, -5,-10,  0,  0,-10, -5,  5,
                5, 10, 10,-20,-20, 10, 10,  5,
                0,  0,  0,  0,  0,  0,  0,  0
            ],
            chess.KNIGHT: [
                -50,-40,-30,-30,-30,-30,-40,-50,
                -40,-20,  0,  0,  0,  0,-20,-40,
                -30,  0, 10, 15, 15, 10,  0,-30,
                -30,  5, 15, 20, 20, 15,  5,-30,
                -30,  0, 15, 20, 20, 15,  0,-30,
                -30,  5, 10, 15, 15, 10,  5,-30,
                -40,-20,  0,  5,  5,  0,-20,-40,
                -50,-40,-30,-30,-30,-30,-40,-50
            ],
            chess.BISHOP: [
                -20,-10,-10,-10,-10,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5, 10, 10,  5,  0,-10,
                -10,  5,  5, 10, 10,  5,  5,-10,
                -10,  0, 10, 10, 10, 10,  0,-10,
                -10, 10, 10, 10, 10, 10, 10,-10,
                -10,  5,  0,  0,  0,  0,  5,-10,
                -20,-10,-10,-10,-10,-10,-10,-20,
            ],
            chess.ROOK: [
                0,  0,  0,  0,  0,  0,  0,  0,
                5, 10, 10, 10, 10, 10, 10,  5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                0,  0,  0,  5,  5,  0,  0,  0
            ],
            chess.QUEEN: [
                0,  0,  0,  0,  0,  0,  0,  0,
                5, 10, 10, 10, 10, 10, 10,  5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                0,  0,  0,  5,  5,  0,  0,  0
            ],
            chess.KING: [
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -20,-30,-30,-40,-40,-30,-30,-20,
                -10,-20,-20,-20,-20,-20,-20,-10,
                20, 20,  0,  0,  0,  0, 20, 20,
                20, 30, 10,  0,  0, 10, 30, 20
            ]
        }

        piece_square_table_endgame = {
            chess.PAWN: [
                0,   0,   0,   0,   0,   0,   0,   0,
                5,  10,  10, -20, -20,  10,  10,   5,
                5,  -5, -10,   0,   0, -10,  -5,   5,
                0,   0,   0,  20,  20,   0,   0,   0,
                5,   5,  10,  25,  25,  10,   5,   5,
                10, 10,  20,  30,  30,  20,  10,  10,
                50, 50,  50,  50,  50,  50,  50,  50,
                0,   0,   0,   0,   0,   0,   0,   0
            ],
            chess.KNIGHT: [
                -50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20,   0,   0,   0,   0, -20, -40,
                -30,   0,  10,  15,  15,  10,   0, -30,
                -30,   5,  15,  20,  20,  15,   5, -30,
                -30,   0,  15,  20,  20,  15,   0, -30,
                -40, -20,   0,   5,   5,   0, -20, -40,
                -50, -40, -30, -30, -30, -30, -40, -50,
                -50, -40, -30, -30, -30, -30, -40, -50
            ],
            chess.BISHOP: [
                -20, -10, -10, -10, -10, -10, -10, -20,
                -10,   5,   0,   0,   0,   0,   5, -10,
                -10,  10,  10,  10,  10,  10,  10, -10,
                -10,  10,  10,  10,  10,  10,  10, -10,
                -10,   5,  10,  10,  10,  10,   5, -10,
                -10,   0,   5,  10,  10,   5,   0, -10,
                -10,   0,   0,   0,   0,   0,   0, -10,
                -20, -10, -10, -10, -10, -10, -10, -20
            ],
            chess.ROOK: [
                0,   0,   0,   5,   5,   0,   0,   0,
                -5,   0,   0,   0,   0,   0,   0,  -5,
                -5,   0,   0,   0,   0,   0,   0,  -5,
                -5,   0,   0,   0,   0,   0,   0,  -5,
                5,  10,  10,  10,  10,  10,  10,   5,
                0,   0,   0,   5,   5,   0,   0,   0,
                5,   5,  10,  10,  10,  10,   5,   5,
                0,   0,   0,   0,   0,   0,   0,   0
            ],
            chess.QUEEN: [
                -5,  -5,  -5,  -5,  -5,  -5,  -5,  -5,
                0,   0,   0,   0,   0,   0,   0,   0,
                5,   5,   5,   5,   5,   5,   5,   5,
                5,   5,   5,   5,   5,   5,   5,   5,
                10,  10,  10,  10,  10,  10,  10,  10,
                10,  10,  10,  10,  10,  10,  10,  10,
                20,  20,  20,  20,  20,  20,  20,  20,
                0,   0,   0,   0,   0,   0,   0,   0
            ],
            chess.KING: [
                20,  30,  10,   0,   0,  10,  30,  20,
                20,  20,   0,   0,   0,   0,  20,  20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30
            ]
        }


        value = 0
        is_opening = board.fullmove_number < 7
        is_endgame =  self.count_material(board) < 20
        if is_opening:
            for piece_type, table in piece_square_table_opening.items():
                for square in board.pieces(piece_type, chess.WHITE):
                    value += table[square]
                for square in board.pieces(piece_type, chess.BLACK):
                    mirrored_square = 63 - square
                    value -= table[mirrored_square]
        elif not is_endgame:
             for piece_type, table in piece_square_table_middlegame.items():
                for square in board.pieces(piece_type, chess.WHITE):
                    value += table[square]
                for square in board.pieces(piece_type, chess.BLACK):
                    mirrored_square = 63 - square
                    value -= table[mirrored_square]
        else:
            for piece_type, table in piece_square_table_endgame.items():
                for square in board.pieces(piece_type, chess.WHITE):
                    value += table[square]
                for square in board.pieces(piece_type, chess.BLACK):
                    mirrored_square = 63 - square
                    value -= table[mirrored_square]
        return value 

    def evaluate_king_safety(self, board):
        king_pos = board.king(chess.WHITE)
        if king_pos:
            row, col = divmod(king_pos, 8)
            if row >= 6:  
                return 0.5
        king_pos = board.king(chess.BLACK)
        if king_pos:
            row, col = divmod(king_pos, 8)
            if row <= 1:
                return -0.5
        return 0

    def evaluate_mobility(self, board):
        return (len(list(board.legal_moves)) / 10) if board.turn == chess.WHITE else -(len(list(board.legal_moves)) / 10)
