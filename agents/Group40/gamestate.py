import numpy as np
from unionfind import unionfind


class gamestate:
    # dictionary associating numbers with players for book keeping
    PLAYERS = {"none": 0, "red": 1, "blue": 2}
    OPPONENT = {0: 0, 1: 2, 2: 1}
    # move value of -1 indicates the game has ended so no move is possible
    GAMEOVER = -1

    # represent edges in the union find strucure for win detection
    EDGE1 = 1
    EDGE2 = 2

    neighbor_patterns = ((-1, 0), (0, -1), (-1, 1), (0, 1), (1, 0), (1, -1))

    def __init__(self, size):
        self.size = size
        self.toplay = self.PLAYERS["red"]
        self.board = np.zeros((size, size))
        self.red_groups = unionfind()
        self.blue_groups = unionfind()

    def play(self, cell):
        if (self.toplay == self.PLAYERS["red"]):
            self.place_red(cell)
            self.toplay = self.PLAYERS["blue"]
        elif (self.toplay == self.PLAYERS["blue"]):
            self.place_blue(cell)
            self.toplay = self.PLAYERS["red"]

    def place_red(self, cell):
        if (self.board[cell] == self.PLAYERS["none"]):
            self.board[cell] = self.PLAYERS["red"]
        # if the placed cell touches a red edge connect it appropriately
        if (cell[0] == 0):
            self.red_groups.join(self.EDGE1, cell)
        if (cell[0] == self.size - 1):
            self.red_groups.join(self.EDGE2, cell)
        # join any groups connected by the new red stone
        for n in self.neighbors(cell):
            if (self.board[n] == self.PLAYERS["red"]):
                self.red_groups.join(n, cell)

    def place_blue(self, cell):
        if (self.board[cell] == self.PLAYERS["none"]):
            self.board[cell] = self.PLAYERS["blue"]
        # if the placed cell touches a blue edge connect it appropriately
        if (cell[1] == 0):
            self.blue_groups.join(self.EDGE1, cell)
        if (cell[1] == self.size - 1):
            self.blue_groups.join(self.EDGE2, cell)
        # join any groups connected by the new blue stone
        for n in self.neighbors(cell):
            if (self.board[n] == self.PLAYERS["blue"]):
                self.blue_groups.join(n, cell)

    def turn(self):
        return self.toplay

    def winner(self):
        if (self.red_groups.connected(self.EDGE1, self.EDGE2)):
            return self.PLAYERS["red"]
        elif (self.blue_groups.connected(self.EDGE1, self.EDGE2)):
            return self.PLAYERS["blue"]
        else:
            return self.PLAYERS["none"]

    def neighbors(self, cell):
        x = cell[0]
        y = cell[1]
        return [(n[0] + x, n[1] + y)
                for n in self.neighbor_patterns
                if (0 <= n[0] + x and n[0] + x < self.size and 0 <= n[1] +
                    y and n[1] + y < self.size)]

    def moves(self):
        moves = []
        for y in range(self.size):
            for x in range(self.size):
                if self.board[x, y] == self.PLAYERS["none"]:
                    moves.append((x, y))
        return moves