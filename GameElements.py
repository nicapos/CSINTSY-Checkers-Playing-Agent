import enum

class Player(enum.Enum):
    Human = 0
    AI = 1

class Piece(enum.Enum):
    # black pieces = AI, white pieces = HUMAN
    BLACK = 1
    BLACK_KING = 2
    WHITE = -1
    WHITE_KING = -2