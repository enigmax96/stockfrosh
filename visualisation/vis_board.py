import pygame
import sys
import os
from square import Square
from piece import Piece

# Initialize Pygame
pygame.init()

# Set up constants
BOARD_SIZE = 600  # size of the chessboard in pixels
SQUARE_SIZE = BOARD_SIZE // 8
SQUARE_WHITE = pygame.Color("burlywood1")
SQUARE_BLACK = pygame.Color("burlywood4")
PIECES = {}
BOARD = []

# Set up display
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("StockFrosh")

def build_pieces():
    """
    Creates all the Pieces
    """
    piece_names = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
    for color in ['white', 'black']:
        for name in piece_names:
            image_path = os.path.join(os.path.dirname(__file__), 'images', f'{color}_{name}.png')
            PIECES[f'{color}_{name}'] = pygame.image.load(image_path)
            PIECES[f'{color}_{name}'] = pygame.transform.scale(PIECES[f'{color}_{name}'], (SQUARE_SIZE, SQUARE_SIZE))
            piece = Piece(name, color, image_path)

    return PIECES

def build_squares():
    """
    Fills the BOARD ARRAY with squares 
    """
    for rank in range(8):
        for file in range(8):
            color = "white" if (rank + file) % 2 == 0 else "black"
            square = Square(SQUARE_WHITE if (rank + file) % 2 == 0 else SQUARE_BLACK, color, rank, file)
            BOARD.append(square)

def draw_board():
    """
    Draws the chessboard using all squares from BOARD
    """
    for square in BOARD:
        # Draw each square
        file_index = ["a", "b", "c", "d", "e", "f", "g", "h"].index(square.file)
        rank_index = ["8", "7", "6", "5", "4", "3", "2", "1"].index(square.rank)
        
        pygame.draw.rect(screen, square.print_color, (file_index * SQUARE_SIZE, rank_index * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Draw square labels on outer squares
        font = pygame.font.SysFont(None, 24)
        if rank_index == 7:  # Bottom rank labels (a-h)
            text = font.render(square.file, True, (0, 0, 0))
            screen.blit(text, (file_index * SQUARE_SIZE + 2, (rank_index + 1) * SQUARE_SIZE - text.get_height() - 2))
        if file_index == 7:  # Right file labels (1-8)
            text = font.render(square.rank, True, (0, 0, 0))
            screen.blit(text, ((file_index + 1) * SQUARE_SIZE - text.get_width() - 2, rank_index * SQUARE_SIZE + 2))


def place_pieces_from_fen(fen, pieces):
    """
    Places pieces on the board according to given FEN notation.
    """
    ranks = fen.split()[0].split("/")
    piece_map = {
        'r': 'black_rook', 'n': 'black_knight', 'b': 'black_bishop', 'q': 'black_queen', 'k': 'black_king', 'p': 'black_pawn',
        'R': 'white_rook', 'N': 'white_knight', 'B': 'white_bishop', 'Q': 'white_queen', 'K': 'white_king', 'P': 'white_pawn'
    }

    for rank_index, rank in enumerate(ranks):
        file_index = 0
        for char in rank:
            if char.isdigit():
                file_index += int(char)  # Empty squares
            else:
                piece_name = piece_map[char]
                screen.blit(pieces[piece_name], (file_index * SQUARE_SIZE, rank_index * SQUARE_SIZE))
                file_index += 1

def update_board(fen, pieces):
    """
    Updates the Board with the given FEN
    """
    screen.fill(pygame.Color("black")) 
    draw_board()                        
    place_pieces_from_fen(fen, pieces)  
    pygame.display.flip()              

'''
def main():
    build_squares()
    build_pieces()
    draw_board()
    #fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    fen = "r7/p4ppp/1q4kb/2pQ1b2/B1P1pP1P/3R2N1/PP2PKPP/Rr1p1B2"
    place_pieces_from_fen(fen, pieces)
    pygame.display.flip()
    
    # Event loop to keep the window open
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
'''