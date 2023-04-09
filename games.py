import math
import random


class Connect4:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.turn = 'X'
        self.current_winner = None

    @staticmethod
    def get_class_name(self):
        return type(self).__name__

    def empty_squares(self):
        for b in self.board:
            if " " in b:
                return True
        return False

    def print_board(self):
        print('-------------')
        for i in range(6):
            print('|', end='')
            for j in range(7):
                print(f' {self.board[i][j]} |', end='')
            print()
            print('-------------')

    def get_board_state(self):
        state = ""
        for b in self.board:
            for c in b:
                state += c
        return state

    def available_moves(self):
        moves = []
        for j in range(7):
            if self.board[0][j] == ' ':
                moves.append(j)
        return moves

    def make_move(self, col, letter):
        row = 5
        while row >= 0:
            if self.board[row][col] == ' ':
                self.board[row][col] = letter
                if self.winner(col, letter):
                    self.current_winner = letter
                break
            row -= 1
        else:
            print('Column is full!')
            return False

        return True

    def repeal_move(self, move):
        for i in range(6):
            if self.board[i][move] != ' ':
                self.board[i][move] = ' '
                break

    def num_empty_squares(self):
        count = 0
        for b in self.board:
            for c in b:
                if c == ' ':
                    count += 1
        return count

    def winner(self, col, letter):
        row = -1
        while row < 5 and self.board[row+1][col] == ' ':
            row += 1

        # check horizontal
        count = 0
        for j in range(4):
            if col + j > 6:
                break
            if self.board[row][col+j] == letter:
                count += 1
            else:
                break
        if count == 4:
            return True

        # check vertical
        count = 0
        for i in range(4):
            if row + i > 5:
                break
            if self.board[row+i][col] == letter:
                count += 1
            else:
                break
        if count == 4:
            return True

        # check diagonal up-right
        count = 0
        for i, j in zip(range(3, -1, -1), range(4)):
            if row - i < 0 or col + j > 6:
                break
            if self.board[row-i][col+j] == letter:
                count += 1
            else:
                break
        if count == 4:
            return True

        # check diagonal up-left
        count = 0
        for i, j in zip(range(3, -1, -1), range(3, -1, -1)):
            if row - i < 0 or col - j < 0:
                break
            if self.board[row-i][col-j] == letter:
                count += 1
            else:
                break
        if count == 4:
            return True

        return False


class TicTacToe:
    '''
    Tic Tac Toe game

    各函数的功能：
        __init__(self): 类的初始化函数，初始化棋盘（一个长度为9，元素为" "的列表）和当前赢家（初始值为None）。
        print_board(self): 打印当前棋盘状态。
        get_board_state(self): 返回当前棋盘状态的字符串表示。
        print_board_nums(): 打印棋盘编号（从0到8）。
        available_moves(self): 返回一个列表，包含棋盘上所有可用的位置。
        empty_squares(self): 返回一个布尔值，表示棋盘上是否有空位。
        num_empty_squares(self): 返回棋盘上空位的数量。
        make_move(self, square, letter): 在给定的位置square上下letter的棋子，并判断是否有胜者。
            如果下完后有胜者，更新当前赢家为letter，并返回True；否则返回False。
        winner(self, square, letter): 检查在位置square下letter是否赢得了比赛。
            首先检查所在行是否全部为letter，其次检查所在列是否全部为letter，最后检查对角线是否全部为letter。
            如果有一种情况成立，则返回True，否则返回False。

    Functions of each function:
    __ init__ (self): Class initialization function that initializes the chessboard (a list with a length of 9 and an element of "") and the current winner (with an initial value of None).
    print_ Board (self): Print the current checkerboard status.
    get_ board_ State (self): Returns a string representation of the current checkerboard state.
    print_ board_ Nums(): Print the checkerboard number (from 0 to 8).
    available_ Moves (self): Returns a list of all available positions on the chessboard.
    empty_ Squares (self): Returns a Boolean value indicating whether there are empty spaces on the chessboard.
    num_ empty_ Squares (self): Returns the number of empty spaces on the chessboard.
    make_ Move (self, square, letter): Move up and down letter pieces at a given position square, and determine whether there is a winner.
    If there is a winner after the placement, update the current winner to letter and return to True; Otherwise, it returns False.
    Winner (self, square, letter): Checks whether letter has won the competition under position square.
    First, check whether all the rows are letters, then check whether all the columns are letters, and finally check whether all the diagonal lines are letters.
    Returns True if one of the conditions is true, otherwise returns False.
    '''

    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_winner = None

    @staticmethod
    def get_class_name(self):
        return type(self).__name__

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    def get_board_state(self):
        return ''.join(self.board)

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j*3, (j+1)*3)]
                        for j in range(3)]
        for row in number_board:
            print("| " + " | ".join(row) + " |")

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def empty_squares(self):
        return " " in self.board

    def num_empty_squares(self):
        return self.board.count(" ")

    def repeal_move(self, square):
        self.board[square] = " "
        self.current_winner = None

    def make_move(self, square, letter):
        if self.board[square] == " ":
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True

        # check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # check diagonal
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        # no winner
        return False
