import chess
import json
from engine_manager import EngineManager
from result_tracker import ResultTracker
import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'visualisation')))
import vis_board

class GameManager:
    def __init__(self, white_engine_id, black_engine_id, num_games, fen_file=None):
        self.white_engine_id = white_engine_id
        self.black_engine_id = black_engine_id
        self.num_games = num_games
        self.fen_positions = []
        if fen_file:
            self.load_fens_from_json(fen_file)
        self.engine_manager = EngineManager()
        self.result_tracker = ResultTracker()
        self.pieces = vis_board.build_pieces()
        vis_board.build_squares()

    def load_fens_from_json(self, fen_file):
        """
        Loads FEN positions from a provided JSON file.
        """
        with open(fen_file, 'r') as f:
            data = json.load(f)
            self.fen_positions = data.get("fens", [])
            if not self.fen_positions:
                print("No FEN positions found in JSON file.")
                sys.exit(1)

    def run(self):
        """
        Runs n games between two engines, starting each game from either a fresh position
        or from a position provided in the JSON file.
        """
        for game_number in range(1, self.num_games + 1):
            print(f"Starting game {game_number}")

            if self.fen_positions:
                # Get FEN position for this game from the list
                fen_position = self.fen_positions[(game_number - 1) % len(self.fen_positions)]  # Loop if not enough FENs
                print(f"Starting with FEN: {fen_position}")
                game = chess.Board(fen_position)  # Start from FEN position
            else:
                # Start from a fresh position
                game = chess.Board()

            # Initialize engines
            white_engine = self.engine_manager.load_engine(self.white_engine_id)
            black_engine = self.engine_manager.load_engine(self.black_engine_id)
            current_turn = white_engine  # White starts

            while not game.is_game_over():
                # Get move from engine and play it
                move = current_turn.get_best_move(game)
                game.push(move)
                
                # Display new position
                fen_position = game.fen().split()[0]
                vis_board.update_board(fen_position, self.pieces)  # Pass the FEN to the visualizer  
                pygame.time.delay(20)

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
