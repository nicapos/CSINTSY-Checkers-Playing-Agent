from GameElements import Piece

class State:
    TILES = 32

    def __init__(self, preset_grid:list=None) -> None:
        # black pieces = AI, white pieces = HUMAN
        self.__tiles = [0 for _ in range(self.TILES)] if preset_grid == None else preset_grid
        self.last_move = None

    def get_piece(self, pos:int) -> int: # where pos = any int between 1 and 32 (inclusive)
        try:
            return self.__tiles[pos-1]
        except IndexError:
            raise Exception(f"Invalid index for get_piece. (Passed {pos})")

    def set_piece(self, pos:int, value:int): # where pos = any int between 1 and 32 (inclusive)
        try:
            self.__tiles[pos-1] = value
            return True
        except IndexError:
            raise Exception(f"Invalid index for set_piece. (Passed {pos})")

    @property
    def tiles(self):
        return self.__tiles

    @property
    def normalBlackPieces(self):
        return sum([piece == Piece.BLACK.value for piece in self.tiles])

    @property
    def blackKingPieces(self):
        return sum([piece == Piece.BLACK_KING.value for piece in self.tiles])

    @property
    def totalBlackPieces(self):
        return self.normalBlackPieces + self.blackKingPieces

    @property
    def normalWhitePieces(self):
        return sum([piece == Piece.WHITE.value for piece in self.tiles])

    @property
    def whiteKingPieces(self):
        return sum([piece == Piece.WHITE_KING.value for piece in self.tiles])

    @property
    def totalWhitePieces(self):
        return self.normalWhitePieces + self.whiteKingPieces

    def __str__(self) -> str:
        s = "\n"
        str_piece = {0: '·', Piece.BLACK.value: 'b', Piece.BLACK_KING.value: 'B', Piece.WHITE.value: 'w', Piece.WHITE_KING.value: 'W'}

        i = 1
        is_side_right = True
        while i < self.TILES:
            if is_side_right:
                s += f"{i:2}  " + ''.join([f"   {str_piece[self.get_piece(j)]}" for j in range(i, i+4)]) + "\n"
            else:
                s += f"{i:2}  " + ''.join([f" {str_piece[self.get_piece(j)]}  " for j in range(i, i+4)]) + "\n"
            i += 4
            is_side_right = not is_side_right

        return s

    def __eq__(self, __o: object) -> bool:
        if __o == None:
            return False 

        for i in range(1, self.TILES+1):
            if (self.get_piece(i) != __o.get_piece(i)):
                return False
        return True