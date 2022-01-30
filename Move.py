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

    def extend(self):
        delta = 1 if self.To > self.From else -1
        newTo = self.From + (((self.To-self.From) * 2) + delta)
        self.__toTile = newTo

    @property
    def From(self) -> tuple():
        return self.__fromTile
    
    @property
    def To(self) -> tuple():
        return self.__toTile

    @property
    def nsteps(self): # using distance formula
        return abs(self.From-self.To)//4

    def type(self) -> MoveType:
        return "SINGLE_MOVE" if self.nsteps == 1 else "SINGLE_JUMP_MOVE" if self.nsteps == 2 else "MULTIPLE_JUMP_MOVE"

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
            raise Exception("Can't generate path for non-jump move")
        

    def isInBounds(self):
        return (1 <= self.To <= State.TILES) and (1 <= self.From <= State.TILES)

    def __str__(self) -> str:
        return f"{self.From} -> {self.To}"