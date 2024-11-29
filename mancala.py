import player_minmax
import player_human
import player_random


STORE = 6  # pointer of store pit


class Board:
    def __init__(self):
        # 6 pits per player (each with 4 stones initially), and 2 stores (Mancalas) for players.
        self.pits = [[4] * 6, [4] * 6]  # 2 players, 6 pits each
        self.pits[0].append(0)   # player 0 store
        self.pits[1].append(0)   # player 0 store
        self.turn = 0  # Player 0's turn starts first

    def draw(self):
        print("   ", end="")
        for i in range(5, -1, -1):
            print(str(self.pits[1][i]).rjust(2, ' '), end=" ")
        print("\n", self.pits[1][STORE], "                 ", self.pits[0][STORE])
        print("   ", end="")
        for i in range(0, 6):
            print(str(self.pits[0][i]).rjust(2, ' '), end=" ")
        print("\n")

    def switch_turns(self):
        # Switch turns between players
        self.turn = 1 - self.turn

    def valid_moves(self):
        valid_moves = list()
        for move in range(STORE):
            if self.is_valid_move(move):
                valid_moves.append(move)
        return valid_moves

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
            pit_index = (pit_index + 1) % 7  # Move to the next pit
            if pit_index == 0:
                side = 1 - side  # switch to other side after roll over to pit 0

            # handling stores during sow
            if pit_index == STORE:  # arriving at a store
                if side == current_player:  # player's store
                    self.pits[side][STORE] += 1
                    stones -= 1

                    if stones == 0:         # the stone in own store was the last
                        finish_in_store = True
                        break
            else:                   # regular 0-5 pit
                self.pits[side][pit_index] += 1
                stones -= 1

        # 3. take opponent stones if land on empty in own side
        if (side == current_player and self.pits[side][pit_index] == 1
                and not finish_in_store):  # last stone was put in empty pit
            self.pits[side][STORE] += self.pits[1-side][5 - pit_index] + 1  # opposite stones + last own stone
            self.pits[1 - side][5 - pit_index] = 0
            self.pits[side][pit_index] = 0

        # 4. switch player except when finish in own store
        if not finish_in_store:  # finished sowing in own store
            self.switch_turns()

    def check_game_over(self):
        # Game is over if one player has no stones left in their pits
        if sum(self.pits[0][1:STORE]) == 0:
            empty_side = 0
        elif sum(self.pits[1][1:STORE]) == 0:
            empty_side = 1
        else:
            return False

        for i in range(STORE):
            self.pits[empty_side][STORE] += self.pits[1 - empty_side][i]
            self.pits[1 - empty_side][i] = 0
        return True

    def get_board_state(self):
        # Returns the current state of the board, useful for AI
        return list([*self.pits[0], *self.pits[1], self.turn == 0])

        # # Returns the current state of the board, useful for displaying to the user
        # return {
        #     "player_1_pits": self.pits[0],
        #     "player_2_pits": self.pits[1],
        #     "player_1_store": self.stores[0],
        #     "player_2_store": self.stores[1]
        # }


class Game:
    def __init__(self, player0='human', player1='random'):
        self.board = Board()
        self.players = []
        if player0 == 'human':
            self.players.append(player_human.Player())
        elif player0 == 'random':
            self.players.append(player_random.Player())
        elif player0 == 'minmax':
            self.players.append(player_minmax.Player(0))
        else:
            raise Exception('Incorrect player0 type')
        if player1 == 'human':
            self.players.append(player_human.Player())
        elif player1 == 'random':
            self.players.append(player_random.Player())
        elif player0 == 'minmax':
            self.players.append(player_minmax.Player(1))
        else:
            raise Exception('Incorrect player1 type')


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
        state = self.board.get_board_state()
        if state[STORE] > state[2*STORE + 1]:
            return f"Player 1 wins! {state[STORE]}:{state[2*STORE + 1]}"
        elif state[STORE] < state[2*STORE + 1]:
            return f"Player 2 wins! {state[STORE]}:{state[2*STORE + 1]}"
        else:
            return f"It's a tie! {state[STORE]}:{state[2*STORE + 1]}"

    def play_game(self, to_draw=False):
        while True:
            if to_draw:
                self.board.draw()

            current_player = self.players[self.board.turn]
            print(f"Player {self.board.turn + 1} turn [{current_player.name}]")

            # Get move from player
            pit_index = current_player.act(self.board)
            if self.play_move(pit_index):
                print("Game Over!")
                print(self.get_winner())
                return self.board.get_board_state()


def main():
    to_draw = True
    game = Game('minmax', 'random')
    game.play_game(to_draw)


if __name__ == '__main__':
    main()
