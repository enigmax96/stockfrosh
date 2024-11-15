import chess.pgn
import zstandard as zstd
import io
import os
import json
import sys

def extract_fen_from_zst(ZST_FILE_PATH, OUTPUT_PATH):
    """
    Extracts the FEN from each game in the provided PGN.zst file.
    Saves the FEN to a JSON file. If the game has fewer than 10 moves, saves the FEN of the last move.
    """
    # Open the .zst file with zstandard
    with open(ZST_FILE_PATH, "rb") as compressed_file:
        # Decompress the zst file on the fly
        dctx = zstd.ZstdDecompressor()
        
        # Use a text stream to read the decompressed PGN data
        with dctx.stream_reader(compressed_file) as reader:
            # Decode the binary stream into a string
            pgn_text = reader.read().decode("utf-8")

            # Create a file-like object from the decoded string
            pgn_file = io.StringIO(pgn_text)

            # Initialize a list to store the FENs
            fen_list = []
            game_count = 0

            # Process each PGN game 
            while True:
                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    break  

                board = game.board()
                move_count = 0

                # Play through the moves until we reach the 10th move or the game ends
                for move in game.mainline_moves():
                    board.push(move)
                    move_count += 1
                    if move_count == 10:
                        fen_list.append(board.fen())  
                        break
                else:
                    # Append latest FEN, if Game has less than 10 moves
                    if move_count < 10:
                        fen_list.append(board.fen())  

                game_count += 1
                print(f"Processed game {game_count}")

    with open(OUTPUT_PATH, "w") as json_file:
        json.dump(fen_list, json_file, indent=4)

    print(f"FEN extraction completed. Output saved to {OUTPUT_PATH}")

import os
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_pgn.zst>")
        sys.exit(1)

    ZST_FILE_PATH = sys.argv[1]
    dir_path = os.path.dirname(ZST_FILE_PATH)
    OUTPUT_PATH = os.path.join(dir_path, f"fens_from_{os.path.basename(ZST_FILE_PATH)}.json")

    extract_fen_from_zst(ZST_FILE_PATH, OUTPUT_PATH)

