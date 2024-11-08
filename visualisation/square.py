class Square:
    def __init__(self, print_color, color, rank, file, piece=None):
        self.print_color = print_color # only visual, the color, that is printed on the board
        self.color = color # white or black
        self.rank = ["8", "7", "6", "5", "4", "3", "2", "1"][rank]
        self.file = ["a", "b", "c", "d", "e", "f", "g", "h"][file]
        self.squareid = self.file + self.rank 
        self.piece = piece
  
    def __enter__(self):
        return 

    def __exit__ (self, exc_type, exc_val, exc_tb):
        return 
    
