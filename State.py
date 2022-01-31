from GameElements import Piece

class State:
    TILES = 32

    def __init__(self, preset_grid:list=None) -> None:
        self.__tiles = [0 for _ in range(self.TILES)] if preset_grid == None else preset_grid
        self.action_applied = None

    def get_piece(self, pos:int) -> int:
        # where pos = any int between 1 and 32 (inclusive)
        return self.__tiles[pos-1]

    def set_piece(self, pos:int, value:int):
        # where pos = any int between 1 and 32 (inclusive)
        self.__tiles[pos-1] = value

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
        str_piece = lambda p: '·' if p == 0 else p

        is_side_right = True
        for i in range(1, self.TILES+1, 4):
            tile_format = lambda s, side_right: f"   {s}" if side_right else f" {s}  "
            s += f"{i:2}  " + ''.join([tile_format(str_piece(self.get_piece(j)), is_side_right) for j in range(i, i+4)]) + "\n"
            is_side_right = not is_side_right

        return s

    def __eq__(self, __o: object) -> bool:
        if __o == None:
            return False 
        return self.tiles == __o.tiles