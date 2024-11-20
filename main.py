import sys
from game_manager import GameManager

def main():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python3 main.py <white_engine_id> <black_engine_id> <num_games> <path/to/fen_file>\n")
        print("or: python3 main.py <white_engine_id> <black_engine_id> <num_games>")
        sys.exit(1)

    white_engine_id = int(sys.argv[1])
    black_engine_id = int(sys.argv[2])
    num_games = int(sys.argv[3])
    fen_file = sys.argv[4] if len(sys.argv) == 5 else None

    game_manager = GameManager(white_engine_id, black_engine_id, num_games, fen_file)
    game_manager.run()

if __name__ == "__main__":
    main()
