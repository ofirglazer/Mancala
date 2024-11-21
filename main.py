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

def main():
    global board
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
        print("It's a tie!")

if __name__ == '__main__':
    main()