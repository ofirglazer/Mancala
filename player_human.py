
class Player:
    def __init__(self, name="human"):
        self.name = name

    def act(self, board):
        current_player = board.turn + 1  # +1 so it will how 1/2 instead of 0/1
        valid_moves = board.valid_moves()
        print(f"Player {current_player} [{self.name}] valid moves are {[move + 1 for move in valid_moves]}")
        while True:
            try:
                pit_index = int(input(f"Choose a valid pit to sow: ")) - 1
                if pit_index not in valid_moves:
                    raise ValueError("Invalid pit number.")
                return pit_index
            except ValueError:
                print(f"Invalid input. Please enter an integer from {[move + 1 for move in valid_moves]}.")
