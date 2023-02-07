from Board import Board
from Game import Game
from Tile import Tile
from Colour import Colour
from Move import Move
import numpy as np


class GameWrapper():

    def __init__(self, board_size=11, red='R', blue='B') -> None:
        self.board_size = board_size
        self.game = Game(board_size)
        pass

    def getInitBoard(self) -> np.ndarray[Tile]:
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        board = []
        for _ in range(self.board_size):
            for _ in range(self.board_size):
                board.append(0)
        return np.array(board)

    def getActionSize(self) -> int:
        """
        Returns:
            actionSize: number of all possible actions
        """
        return self.board_size**2

    def getNextState(self, board: np.ndarray[Tile], player: str,
                     action: tuple[int, int]) -> tuple[np.ndarray[Tile], str]:
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player
        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        clr = None
        if player == 1:
            clr = Colour.RED
        else:
            clr = Colour.BLUE
        move = Move(clr, action[0], action[1])
        if not move.is_valid_move(self.game):
            return (None, None)
        move = Move(player, action[0], action[1])
        self.game._make_move(move)
        board[11*action[0]+action[1]] = player
        # handle swap on our board
        return board, -player

    def getValidMoves(self, board, player) -> list[int]:
        """
        Input:
            board: current board
            player: current player
        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        valid = [0] * self.getActionSize()
        for i, tile in enumerate(board):
            if not tile:
                valid[i] = 1
        return valid

    def getGameEnded(self, board: np.ndarray[Tile], player: str):
        """
        Input:
            board: current board
            player: current player (1 or -1)
        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.

        """
        if self.game.get_next_player() == "END":
            return 1 if self.game.get_player() == player else -1
        return 0

    def getOriginalForm(self, board: np.ndarray[Tile], player: str):
        if player == 1 or player==-1:
            if player == 1:
                return board
            else:
                cpy = board
                for idx, tile in enumerate(board):
                    if tile == 1:
                        cpy[idx] = -1 
                    elif tile == -1:
                        cpy[idx] = 1
                return cpy
        else:
            if player == "R":
                return board
            else:
                ## PROBABLY NOT CORRECT
                cpy = board
                for i, tile in enumerate(board):
                    if tile.get_colour() == 1:
                        cpy[i].set_colour(-1)
                    if tile.get_colour() == -1:
                        cpy[i].set_colour(1)
                return cpy

    def getCanonicalForm(self, board: np.ndarray[Tile],
                         player: str) -> np.ndarray[Tile]:
        """
        Input:
            board: current board
            player: current player (1 or -1)
        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        # chose player 1 as cannonical
        if player == "R" or player=="B":
            if player == "R":
                return board
            else:
                cpy = board
                for i, tile in enumerate(board):
                    if tile.get_colour() == 1:
                        cpy[i].set_colour(-1)
                    if tile.get_colour() == -1:
                        cpy[i].set_colour(1)
                return cpy
        elif player == 1 or player == -1:
            if player == 1:
                return board
            else:
                cpy = board
                for idx, tile  in enumerate(board):
                    if tile == 1:
                        cpy[idx] = -1 
                    elif tile == -1:
                        cpy[idx] = 1
                return cpy
                

    def getSymmetries(self, board: np.ndarray[Tile], pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()
        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        pass

    def stringRepresentation(self, board: np.ndarray[Tile]) -> str:
        """
        Input:
            board: current board
        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        def int_to_str(x):
            if x == 1:
                return 'R'
            if x == -1:
                return 'B'
            return ' '
            
        string: str = ""
        for tile in board:
            string += int_to_str(tile)
        return string

    def getBoardSize(self):
        return (self.board_size, self.board_size)
