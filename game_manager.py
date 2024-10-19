import chess
import chess.pgn
from engine_manager import EngineManager
from result_tracker import ResultTracker

class GameManager:
    def __init__(self, white_engine_id, black_engine_id, num_games):
        self.white_engine_id = white_engine_id
        self.black_engine_id = black_engine_id
        self.num_games = num_games
        self.engine_manager = EngineManager()
        self.result_tracker = ResultTracker()

    def run(self):
        for game_number in range(1, self.num_games + 1):
            print(f"Starting game {game_number}")
            game = chess.Board()

            white_engine = self.engine_manager.load_engine(self.white_engine_id)
            black_engine = self.engine_manager.load_engine(self.black_engine_id)

            current_turn = white_engine  # White starts

            while not game.is_game_over():
                print(game)
                print("---------------")
                move = current_turn.get_best_move(game)
                game.push(move)
                current_turn = black_engine if current_turn == white_engine else white_engine

            self.result_tracker.record_game_result(game, self.white_engine_id, self.black_engine_id)
            print(f"Game {game_number} result: {game.result()}")

        self.result_tracker.print_summary(self.num_games, self.white_engine_id, self.black_engine_id)
        print ("\n")
        print ("White engine:")
        print ("-> Evaluation used: ", white_engine.eval_info)
        print ("-> SearchAlgo used: ", white_engine.search_info)
        print ("\n")
        print ("Black engine:")
        print ("-> Evaluation used: ", black_engine.eval_info)
        print ("-> SearchAlgo used: ", black_engine.search_info)


