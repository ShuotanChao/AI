import time
import matplotlib.pyplot as plt
from games import TicTacToe, Connect4
from players import RandomPlayer, MinMaxPlayer, QLearningPlayer, DefaultOpponent


def play(game, x_player, o_player, print_game=True):

    if print_game and game.get_class_name == "TicTacToe":
        game.print_board_nums()

    letter = x_player.letter
    while game.empty_squares():
        if letter == o_player.letter:
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(letter + f" makes a move to square {square}")
                game.print_board()
                print("")

            if game.current_winner:
                if print_game:
                    print(letter + " wins!")
                return letter

            letter = o_player.letter if letter == x_player.letter else x_player.letter

    if print_game:
        print("It's a tie!")


if __name__ == "__main__":
    game = "TicTacToe"
    game = "Connect4"
    r_player = RandomPlayer("R")
    start_time = time.time()
    o_player = MinMaxPlayer("O", "Connect4", depth=2)
    # d_player = DefaultOpponent("D", "O", "Connect4")
    q_player = QLearningPlayer("Q", 'Connect4')
    q_player.train(100000)

    num_games = 1000
    o_player_wins = 0
    # d_player_wins = 0
    q_player_wins = 0

    o_win_rate_history = []
    # d_win_rate_history = []
    q_win_rate_history = []
    tie_rate_history = []

    for i in range(1, num_games+1):
        t = Connect4()

        play(t, o_player, q_player, print_game=False)

        if t.current_winner == "O":
            o_player_wins += 1
        elif t.current_winner == "Q":
            q_player_wins += 1

        o_win_rate_history.append(o_player_wins / i)
        q_win_rate_history.append(q_player_wins / i)
        tie_rate_history.append((i - o_player_wins - q_player_wins) / i)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"Number of games played: {num_games}")
    print(f"Execution time: {total_time:.2f}s")
    print(f"O player win rate: {o_player_wins/num_games:.2f}")
    print(f"Q player win rate: {q_player_wins/num_games:.2f}")
    print(
        f"Tie rate: {(num_games - o_player_wins - q_player_wins)/num_games:.2f}")

    plt.plot(o_win_rate_history, label="O player win rate")
    plt.plot(q_win_rate_history, label="Q player win rate")
    plt.plot(tie_rate_history, label="Tie rate")
    plt.xlabel("Number of games")
    plt.ylabel("Win/Tie rate")
    plt.legend()
    plt.show()
