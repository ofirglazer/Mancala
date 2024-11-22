class Board:
    def __init__(self):
        # 6 pits per player (each with 4 stones initially), and 2 stores (Mancalas) for players.
        self.pits = [[4] * 6, [4] * 6]  # 2 players, 6 pits each
        self.stores = [0, 0]  # Two stores, one for each player
        self.turn = 0  # Player 0's turn starts first

    def draw(self):
        print("   ", end="")
        for i in range(5, -1, -1):
            print(str(self.pits[1][i]).rjust(2, ' '), end=" ")
        print("\n", self.stores[1], "                 ", self.stores[0])
        print("   ", end="")
        for i in range(0, 6):
            print(str(self.pits[0][i]).rjust(2, ' '), end=" ")
        print("\n")

    def switch_turn(self):
        # Switch turns between players
        self.turn = 1 - self.turn

    def is_valid_move(self, pit_index):
        # Checks if the pit chosen by the player is valid (i.e., it must contain stones)
        if self.pits[self.turn][pit_index] > 0:
            return True
        return False

    def sow(self, pit_index):
        # Perform the sowing operation from a selected pit

        # 1. removes stones from selected pit
        current_player = self.turn
        side = current_player
        stones = self.pits[side][pit_index]
        self.pits[side][pit_index] = 0  # Empty the selected pit

        # 2. put stones in next pits
        while stones > 0:
            finish_in_store = False
            pit_index = (pit_index + 1) % 6  # Move to the next pit

            # handling stores during sow
            if pit_index == 0:  # arriving at a store
                if side == current_player:  # player's store
                    self.stores[side] += 1
                    stones -= 1

                if stones == 0:  # the stone in the store was the last
                    finish_in_store = True
                    break
                else:
                    side = 1 - side  # switch to other side after store

            self.pits[side][pit_index] += 1
            stones -= 1

        # 3. take opponent stones if land on empty in own side
        if side == current_player and self.pits[side][pit_index] == 1 and not finish_in_store:  # last stone was put in empty pit
            self.stores[current_player] += self.pits[1-side][5 - pit_index] + 1  # opposite stones + last own stone
            self.pits[1 - side][5 - pit_index] = 0
            self.pits[side][pit_index] = 0

        # 4. switch player except when finish in own store
        if not finish_in_store:  # finished sowing in own store
            self.switch_turn()

    def check_game_over(self):
        # Game is over if one player has no stones left in their pits
        if sum(self.pits[0]) == 0:
            empty_side = 0
        elif sum(self.pits[1]) == 0:
            empty_side = 1
        else:
            return False

        for i in range(0, 6):
            self.stores[empty_side] += self.pits[1 - empty_side][i]
            self.pits[1 - empty_side][i] = 0
        return True

    def get_board_state(self):
        # Returns the current state of the board, useful for displaying to the user
        return {
            "player_1_pits": self.pits[0],
            "player_2_pits": self.pits[1],
            "player_1_store": self.stores[0],
            "player_2_store": self.stores[1]
        }


class Game:
    def __init__(self):
        self.board = Board()
        self.players = ["Player 1", "Player 2"]

    def play_move(self, pit_index):
        # First, check if the move is valid
        if not self.board.is_valid_move(pit_index):
            print(f"Invalid move for {self.players[self.board.turn]}. Try again.")
            return False
        # Then perform the move
        self.board.sow(pit_index)
        if self.board.check_game_over():
            return True  # Game Over
        return False

    def get_winner(self):
        # Calculate the total number of stones in each player's store
        if self.board.stores[0] > self.board.stores[1]:
            return "Player 1 wins!"
        elif self.board.stores[0] < self.board.stores[1]:
            return "Player 2 wins!"
        else:
            return "It's a tie!"

    def play_game(self):
        while True:
            # Display current board state
            # board_state = self.board.get_board_state()
            # print(f"Player 1: {board_state['player_1_store']} | {board_state['player_1_pits']}")
            # print(f"Player 2: {board_state['player_2_store']} | {board_state['player_2_pits']}")
            self.board.draw()

            current_player = self.players[self.board.turn]
            print(f"{current_player}'s turn")

            # Prompt player for a move
            try:
                pit_index = int(input(f"Choose a pit (1-6) to sow for {current_player}: ")) - 1
                if not 0 <= pit_index < 6:
                    raise ValueError("Invalid pit number.")
                if self.play_move(pit_index):
                    print("Game Over!")
                    print(self.get_winner())
                    break
            except ValueError:
                print("Invalid input. Please enter an integer between 1 and 6.")


"""
# Set up the game
board = [0] * 14
player_turn = 0  # Player 1: 0, Player 2: 1
game_over = False


# Function to draw the board
def draw_board():
    # print("\nPlayer 2 store:", board[13])
    print("   ", end="")
    for i in range(12, 6, -1):
        print(str(board[i]).rjust(2, ' '), end=" ")
    print("\n", board[13], "                 ", board[6])
    print("   ", end="")
    for i in range(0, 6):
        print(str(board[i]).rjust(2, ' '), end=" ")
    # print("\nPlayer 1 store:", board[6])
    print("\n")


# Function to update the game state
def update_game_state(pit_index):
    global game_over
    print(f"Board sum is {sum(board)}")
    global player_turn # required because this function changes this global var
    stones = board[pit_index]
    board[pit_index] = 0
    current_index = pit_index
    while stones > 0:
        current_index = (current_index + 1) % 14
        if (player_turn == 0
                and current_index == 13) or (player_turn == 1
                                             and current_index == 6):
            continue
        board[current_index] += 1
        stones -= 1

    # Capture stones if the last stone lands in an empty pit on the player's side
    if current_index != 6 and current_index != 13 and board[current_index] == 1:
        if ((player_turn == 0 and current_index in range(0, 6)) or
            (player_turn == 1 and current_index in range(7, 13))):
            opposite_pit = 12 - current_index
            captured_stones = board[opposite_pit] + 1
            board[opposite_pit] = 0
            board[current_index] = 0
            if player_turn == 0:
                board[6] += captured_stones
            else:
                board[13] += captured_stones

    # Switch player turn if the last stone does not land in the player's store
    if ((player_turn == 0 and current_index != 6) or
            (player_turn == 1 and current_index != 13)):
        player_turn = 1 - player_turn

    # Check for game over condition
    if all(stones == 0
           for stones in board[0:6]) or all(stones == 0
                                            for stones in board[7:13]):
        game_over = True
"""


def main():
    game = Game()
    # TODO draw pit positions
    game.play_game()


"""
    # global board
    # draw pit positions
    for i in range(1,15):
        board[i-1] = i
    print("Pit numbering:")
    draw_board()
    print("")
    board = [4] * 14  # Number of pits (12) + 2 stores (1 for each player)
    board[6] = board[13] = 0

    # Main game loop
    while not game_over:
        draw_board()
        if player_turn == 0:
            pit_index = int(input("Player 1's turn. Select a pit (1-6): ")) - 1
            if pit_index not in range(0,6):
                print("Invalid move! Try again.")
                continue
        else:
            pit_index = int(input("Player 2's turn. Select a pit (8-13): ")) - 1
            if pit_index not in range(7,13):
                print("Invalid move! Try again.")
                continue
        if board[pit_index] == 0:
            print("Invalid move! Try again.")
            continue
        update_game_state(pit_index)

    # Game over
    draw_board()
    print("Game over!")
    if board[6] > board[13]:
        print("Player 1 wins!")
    elif board[6] < board[13]:
        print("Player 2 wins!")
    else:
        print("It's a tie!")"""

if __name__ == '__main__':
    main()
