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
from datetime import datetime, timedelta


class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._saved_time = datetime.now()
        self._time_used = datetime.now() - datetime.now()
        self._mycolor = None

    def getPlayerName(self):
        return self._mycolor

    def getPlayerMove(self):
        self._saved_time = datetime.now()
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        
        # Regarde si notre temps restant est vraiment critique dans ce cas nous renvoyons juste des move aléatoires
        if (self._time_used < timedelta(minutes = 29)):
            # Regarde s'il nous plus de 5min pour jouer, si oui limite la profondeur de recherche pour l'algorithme à 2 pour dans l'algorithme de recherche alpha-beta
            if (self._time_used < timedelta(minutes = 25)):
                max_depth = 2
            else:

                max_depth = 0
                number_of_moves = len(self._board.legal_moves()) - 1
                # Calcul la profondeur maximale de recherche pour un nombre de coups possibles donné
                while(self.limit_max_depth(max_depth, number_of_moves)):
                    max_depth += 1
                max_depth -= 1
            
            # Choix du coup optimal par l'algorithme alpha-beta
            move = self.choice_alpha_beta(self._board, max_depth) 
            self._board.push(move)
        else:
            moves = self._board.legal_moves()
            move = choice(moves) 
            self._board.push(move)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()

        self._time_used = self._time_used + datetime.now() - self._saved_time

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


    # Fonction qui calcule la profondeur de recherche maximale authorisée
    def limit_max_depth(self, max_depth, number_of_moves):
        
        if (max_depth > number_of_moves):
            return False

        val = 1
        
        for _ in range(max_depth):
            val = val*number_of_moves
            # val = val*(number_of_moves - 1)
            number_of_moves = number_of_moves - 1

        return (val <= (81*80))

    # Fonction qui définie les paramètres de la fonction alpha-beta et appelle la fonction alpha-beta
    def choice_alpha_beta(self, board, depth):

        # Cette partie de la fonction regarde si l'adversaire a passer avec nous, si c'est le cas et que nous avons un meilleur score que lui nous passons aussi
        if (self._board._lastPlayerHasPassed):
            if (self._mycolor == Goban.Board._BLACK):
                points = board.compute_score()
                if (points[0] > points[1]):
                    return self._board.legal_moves()[-1]
            else :
                points = board.compute_score()
                if (points[1] > points[0]):
                    return self._board.legal_moves()[-1]

            
        best_move = board.legal_moves()[0]
        _, move = self.alpha_beta(board, best_move, depth, -1000000000, 1000000000, True)
        return move


    # Fonction effectuant la recherche deu coup optimale selon notre heuristique maison
    def alpha_beta(self, board, best_move, depth, alpha, beta, maximizingPlayer):
        if ((depth == 0) or (board.is_game_over())):
            return [self.hand_made_heuristique(board, maximizingPlayer), best_move]
        
        # Cette partie de la fonction regarde si le seul coup que nous pouvons jouer est de passer, si c'est le cas nous passons notre tour
        if (board.legal_moves()[0] == "PASS"):
            return [self.hand_made_heuristique(board, maximizingPlayer), board.legal_moves()[0]]

        if (maximizingPlayer):
            value = -1000000000
            for move in board.legal_moves()[:-1]:
                board.push(move)

                # Cette partie de code rend les coups que nous jouons aux extrémités moins favorables pour nous
                if (self._board._historyMoveNames[-1][0] == 'A' or self._board._historyMoveNames[-1][0] == 'J' or self._board._historyMoveNames[-1][1] == '1' or self._board._historyMoveNames[-1][1] == '9'):
                    if (maximizingPlayer):
                        value = value + 0.5

                old_value = value

                value = max(value, self.alpha_beta(board, best_move, depth - 1, alpha, beta, False)[0])

                board.pop()
                if (value > old_value):
                    best_move = move
                else:
                    value = value - 0.5

                if (value > beta):
                    break # (* β cutoff *)
                alpha = max(alpha, value)
            return [value, best_move]
        else:
            value = 1000000000
            for move in board.legal_moves()[:-1]:
                board.push(move)


                # Cette partie de code rend les coups que joué par l'adversaire aux extrémités plus favorables pour nous
                if (self._board._historyMoveNames[-1][0] == 'A' or self._board._historyMoveNames[-1][0] == 'J' or self._board._historyMoveNames[-1][1] == '1' or self._board._historyMoveNames[-1][1] == '9'):
                    if (maximizingPlayer):
                        value = value - 0.5

                old_value = value
                value = min(value, self.alpha_beta(board, best_move, depth - 1, alpha, beta, True)[0])
                board.pop()
                if (value <= old_value):
                    best_move = move
                else:
                    value = value + 0.5

                if (value < alpha):
                    break # (* α cutoff *)
                beta = min(beta, value)
            return [value, best_move]
            

    # La fonction qui calcule notre heuristique maison en se basant sur les scores des joueurs pour un plateau donné
    def hand_made_heuristique(self, board, maximizingPlayer):
        
        heuristique = 0

        points = board.compute_score()

        # En fonction de si le joueur est _BLACK ou _WHITE on ne chercher pas à maximiser le même score
        if (self._mycolor == Goban.Board._BLACK):
            if (maximizingPlayer):
                heuristique = heuristique + points[0] - points[1]
            else:
                heuristique = heuristique + points[1] - points[0]
        else:
            if (maximizingPlayer):
                heuristique = heuristique + points[1] - points[0]
            else:
                heuristique = heuristique + points[0] - points[1]
        
        return heuristique