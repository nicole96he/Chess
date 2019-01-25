import chess

class MinimaxAI():
    def __init__(self, depth):
        self.calls = 0
        self.depth = depth
        pass

    '''
    Purpose: call ids function to get best_move
        Args: board
        Return: best_move
    '''
    def choose_move(self,board):
        best_move = self.ids(board)  #call ids function
        print (self.calls)  # print visited node
        print (self.depth)
        return best_move

    '''
    Purpose: use iterative deepening to find better move
        Args: board
        Return: best_move
    '''
    def ids(self,board):
        best_move = ""
        if board.turn:  # when it is white to take action
            cur_value = float ('-inf')  # initialize the value as negative infinity
            for cur_depth in range(1,self.depth+1): # loop depth
                cur_node = self.minimax(board,cur_depth)
                if cur_value < cur_node.value:
                    # bigger value is better for white, so i compare current value with former one.
                    cur_value = cur_node.value # choose bigger value
                    best_move = cur_node.move # renew move
                if cur_value == 10000: # judge if white wins here
                    return best_move # If black wins here, this is the real best move.
        else: # when it is black to take action
            cur_value = float ('inf')  # initialize the value as positive infinity
            for cur_depth in range(1,self.depth+1):
                cur_node = self.minimax(board,cur_depth)
                if cur_value > cur_node.value:
                    # smaller value is better for black, so if current value is bigger, we will replace with smaller value.
                    cur_value = cur_node.value
                    best_move = cur_node.move # renew move
                if cur_value == -10000: # judge if black wins or not
                    return best_move
        return best_move

    '''
    Purpose: minimax function
        Args: board, depth
        Returns: Node (include move and evaluation value)
    '''
    def minimax(self,board,depth):
        self.calls += 1 # calls is used to count visited nodes
        Node = node() # initialize a node
        if self.cut_off(board,depth): # judge whether it has arrived result state or not.
            Node.value = self.Utility(board) # get current evaluation
            return Node
        if board.turn: # when it is white to take action
            Node.value = float('-inf') # initialize value as negative infinity
            for cur_move in board.legal_moves: # traverse all possible legal_moves
                board.push(cur_move) # renew the board, apply move to board
                new_Node = self.minimax(board,depth-1)

                if Node.value < new_Node.value: # Get max value
                    Node.move = cur_move # renew move
                    Node.value = new_Node.value

                board.pop() # repent the move

        else: # when it is black to take action
            Node.value = float('inf') # initialize value as positive infinity
            for cur_move in board.legal_moves: # traverse all legal moves
                board.push(cur_move) # renew board
                new_Node = self.minimax(board,depth-1)
                if Node.value > new_Node.value: # get min value
                    Node.move = cur_move
                    Node.value = new_Node.value
                board.pop() # repent the move

        return Node


    '''
    Purpose: get evaluation for different situation
        Args: board
        Return: value
    '''
    def Utility(self,board):
        if board.result() == '*': # For no result situation
            return self.evaluation(board) # return evaluation value
        elif board.result() == "1-0": # when white wins
            return 10000              # return a biggest value
        elif board.result() == "0-1": # when black wins
            return -10000            # return a smallest value
        elif board.result() == "1/2-1/2": # For draw situation
            return 0        # return zero
        return self.evaluation(board)


    '''
    Purpose: judge if the minimax search should stop or not
        Args: board, depth
        Return: true or false
    '''
    def cut_off(self, board,depth):
        if board.is_game_over(): # judge if the game is game over
            return True
        elif depth == 0: # judge if search has reached maximum depth
            return True
        return False

    '''
    Purpose: calculate evaluation value
        Args: board
        Returns: value
    '''
    def evaluation(self,board):
        evaluation_white = 1*len(board.pieces(chess.PAWN, chess.WHITE)) + 3*len(board.pieces(chess.KNIGHT,chess.WHITE)) + 3*len(board.pieces(chess.BISHOP,chess.WHITE))
        evaluation_white += 5*len(board.pieces(chess.ROOK,chess.WHITE)) + 9*len(board.pieces(chess.QUEEN,chess.WHITE))
        evaluation_black = 1*len(board.pieces(chess.PAWN, chess.BLACK)) + 3*len(board.pieces(chess.KNIGHT,chess.BLACK)) + 3*len(board.pieces(chess.BISHOP,chess.BLACK))
        evaluation_black += 5*len(board.pieces(chess.ROOK,chess.BLACK)) + 9*len(board.pieces(chess.QUEEN,chess.BLACK))
        evaluation_diff = evaluation_white - evaluation_black
        return evaluation_diff

class node:
    def __init__(self):
        self.move = ""
        self.value = 0
