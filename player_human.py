
class Human():
    def __init__(self, name="human"):
        self.name = name
    def act(self, board):
        # TODO choose between legal moves
        current_player = board.turn + 1  # +1 so it will how 1/2 instead of 0/1
        while True:
            try:
                pit_index = int(input(f"Choose a pit (1-6) to sow for player {current_player}: ")) - 1
                if not 0 <= pit_index < 6:
                    raise ValueError("Invalid pit number.")
                return pit_index
            except ValueError:
                print("Invalid input. Please enter an integer between 1 and 6.")

if __name__ == '__main__':
    player = Human()
    print(f"Player selected pit {player.act(0)}")

