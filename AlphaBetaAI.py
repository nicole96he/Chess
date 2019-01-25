import chess
from math import inf
import random

class AlphaBetaAI():
    def __init__(self, depth):
        self.consider_call = 0
        self.depth = depth

    '''
    Purpose: call ids function to get best_move
        Args: board
        Return: best_move
    '''
    def choose_move(self, board):
        node = self.alphabeta(board, self.depth, float('-inf'), float('inf'))
        # call alphabeta function
        print (self.consider_call) # print total number of visited nodes
        return node.move

    '''
    Purpose: alphabeta function
        Args: board, depth, alpha, beta
        Returns: Node (include move and evaluation value)
    '''
    def alphabeta(self,board, depth, alpha, beta):
        Node = node()
        if depth==0 or self.cut_off(board,depth)==True:
            Node.value = self.Utility(board)
            return Node
        if board.turn: # when it is white to take action
            Node.value = float('-inf') # initialize value as negative infinity
            possible_moves = list(board.legal_moves)  # transform legal_moves into list
            random.shuffle(possible_moves)
            # This is reorder function. If you don't want to reorder moves, just uncomment this command line.
            for cur_move in possible_moves: # traverse all possible moves
                board.push(cur_move) # renew current board
                new_node = self.alphabeta(board,depth-1,alpha,beta)
                self.consider_call  += 1 # calculate the number of visited nodes
                if Node.value < new_node.value:
                    Node.move = cur_move
                    Node.value = new_node.value
                board.pop()
                alpha = max(alpha,Node.value)
                if beta <= alpha:
                    break

        else:
            Node.value = float('inf')
            possible_moves = list(board.legal_moves)
            random.shuffle(possible_moves)
            # This is reorder function. If you don't want to reorder moves, just uncomment this command line.
            for cur_move in possible_moves:
                board.push(cur_move)
                new_node = self.alphabeta(board,depth-1, alpha, beta)
                self.consider_call += 1
                if Node.value > new_node.value:
                    Node.move = cur_move
                    Node.value = new_node.value
                beta = min(beta,Node.value)
                board.pop()
                if beta <= alpha:
                    break
        return Node


    '''
    Purpose: get evaluation for different situation
        Args: board
        Return: value
    '''
    def Utility(self, board):
        if board.result() == '*':
            return self.evaluation(board)
        elif board.result() == "1-0":
            return 10000
        elif board.result() == "0-1":
            return -10000
        elif board.result() == "1/2-1/2":
            return 0
        return self.evaluation(board)


    '''
    Purpose: judge if the minimax search should stop or not
        Args: board, depth
        Return: true or false
    '''
    def cut_off(self, board, depth):
        if board.is_game_over():
            return True
        elif depth == 0:
            return True
        return False

    '''
    Purpose: calculate evaluation value
        Args: board
        Returns: value
    '''

    def evaluation(self, board):
        evaluation_white = 1 * len(board.pieces(chess.PAWN, chess.WHITE)) + 3 * len(board.pieces(chess.KNIGHT, chess.WHITE)) + 3 * len(board.pieces(chess.BISHOP, chess.WHITE))
        evaluation_white += 5 * len(board.pieces(chess.ROOK, chess.WHITE)) + 9 * len(board.pieces(chess.QUEEN, chess.WHITE))
        evaluation_black = 1 * len(board.pieces(chess.PAWN, chess.BLACK)) + 3 * len(board.pieces(chess.KNIGHT, chess.BLACK)) + 3 * len(board.pieces(chess.BISHOP, chess.BLACK))
        evaluation_black += 5 * len(board.pieces(chess.ROOK, chess.BLACK)) + 9 * len(board.pieces(chess.QUEEN, chess.BLACK))
        evaluation_diff = evaluation_white - evaluation_black
        return evaluation_diff


class node:
    def __init__(self):
        self.move = ""
        self.value = 0
        self.kind = ""



