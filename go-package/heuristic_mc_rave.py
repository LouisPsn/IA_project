import time
import Goban 
from random import choice
from playerInterface import *
import math


def mc_rave(board, s0, time_available):
    while (time_available):
        simulate(board, s0)
    set_position(board, s0)
    return select_move(board, s0, 0)



def simulate(board, s0):
    set_position(board, s0)
    tree = sim_tree(board)
    (default, z) = sim_default(board, T)
    concat = 
    backup(tree[0:-2], concat)


def sim_default(board, T):
    t = T + 1
    while(not board.is_game_over()):
        at = default_policy(board)
        board.push(at)
        t = t + 1
    z = board
    return 


def sim_tree(board):
    t = 0
    while (not board.is_game_over()):
        