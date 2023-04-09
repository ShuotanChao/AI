
from games import TicTacToe, Connect4
from players import RandomPlayer, MinMaxPlayer, QLearningPlayer, DefaultOpponent


def play(game, x_player, o_player, print_game=True):
    '''
    游戏的主要逻辑，功能是让两个玩家轮流下棋，直到游戏结束，然后返回获胜者的字母或者平局的消息。

    参数：

    game：一个游戏实例，存储了游戏的状态和棋盘等信息。
    x_player：一个玩家实例，代表X方。
    o_player：一个玩家实例，代表O方。
    print_game：一个布尔值，表示是否在控制台输出游戏过程。

    The main logic of the game is to have two players take turns playing chess until the game is over, and then return the winner's letter or a draw message.
    Parameters:
    Game: A game instance that stores information such as the status of the game and the chessboard.
    x_ Player: A player instance representing the X side.
    o_ Player: A player instance representing the O side.
    print_ Game: A Boolean value indicating whether to output the game process on the console.
    '''

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
    # x_player = HumanPlayer("X")
    # r_player = RandomPlayer("R")

    # o_player = AIPlayer("O", "Connect4")
    # q_player = QLearningPlayer("Q", 'Connect4')
    game = "Connect4"
    if game == "TicTacToe":
        t = TicTacToe()
        o_player = MinMaxPlayer("O", "TicTacToe")
        q_player = QLearningPlayer("Q", 'TicTacToe')
    elif game == "Connect4":
        t = Connect4()
        o_player = MinMaxPlayer("O", "Connect4")
        q_player = QLearningPlayer("Q", 'Connect4')
    else:
        raise ValueError("game must be TicTacToe or Connect4")

    # q_player.train(20)
    # play(t, q_player, o_player, print_game=True)
    # t = TicTacToe()
    t = Connect4()
    d_player = DefaultOpponent("D", "R", "Connect4")
    r_player = RandomPlayer("R")
    play(t, r_player, d_player, print_game=True)
