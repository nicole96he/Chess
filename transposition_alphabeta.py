import chess
import random
class transposition_table():
    def __init__(self, depth):
        self.depth = depth
        self.consider_call = 0
        pass

    '''
    Purpose: call ids function to get best_move
        Args: board
        Return: best_move
    '''
    def choose_move(self, board):
        node = self.alphabeta_trans(board, self.depth, float('-inf'), float('inf'))
        print (self.consider_call)
        return node.move

    '''
    Purpose: alphabeta function
        Args: board, depth, alpha, beta
        Returns: Node (include move and evaluation value)
    '''
    def alphabeta_trans(self, board, depth, alpha, beta):
        Node = node()
        hash_table_white = {}
        # create a dictionary to store white visited nodes.
        hash_table_black = {}
        # create a dictionary to store black visited nodes.
        if depth == 0 or self.cut_off(board, depth) == True:
            Node.value = self.Utility(board)
            return Node
        if board.turn: # when it is white to take action
            Node.value = float('-inf')
            possible_moves = list(board.legal_moves)  # transform legal_moves into list
            random.shuffle(possible_moves)
            for cur_move in possible_moves:
                board.push(cur_move)
                hash_board = wrap_board(board) # transform board into numbers using wrap_board class
                if hash_board in hash_table_white: # Judge if current board has visited before
                    Node = hash_table_white[hash_board] # get Node from dictionary
                    board.pop() # reset the board
                    continue

                self.consider_call += 1
                new_node = self.alphabeta_trans(board, depth - 1, alpha, beta)

                if new_node.value <= alpha: # if current value is smaller than or equal to alpha
                    new_node.kind = "at most" # this node value is at most this value
                    hash_table_white[hash_board] = new_node  # put this node into dictionary
                elif new_node.value >= beta: # if current value is bigger than or equal to beta
                    new_node.kind = "at least"  # this node value is at least this value
                    hash_table_white[hash_board] = new_node # put this node into dictionary
                else:            # if this value is between alpha and beta
                    new_node.kind = "exact"  # this node value is exact this value
                    hash_table_white[hash_board] = new_node # put this node into dictionary

                if Node.value < new_node.value: # this part is same as normal alpta-beta search.
                    Node.move = cur_move
                    Node.value = new_node.value
                board.pop()
                alpha = max(alpha, Node.value)
                if beta <= alpha:
                    break

        else:  # when it is black to take action
            Node.value = float('inf')
            possible_moves = list(board.legal_moves)  # transform legal_moves into list
            random.shuffle(possible_moves)
            for cur_move in possible_moves:
                board.push(cur_move)
                hash_board = wrap_board(board)
                if hash_board in hash_table_black:
                    Node = hash_table_black[hash_board]
                    board.pop()
                    continue

                self.consider_call += 1
                new_node = self.alphabeta_trans(board, depth - 1, alpha, beta)

                if new_node.value <= alpha:
                    new_node.kind = "at most"
                    hash_table_black[hash_board] = new_node
                elif new_node.value >= beta:
                    new_node.kind = "at least"
                    hash_table_black[hash_board] = new_node
                else:
                    new_node.kind = "exact"
                    hash_table_black[hash_board] = new_node


                if Node.value > new_node.value:
                    Node.move = cur_move
                    Node.value = new_node.value
                beta = min(beta, Node.value)
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
        evaluation_white = 1 * len(board.pieces(chess.PAWN, chess.WHITE)) + 3 * len(
            board.pieces(chess.KNIGHT, chess.WHITE)) + 3 * len(board.pieces(chess.BISHOP, chess.WHITE))
        evaluation_white += 5 * len(board.pieces(chess.ROOK, chess.WHITE)) + 9 * len(
            board.pieces(chess.QUEEN, chess.WHITE))
        evaluation_black = 1 * len(board.pieces(chess.PAWN, chess.BLACK)) + 3 * len(
            board.pieces(chess.KNIGHT, chess.BLACK)) + 3 * len(board.pieces(chess.BISHOP, chess.BLACK))
        evaluation_black += 5 * len(board.pieces(chess.ROOK, chess.BLACK)) + 9 * len(
            board.pieces(chess.QUEEN, chess.BLACK))
        evaluation_diff = evaluation_white - evaluation_black
        return evaluation_diff


class node:
    def __init__(self):
        self.move = ""
        self.value = 0
        self.kind = ""


'''
Purpose: wraps game boards
'''
class wrap_board():
    def __init__(self, board):
        self.board = board

    def hash(self):
        return hash(str(self.board))