from State import State

class GameTreeNode():
    NODES_GENERATED = 0

    def __init__(self, state:State, heuristic=None) -> None:
        self.state = state
        self.heuristic = heuristic
        self.children = []
        GameTreeNode.NODES_GENERATED += 1

    def set_heuristic(self, v):
        self.heuristic = v

    def add_child(self, otherGameTreeNode):
        self.children.append(otherGameTreeNode)

    def clear_heuristic(self):
        self.heuristic = None

    def clear_all_heuristic(self):
        self.clear_heuristic()
        for child in self.children():
            child.clear_all_heuristic()

    @property
    def num_children(self):
        return len(self.children)