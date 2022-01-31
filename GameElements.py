import enum

class Player(enum.Enum):
    Human = 0
    AI = 1

class Piece(enum.Enum):
    # black pieces = AI, white pieces = HUMAN
    BLACK = "b"
    BLACK_KING = "B"
    WHITE = "w"
    WHITE_KING = "W"