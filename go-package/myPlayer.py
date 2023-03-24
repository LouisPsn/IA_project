# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban 
from random import choice
from playerInterface import *
import math

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

    def getPlayerName(self):
        return "Random Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        moves = self._board.legal_moves() # Dont use weak_legal_moves() here!
        max_depth = 2
        move = self.choice_alpha_beta(self._board, max_depth) 
        self._board.push(move)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



    def choice_alpha_beta(self, board, depth):
        best_move = board.legal_moves()[0]
        _, move = self.alpha_beta(board, best_move, depth, -1000000000, 1000000000, True)
        return move



    def alpha_beta(self, board, best_move, depth, alpha, beta, maximizingPlayer):
        if ((depth == 0) or (board.is_game_over())):
            return [self.hand_made_heuristique(board, maximizingPlayer), best_move]
        if (maximizingPlayer):
            value = -1000000000
            for move in board.legal_moves():
                board.push(move)
                old_value = value
                value = max(value, self.alpha_beta(board, best_move, depth - 1, alpha, beta, False)[0])
                board.pop()
                if (value > old_value):
                    best_move = move
                if (value > beta):
                    break # (* β cutoff *)
                alpha = max(alpha, value)
            return [value, best_move]
        else:
            value = 1000000000
            for move in board.legal_moves():
                board.push(move)
                old_value = value
                value = min(value, self.alpha_beta(board, best_move, depth - 1, alpha, beta, True)[0])
                board.pop()
                if (value < old_value):
                    best_move = move
                if (value < alpha):
                    break # (* α cutoff *)
                beta = min(beta, value)
            return [value, best_move]
            


    def hand_made_heuristique(self, board, maximizingPlayer):
        points = board.compute_score()
        if (self._mycolor == "_Black"):
            if (maximizingPlayer):
                heuristique = points[0] - points[1]
            else:
                heuristique = points[1] - points[0]
        else:
            if (maximizingPlayer):
                heuristique = points[1] - points[0]
            else:
                heuristique = points[0] - points[1]
        return heuristique



def test():
    p = myPlayer()
    move = p.choice_alpha_beta(p._board, 1)
    print(move)


test()