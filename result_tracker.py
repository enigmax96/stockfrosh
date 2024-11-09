class ResultTracker:
    def __init__(self):
        self.results = {
            "white_wins": 0,
            "black_wins": 0,
            "draws": 0
        }

    def record_game_result(self, game, white_engine_id, black_engine_id):
        """
        Keeps track of the result for each game
        """
        result = game.result()
        if result == '1-0':
            self.results["white_wins"] += 1
        elif result == '0-1':
            self.results["black_wins"] += 1
        else:
            self.results["draws"] += 1

    def print_summary(self, num_games, white_engine_id, black_engine_id):
        """
        Prints the total result
        """
        print(f"Summary of {num_games} games between Engine {white_engine_id} (White) and Engine {black_engine_id} (Black):")
        print(f"White wins: {self.results['white_wins']}")
        print(f"Black wins: {self.results['black_wins']}")
        print(f"Draws: {self.results['draws']}")
