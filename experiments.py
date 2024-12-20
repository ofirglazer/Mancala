from mancala import Game
from mancala import STORE


def main(n_games=5):
    wins = [0, 0, 0]  # wins player 1, wins player 2, ties
    to_draw = False
    for _ in range(n_games):
        game = Game('minmax', 'minmax')
        end_state = game.play_game(to_draw)
        if end_state[STORE] > end_state[STORE * 2 + 1]:
            wins[0] += 1
        elif end_state[STORE] < end_state[STORE * 2 + 1]:
            wins[1] += 1
        else:
            wins[2] += 1
    print(f"Total wins rate is {wins}")


if __name__ == '__main__':
    main(100)
