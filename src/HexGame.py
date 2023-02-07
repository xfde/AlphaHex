import numpy as np
import collections
from Logic import Board

class HexGame():
    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n+1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board(self.n)
        b.pieces = np.copy(board)
        if action == 121:
            move = (-1,-1)
        else:
            move = (int(action/self.n), action%self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board) 

        # if player == -1:
        #     b.pieces = np.rot90(-1 * board, axes=(1, 0))
        # else:
        #     b.pieces = np.copy(board) 

        # print('get valid', player)
        # display(b.pieces)  

        legalMoves = b.get_legal_moves(player)
        if len(legalMoves)==0:
            print('no valid moves')
            return np.array(valids)
        for x, y in legalMoves:
            if x == -1 and y == -1:
                valids[121]= 1
            else:
                valids[self.n*x+y]=1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost

        b = Board(self.n)
        b.pieces = board

        for y in range(self.n):
            if b.is_connected((0, y), 1):
                # print('=============== end', (0, y), player, 1 if player == 1 else -1)
                return 1 if player == 1 else -1

        for x in range(self.n):
            if b.is_connected((x, 0), -1):
                # print('=============== end', (x, 0), player, 1 if player == -1 else -1)
                return 1 if player == -1 else -1
        
        return 0            


    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        if player == 1:
            return board
        else:
            return np.fliplr(np.rot90(-1*board, axes=(1, 0)))

    def getOriginalForm(self, board, player):
        if player == 1:
            return board
        else:
            return np.rot90(np.fliplr(-1*board), axes=(0, 1))
            
    def getSymmetries(self, board, pi):
        # rotation 180 degree
        tmp_pi = pi[:121]
        pi_board = np.reshape(tmp_pi, (self.n, self.n))
        l = []

        for i in [0, 2]:
            newB = np.rot90(board, i)
            newPi = np.rot90(pi_board, i)
            new_pi = list(newPi.ravel())
            new_pi.append(pi[121])
            l += [(newB, new_pi)]
        return l

    def stringRepresentation(self, board):
        string = ""
        for i in range(len(board)):
            for j in range(len(board[0])):
                string+=str(board[i,j])
        return string


# def display(board):
#     n = board.shape[0]

#     print("   ", "B  " * n, "\n    ", end="")
#     for y in range(n):
#         print (y, "\\",end="")
#     print("")
#     print("", "----" * n)
#     for y in range(n):
#         print(" " * y, "W", y, "\\",end="")    # print the row #
#         for x in range(n):
#             piece = board[x][y]    # get the piece to print
#             if piece == -1: print("b  ",end="")
#             elif piece == 1: print("w  ",end="")
#             else:
#                 if x==n:
#                     print("-",end="")
#                 else:
#                     print("-  ",end="")
#         print("\\ {} W".format(y))

#     print(" " * n, "----" * n)
#     print("      ", " " * n, end="")
#     for y in range(n):
#         print (y, "\\",end="")
#     print("")        
#     print("      ", " " * n, "B  " * n)