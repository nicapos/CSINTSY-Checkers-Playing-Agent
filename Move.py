from math import sqrt, pow
import enum
from State import State

class MoveType(enum.Enum):
    SIMPLE_MOVE = "SIMPLE_MOVE",
    SINGLE_JUMP_MOVE = "SINGLE_JUMP_MOVE",
    MULTIPLE_JUMP_MOVE = "MULTIPLE_JUMP_MOVE"

class Move:
    def __init__(self, fromTile, toTile) -> None:
        self.__fromTile = fromTile
        self.__toTile = toTile

    def extend(self) -> bool:
        col = lambda x: ((x - 1) % 4) + 1
        side = lambda x : ((x - 1) // 4) % 2

        if col(self.From) == col(self.To) and col(self.From) in [1,4]:
            if col(self.From) == 1 and side(self.From) == 0:
                return False
            elif col(self.From) == 4 and side(self.From) == 1:
                return False

        piece_diagonals = [-5, -4, 3, 4] if side(self.From) else [-4, -3, 4, 5]
        non_piece_diagonals = [-5, -4, 3, 4] if not side(self.From) else [-4, -3, 4, 5]
        i = -1
        for j in range(len(piece_diagonals)):
            if (self.From + piece_diagonals[j]) == self.To:
                i = j

        newTo = self.To + non_piece_diagonals[i]

        if i == -1:
            raise Exception("No extend match found.") # DEBUG

        if (not (1 <= newTo <= 32)):
            return False

        self.__toTile = newTo
        return True

    @property
    def From(self):
        return self.__fromTile
    
    @property
    def To(self):
        return self.__toTile

    @property
    def nsteps(self): 
        row = lambda x: (x-1) // 4
        return abs(row(self.From) - row(self.To))

    def type(self) -> MoveType:
        return "SIMPLE_MOVE" if self.nsteps == 1 else "SINGLE_JUMP_MOVE" if self.nsteps == 2 else "MULTIPLE_JUMP_MOVE"

    def getPath(self): # for checkers
        if self.nsteps == 2:
            col = lambda x: ((x - 1) % 4) + 1
            side = lambda x : ((x - 1) // 4) % 2
            min_tile = min(self.From, self.To)
            max_tile = max(self.From, self.To)
            if side(self.From):
                return min_tile + 4 if col(min_tile) < col(max_tile) else min_tile + 3
            else:
                return min_tile + 5 if col(min_tile) < col(max_tile) else min_tile + 4
        else:
            return -1
            #raise Exception("Can't generate path for non-jump move")
        

    def isInBounds(self):
        return (1 <= self.To <= State.TILES) and (1 <= self.From <= State.TILES)

    def __str__(self) -> str:
        return f"{self.From} -> {self.To}" if self.nsteps == 1 else f"{self.From} -> {self.To} (path: {self.getPath()})"