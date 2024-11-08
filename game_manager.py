import chess
import sys
import os
import pygame
from engine_manager import EngineManager
from result_tracker import ResultTracker
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'visualisation')))
import vis_board

class GameManager:
    def __init__(self, white_engine_id, black_engine_id, num_games):
        self.white_engine_id = white_engine_id
        self.black_engine_id = black_engine_id
        self.num_games = num_games
        self.engine_manager = EngineManager()
        self.result_tracker = ResultTracker()
        self.pieces = vis_board.build_pieces()
        vis_board.build_squares() 

    def run(self):
        """
        Runs n games between two engines. Asks each engine for a move and plays it. 
        Calls vis_board to display the current position.
        After all games are played displays the stats and information about the two engines.
        """
        for game_number in range(1, self.num_games + 1):
            print(f"Starting game {game_number}")
            game = chess.Board()

            # Initialize engines
            white_engine = self.engine_manager.load_engine(self.white_engine_id)
            black_engine = self.engine_manager.load_engine(self.black_engine_id)
            current_turn = white_engine  # White starts

            while not game.is_game_over():
                # Get move from engine and play it
                move = current_turn.get_best_move(game)
                game.push(move)
                
                # Diplay new position uncomment prints to get game in ASCII
                fen_position = game.fen().split()[0]
                vis_board.update_board(fen_position, self.pieces)  # Pass the FEN to the visualizer  
                pygame.time.delay(100)

                #print(game)
                #print("---------------")

                current_turn = black_engine if current_turn == white_engine else white_engine

            # Track the result of the current game
            self.result_tracker.record_game_result(game, self.white_engine_id, self.black_engine_id)
            print(f"Game {game_number} result: {game.result()}")

        # Print the result and information about the engines
        self.result_tracker.print_summary(self.num_games, self.white_engine_id, self.black_engine_id)
        print ("\n")
        print ("White engine:")
        print ("-> Evaluation used: ", white_engine.eval_info)
        print ("-> SearchAlgo used: ", white_engine.search_info)
        print ("\n")
        print ("Black engine:")
        print ("-> Evaluation used: ", black_engine.eval_info)
        print ("-> SearchAlgo used: ", black_engine.search_info)


