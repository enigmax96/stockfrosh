import chess.pgn
import zstandard as zstd
import io
import os

ZST_FILE_PATH = "/home/max/stockfrosh/fen_generation/lichess_db_standard_rated_2013-01.pgn.zst"
OUTPUT_PATH = f"fens_from_{os.path.basename(ZST_FILE_PATH)}.txt"  

def extract_fen_from_zst(ZST_FILE_PATH, OUTPUT_PATH):
    """
    Runs through every game from provided pgn.zst file and plays 10 moves. 
    Safes the fen of the position to a txt file.
    If the game has less than 10 mioves safe the fen of the last move.
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

            with open(OUTPUT_PATH, "w") as fen_file:
                game_count = 0 

                # Process each PGN game in the decompressed content
                while True:
                    game = chess.pgn.read_game(pgn_file)
                    if game is None:
                        break  # End of file

                    board = game.board()
                    move_count = 0

                    # Play through the moves until we reach the 10th move or the game ends
                    for move in game.mainline_moves():
                        board.push(move)
                        move_count += 1
                        if move_count == 10:
                            fen_file.write(board.fen() + "\n")  # Write the FEN after the 10th move
                            break
                    else:
                        # If the loop completes without breaking (i.e., game ended before move 10)
                        if move_count < 10:
                            fen_file.write(board.fen() + "\n")  # Write the FEN from the last move

                    game_count += 1
                    print(f"Processed game {game_count}")

    print(f"FEN extraction after move 10 completed. Output saved to {OUTPUT_PATH}")





extract_fen_from_zst(ZST_FILE_PATH, OUTPUT_PATH)
