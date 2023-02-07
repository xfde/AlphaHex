import socket
from gamestate import gamestate
from MCTS import rave_node
import time
import random
from copy import deepcopy
from queue import Queue


class AgentFS():
    HOST = "127.0.0.1"
    PORT = 1234
    EXPLORATION = 1
    RAVE_CONSTANT = 300
    MOVE_TIME = 0.6

    def __init__(self, board_size=11):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))

        self.board_size = board_size
        self.colour = ""
        self.turn_count = 0
        self.rootstate = deepcopy(gamestate(self.board_size))
        self.root = rave_node()

    def run(self):
        while True:
            data = self.s.recv(1024)
            if not data:
                break
            # game ended
            if (self.interpret_data(data)):
                break

    def interpret_data(self, data):
        messages = data.decode("utf-8").strip().split("\n")
        messages = [x.split(";") for x in messages]
        for s in messages:
            if s[0] == "START":
                self.board_size = int(s[1])
                self.rootstate = deepcopy(gamestate(self.board_size))
                if s[2] == "R":
                    self.colour = 1
                else:
                    self.colour = 2

                if self.colour == 1:
                    self.make_move()
            elif s[0] == "END":
                return True
            elif s[0] == "CHANGE":
                if s[3] == "END":
                    return True
                elif s[1] == "SWAP":  # must be turn 3 - T1 R, T2 SWAP, T3 -B
                    self.colour = self.opp_colour()
                    if self.compare_colours(s[3]):
                        self.make_move()
                elif self.compare_colours(s[3]):
                    action = [int(x) for x in s[1].split(",")]
                    action = (action[0], action[1])
                    self.move(action)
                    self.make_move()
        return False

    # already changes colour
    def make_move(self):
        if self.colour == 2 and self.turn_count == 0:
            self.s.sendall(bytes("SWAP\n", "utf-8"))
        else:
            self.search(self.MOVE_TIME)
            move = self.best_move()
            # move is inside agents board
            self.move(move)
            self.s.sendall(bytes(f"{move[0]},{move[1]}\n", "utf-8"))
        self.turn_count += 1

    def opp_colour(self):
        if self.colour == 1:
            return 2
        elif self.colour == 2:
            return 1
        else:
            return 0

    def compare_colours(self, jon):
        # return true if our colous is the same as param, false otherwise
        if jon == "R":
            if self.colour == 1:
                return True
            else:
                return False
        if jon == "B":
            if self.colour == 2:
                return True
            else:
                return False
        return False

    # MCTS
    def best_move(self):
        if (self.rootstate.winner() != gamestate.PLAYERS["none"]):
            return gamestate.GAMEOVER
        # choose the move of the most simulated node breaking ties randomly
        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        bestchild = random.choice(max_nodes)
        return bestchild.move

    def move(self, move):
        if move in self.root.children:
            child = self.root.children[move]
            child.parent = None
            self.root = child
            self.rootstate.play(child.move)
            return

        # if for whatever reason the move is not in the children of
        # the root just throw out the tree and start over
        self.rootstate.play(move)
        self.root = rave_node()

    def search(self, time_budget):
        startTime = time.time()
        num_rollouts = 0

        # do until we exceed our time budget
        while (time.time() - startTime < time_budget):
            node, state = self.select_node()
            turn = state.turn()
            outcome, blue_rave_pts, red_rave_pts = self.roll_out(state)
            self.backup(node, turn, outcome, blue_rave_pts, red_rave_pts)
            num_rollouts += 1

    def select_node(self):
        node = self.root
        state = deepcopy(self.rootstate)

        # stop if we reach a leaf node
        while (len(node.children) != 0):
            max_value = max(node.children.values(),
                            key=lambda n: n.value(
                                self.EXPLORATION, self.RAVE_CONSTANT)).value(
                                    self.EXPLORATION, self.RAVE_CONSTANT)
            # decend to the maximum value node, break ties at random
            max_nodes = [
                n for n in node.children.values()
                if n.value(self.EXPLORATION, self.RAVE_CONSTANT) == max_value
            ]
            node = random.choice(max_nodes)
            state.play(node.move)

            # if some child node has not been explored select it before expanding
            # other children
            if node.N == 0:
                return (node, state)

        # if we reach a leaf node generate its children and return one of them
        # if the node is terminal, just return the terminal node
        if (self.expand(node, state)):
            node = random.choice(list(node.children.values()))
            state.play(node.move)
        return (node, state)

    def backup(self, node, turn, outcome, blue_rave_pts, red_rave_pts):
        # note that reward is calculated for player who just played
        # at the node and not the next player to play
        reward = -1 if outcome == turn else 1

        while node != None:
            if turn == gamestate.PLAYERS["red"]:
                for point in red_rave_pts:
                    if point in node.children:
                        node.children[point].Q_RAVE += -reward
                        node.children[point].N_RAVE += 1
            else:
                for point in blue_rave_pts:
                    if point in node.children:
                        node.children[point].Q_RAVE += -reward
                        node.children[point].N_RAVE += 1

            node.N += 1
            node.Q += reward
            if turn == gamestate.PLAYERS["blue"]:
                turn = gamestate.PLAYERS["red"]
            else:
                turn = gamestate.PLAYERS["blue"]
            reward = -reward
            node = node.parent

    def expand(self, parent, state):
        children = []
        if (state.winner() != gamestate.PLAYERS["none"]):
            # game is over at this node so nothing to expand
            return False

        for move in state.moves():
            children.append(rave_node(move, parent))

        parent.add_children(children)
        return True

    def set_gamestate(self, state):
        self.rootstate = deepcopy(state)
        self.root = rave_node()

    def roll_out(self, state):
        moves = state.moves()
        while (state.winner() == gamestate.PLAYERS["none"]):
            move = random.choice(moves)
            state.play(move)
            moves.remove(move)

        blue_rave_pts = []
        red_rave_pts = []

        for x in range(state.size):
            for y in range(state.size):
                if state.board[(x, y)] == gamestate.PLAYERS["blue"]:
                    blue_rave_pts.append((x, y))
                elif state.board[(x, y)] == gamestate.PLAYERS["red"]:
                    red_rave_pts.append((x, y))

        return state.winner(), blue_rave_pts, red_rave_pts

    def tree_size(self):
        Q = Queue()
        count = 0
        Q.put(self.root)
        while not Q.empty():
            node = Q.get()
            count += 1
            for child in node.children.values():
                Q.put(child)
        return count


if (__name__ == "__main__"):
    agent = AgentFS()
    agent.run()
