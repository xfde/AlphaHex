from gamestate import gamestate
from math import sqrt, log


class node:
    def __init__(self, move=None, parent=None):
        self.move = move
        self.parent = parent
        self.N = 0  # times this position was visited
        self.Q = 0  # average reward (wins-losses) from this position
        self.children = []
        self.outcome = gamestate.PLAYERS["none"]

    def add_children(self, children):
        self.children += children

    def set_outcome(self, outcome):
        self.outcome = outcome

    def value(self, explore):
        # unless explore is set to zero, maximally favor unexplored nodes
        if (self.N == 0):
            if (explore == 0):
                return 0
            else:
                return float('inf')
        else:
            return self.Q / self.N + explore * sqrt(
                2 * log(self.parent.N) / self.N)


class rave_node(node):

    def __init__(self, move=None, parent=None):
        self.move = move
        self.parent = parent
        self.N = 0  # times this position was visited
        self.Q = 0  # average reward (wins-losses) from this position
        self.Q_RAVE = 0  # times this move has been critical in a rollout
        self.N_RAVE = 0  # times this move has appeared in a rollout
        self.children = {}
        self.outcome = gamestate.PLAYERS["none"]

    def add_children(self, children):
        for child in children:
            self.children[child.move] = child

    def value(self, explore, crit):
        # unless explore is set to zero, maximally favor unexplored nodes
        if (self.N == 0):
            if (explore == 0):
                return 0
            else:
                return float('inf')
        else:
            # rave valuation:
            alpha = max(0, (crit - self.N) / crit)
            return self.Q * (1 -
                             alpha) / self.N + self.Q_RAVE * alpha / self.N_RAVE
