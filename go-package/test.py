import Goban 
from playerInterface import *
import importlib
import sys
import time


def fileorpackage(name):
    if name.endswith(".py"):
        return name[:-3]
    return name

if len(sys.argv) > 2:
    classNames = [fileorpackage(sys.argv[1]), fileorpackage(sys.argv[2])]
elif len(sys.argv) > 1:
    classNames = [fileorpackage(sys.argv[1]), 'myPlayer']
else:
    classNames = ['myPlayer', 'myPlayer']


b = Goban.Board()

players = []
player1class = importlib.import_module(classNames[0])
player1 = player1class.myPlayer()
player1.newGame(Goban.Board._BLACK)
players.append(player1)

player2class = importlib.import_module(classNames[1])
player2 = player2class.myPlayer()
player2.newGame(Goban.Board._WHITE)
players.append(player2)


print(b)
print("-------")

t1 = time.time()

print(b.legal_moves())
t2 = time.time()

print(b.weak_legal_moves())
t3 = time.time()

print((t2 - t1)*1000)
print((t3 - t2)*1000)