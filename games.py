import math
import random


class Connect4:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.turn = 'X'
        self.current_winner = None

    def get_class_name(self):
        return type(self).__name__

    def empty_squares(self):
        for b in self.board:
            if " " in b:
                return True
        return False

    def print_board(self):
        print('-----------------------------')
        for i in range(6):
            print('|', end='')
            for j in range(7):
                print(f' {self.board[i][j]} |', end='')
            print()
            print('-----------------------------')

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
        if self.winner(col, letter):
            self.current_winner = letter
            return True
        for row in range(5, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = letter
                break
        else:
            return False

        if self.winner(col, letter):
            self.current_winner = letter

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
        # check horizontal
        for i in range(6):
            for j in range(4):
                if self.board[i][j] == letter and \
                        self.board[i][j+1] == letter and \
                        self.board[i][j+2] == letter and \
                        self.board[i][j+3] == letter:
                    return True

        # check vertical
        for i in range(3):
            for j in range(7):
                if self.board[i][j] == letter and \
                        self.board[i+1][j] == letter and \
                        self.board[i+2][j] == letter and \
                        self.board[i+3][j] == letter:
                    return True

        # check diagonal (up-right)
        for i in range(3):
            for j in range(4):
                if self.board[i][j] == letter and \
                        self.board[i+1][j+1] == letter and \
                        self.board[i+2][j+2] == letter and \
                        self.board[i+3][j+3] == letter:
                    return True

        # check diagonal (up-left)
        for i in range(3):
            for j in range(3, 7):
                if self.board[i][j] == letter and \
                        self.board[i+1][j-1] == letter and \
                        self.board[i+2][j-2] == letter and \
                        self.board[i+3][j-3] == letter:
                    return True

        return False


class TicTacToe:
    '''
    Tic Tac Toe game
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

    def get_class_name(self):
        return type(self).__name__

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    def get_board_state(self):
        return ''.join(self.board)

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
