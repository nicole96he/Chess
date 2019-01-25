# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame
from transposition_alphabeta import transposition_table

import sys


player1 = AlphaBetaAI(2)
player2 = AlphaBetaAI(2)
player3 = MinimaxAI(3)
player4 = MinimaxAI(3)
player5 = transposition_table(2)
player6 = transposition_table(2)
game = ChessGame(player3, player4)
while not game.is_game_over():
    print(game)
    game.make_move()
print (game.board.result())

#print (player1.consider_call)
#print (player2.consider_call)
#print(hash(str(game.board)))
