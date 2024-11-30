import copy
from mancala import STORE

class Player():
    """
    Returns the optimal action for the current player on the board.
    If the board is a terminal board, the minimax function should return None.

    Pseudocode:

    Given a state s
    The maximizing player picks action a in Actions(s) that produces the highest value of Min-Value(Result(s, a)).
    The minimizing player picks action a in Actions(s) that produces the lowest value of Max-Value(Result(s, a)).

    Function Max-Value(state)
    v = -∞
    if Terminal(state):
    return Utility(state)
    for action in Actions(state):
    v = Max(v, Min-Value(Result(state, action)))
    return v

    Function Min-Value(state):
    v = ∞
    if Terminal(state):
    return Utility(state)
    for action in Actions(state):
    v = Min(v, Max-Value(Result(state, action)))
    return v
    """

    def __init__(self, player, name="minmax", max_depth=7):
        self.player = player
        self.name = name
        self.max_depth = max_depth

    def minmax_eval(self, board, depth=None):
        if depth == None:
            depth = self.max_depth
        if board.check_game_over() or depth == 0:
            # TODO add score if it remains player turn
            return board.pits[self.player][STORE] - board.pits[1 - self.player][STORE]

        if board.turn == 0:
            score = -50
            for move in board.valid_moves():
                score = max(score, self.minmax_eval(self.result(board, move), depth - 1))
                print(f"Player 0, move {move}, score {score}")
        else:
            score = 50
            for move in board.valid_moves():
                score = min(score, self.minmax_eval(self.result(board, move), depth - 1))
                print(f"Player 0, move {move}, score {score}")
        print(f"Best score is {score}")
        return score

    def result(self, board, move):
        """
        Returns the board that results from making the on the board.
        If invalid move, raise Exception.
        Result is a deepcopy board
        """
        # check validity of move - not required because selecting from valid list

        next_board = copy.deepcopy(board)
        next_board.sow(move)
        return next_board


    def act(self, board):
        current_player = board.turn
        valid_moves = board.valid_moves()

        if valid_moves == []:  # if game is over
            return None

        evaluated_moves = []
        for move in valid_moves:
            board_after_optional_move = self.result(board, move)
            evaluated_moves.append([move, self.minmax_eval(board_after_optional_move, self.max_depth)])  # result(board, action)

        if current_player == 0:
            # player 0, return max
            return max(evaluated_moves, key=lambda s: s[1])[0]
        else:
            # player 1, return min
            return min(evaluated_moves, key=lambda s: s[1])[0]
