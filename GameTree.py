from State import State

NODES_GENERATED = 0

class GameTreeNode():
    def __init__(self, state:State, heuristic=None) -> None:
        self.__state = state
        self.__heuristic = heuristic
        self.__children = []

    def set_heuristic(self, val):
        self.__heuristic = val

    def add_child(self, otherGameTreeNode):
        self.__children.append(otherGameTreeNode)

    @property
    def state(self):
        return self.__state

    @property
    def heuristic(self):
        return self.__heuristic

    @property
    def children(self):
        return self.__children

    @property
    def num_children(self):
        return len(self.__children)