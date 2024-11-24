import random
class Player():
    def __init__(self, name="random"):
        self.name = name
        random.seed()
    def act(self, board):
        current_player = board.turn + 1  # +1 so it will how 1/2 instead of 0/1
        valid_moves = board.valid_moves()
        print(f"Player {current_player} [{self.name}] valid moves are {[move + 1 for move in valid_moves]}")
        pit_index = random.choice(valid_moves)
        print(f"Player {current_player} [{self.name}] picked move {pit_index + 1}")
        return pit_index


if __name__ == '__main__':
    player = Player()
    print(f"Player selected pit {player.act(0)}")

