import random
import copy

from games import Connect4, TicTacToe


class Player:
    '''
    Player base class
    Function:
         __init__(self, letter): Class initialization function that initializes the type of chessman (letter).
        get_move(self, game): Returns an integer indicating the location of the next step.
    '''

    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class DefaultOpponent(Player):

    def __init__(self, letter, adversary_letter, game_type):
        super().__init__(letter)
        self.game_type = game_type
        self.adversary_letter = adversary_letter

    def get_move(self, game):
        if self.game_type == "Connect4":
            return self.connect4_move(game, self.letter)
        elif self.game_type == "TicTacToe":
            return self.tic_tac_toe_move(game, self.letter)

    def connect4_move(self, game, player):
        # Check if there are any moves to create a four-in-a-row
        for col in range(len(game.board[0])):
            if game.make_move(col, player):
                if game.winner(col, player):
                    game.repeal_move(col)
                    return col
                game.repeal_move(col)

        # Check if there are any moves to block the player's attempts
        for col in range(len(game.board[0])):
            if game.make_move(col, self.adversary_letter):
                if game.winner(col, self.adversary_letter):
                    game.repeal_move(col)
                    return col
                game.repeal_move(col)

        # Choose a random valid move
        valid_moves = game.available_moves()
        return random.choice(valid_moves)

    def tic_tac_toe_move(self, game, player):
        # Check if there are any moves to create a three-in-a-row
        for i in range(len(game.board)):
            if game.board[i] == " ":
                game.board[i] = player
                if game.winner(i, player):
                    game.repeal_move(i)
                    return i
                game.repeal_move(i)

        # Check if there are any moves to block the player's attempts
        for i in range(len(game.board)):
            if game.board[i] == " ":
                game.board[i] = self.adversary_letter
                if game.winner(i, self.adversary_letter):
                    game.repeal_move(i)
                    return i
                game.repeal_move(i)

        # Choose a random valid move
        valid_moves = game.available_moves()
        return random.choice(valid_moves)


class RandomPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        return random.choice(game.available_moves())


class MinMaxPlayer(Player):
    '''
    __init__(self, letter): The initialization function accepts a parameter letter representing the player's tag.

    get_move(self, game): Obtain the next step of the AI player. If the number of spaces on the current game board is 9,
    to set it the first step, AI randomly selects a walkable method. Otherwise, use the minimax algorithm to calculate the best 
    walking method and return the location of the best walking method.

    minimax(self, state, player, alpha=float('-inf'), beta=float('inf')): The implementation of minimax algorithm.
    The input parameters are game state, current player, alpha value, and beta value. Calculates the optimal solution through recursive search and returns a dictionary containing the optimal location and corresponding score.
    If there is a winner in the current state, return the winner's score; If tied, return 0 points; Otherwise, traverse all feasible walks, calculate scores, and update the optimal solution.
    If the current player is max_ Player, choose the walking method with the highest score; If the current player is another_ Player, choose the walking method with the lowest score.
    At the same time, the alpha beta pruning optimization algorithm is used to reduce search space and improve algorithm efficiency.
    '''

    def heuristic(self, state, player):
        opponent = 'O' if player == 'X' else 'X'
        score = 0
        n = int(len(state.board)**0.5)

        def evaluate_sequence(sequence):
            nonlocal score
            if sequence.count(player) == 3:
                score += 100
            elif sequence.count(player) == 2 and sequence.count(opponent) == 0:
                score += 1
            elif sequence.count(opponent) == 3:
                score -= 100

        # Check rows
        for row in range(n):
            row_symbols = [state.board[row * n + col] for col in range(n)]
            evaluate_sequence(row_symbols)

        # Check columns
        for col in range(n):
            column_symbols = [state.board[row * n + col] for row in range(n)]
            evaluate_sequence(column_symbols)

        # Check diagonals
        diagonal1 = [state.board[i * n + i] for i in range(n)]
        diagonal2 = [state.board[i * n + (n - i - 1)] for i in range(n)]

        evaluate_sequence(diagonal1)
        evaluate_sequence(diagonal2)

        return score

    def __init__(self, letter, game_name, depth=4):
        super().__init__(letter)
        self.game_name = game_name
        self.depth = depth

    def get_move(self, game):
        if len(game.available_moves()) == 9 and self.game_name == 'TicTacToe':
            return random.choice(game.available_moves())
        elif len(game.available_moves()) == 42 and self.game_name == 'Connect4':
            return random.choice(game.available_moves())
        else:
            return self.minimax(game, self.letter, self.depth)['position']

    def minimax(self, state, player, depth, alpha=float('-inf'), beta=float('inf')):
        max_player = self.letter
        other_player = 'O'
        if depth == 0:
            return {'position': None, 'score': self.heuristic(state, max_player)}
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': float('-inf')}
            available_moves = state.available_moves()
            for possible_move in available_moves:
                state.make_move(possible_move, player)
                sim_score = self.minimax(
                    state, other_player, depth-1, alpha, beta)
                # state.board[possible_move] = " "
                state.repeal_move(possible_move)
                state.current_winner = None
                sim_score['position'] = possible_move

                if sim_score['score'] > best['score']:
                    best = sim_score

                alpha = max(alpha, best['score'])
                if alpha >= beta:
                    break
            return best

        else:
            best = {'position': None, 'score': float('inf')}
            available_moves = state.available_moves()
            for possible_move in available_moves:
                state.make_move(possible_move, player)
                sim_score = self.minimax(
                    state, max_player, depth-1, alpha, beta)
                # state.board[possible_move] = " "
                state.repeal_move(possible_move)
                state.current_winner = None
                sim_score['position'] = possible_move

                if sim_score['score'] < best['score']:
                    best = sim_score

                beta = min(beta, best['score'])
                if alpha >= beta:
                    break
            return best


class QLearningPlayer(Player):
    '''
    __init__(self, letter, learning_rate=0.3, discount_factor=0.9, exploration_rate=0.1):
    Initialize the object of the QLearningPlayer. Letter is a chess piece ("X" or "O") used by players, 
    learning_ Rate is the learning rate, discount_ factor 
    Is the discount factor, exploration_ Rate is the exploration rate. 
    The default learning rate is 0.3, the discount factor is 0.9, and the exploration rate is 0.1.
    get_ Move (self, game): Given the current status game of the jigsaw puzzle, 
    the player's next chess position is determined based on the current Q table and exploration rate.
    get_ best_ Move (self, game): Select the walking method with the highest Q value among the currently available walking methods. 
    If there are multiple walking methods with the same Q value, randomly choose one.
    update_ q_ Table (self, game, old_state, new_state, move, reward): Updates the Q table based on the Q-Learning algorithm.
    old_ State and new_ "State" refers to the status of the game before and after the update, 
    and "move" refers to the status of the player in "old"_ The position of a chess piece under state, reward, is the reward value.
    Train (self, num_episodes): Use the Q-Learning algorithm to train the model. 
    During training, the QLearningPlayer will play a tic-tacs game with another AI Player,
    Training num_ Episodes rounds. In each round, the player calls get_ The move method selects the next chess piece position,
    And by calling update_ q_ The table method updates the Q table.

    '''

    def __init__(self, letter, game_name, learning_rate=0.3, discount_factor=0.9, exploration_rate=0.1):
        super().__init__(letter)
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.game_name = game_name

    def get_move(self, game):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(game.available_moves())
        else:
            move = self.get_best_move(game)
            return move

    def get_best_move(self, game):
        available_moves = game.available_moves()
        max_value = -float('inf')
        best_moves = []
        for move in available_moves:
            game.make_move(move, self.letter)
            state = game.get_board_state()
            value = self.q_table.get(state, 0)
            if value > max_value:
                max_value = value
                best_moves = [move]
            elif value == max_value:
                best_moves.append(move)
            # game.board[move] = " "
            game.repeal_move(move)
        if len(best_moves) > 0:
            return random.choice(best_moves)
        else:
            return None

    def update_q_table(self, game, old_state, new_state, move, reward):
        old_q_value = self.q_table.get((old_state, move), 0)
        try:
            best_next_move_value = max([self.q_table.get(
                (new_state, next_move), 0) for next_move in game.available_moves()])
        except:
            best_next_move_value = 0.0
        new_q_value = (1 - self.learning_rate) * old_q_value + self.learning_rate * \
            (reward + self.discount_factor * best_next_move_value)
        self.q_table[(old_state, move)] = new_q_value

    def train(self, num_episodes):
        for i in range(num_episodes):
            if self.game_name == "TicTacToe":
                t = TicTacToe()
            elif self.game_name == "Connect4":
                t = Connect4()
            else:
                raise ValueError("game must be TicTacToe or Connect4")

            current_player = self
            another_player = AIPlayer("O", self.game_name)
            while t.current_winner is None:
                current_state = t.get_board_state()
                if not ' ' in current_state:
                    break
                move = current_player.get_move(t)
                t.make_move(move, current_player.letter)
                # next_state = t.get_board_state()
                reward = 0
                if t.current_winner is not None:
                    if t.current_winner == self.letter:
                        reward = 1
                    else:
                        reward = -1
                if current_player == self:
                    self.update_q_table(
                        t, current_state, t.get_board_state(), move, reward)
                if current_player == self:
                    current_player = another_player
                else:
                    current_player = self


class AIPlayer(Player):
    '''
    AIPlayer class used for training the Q-learning algorithm
    '''

    def __init__(self, letter, game_name, q_table=None, learning_rate=0.3, discount_factor=0.9, exploration_rate=0.1):
        super().__init__(letter)
        self.q_table = q_table or {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.game_name = game_name

    def get_move(self, game):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(game.available_moves())
        else:
            move = self.get_best_move(game)
            return move

    def get_best_move(self, game):
        available_moves = game.available_moves()
        max_value = -float('inf')
        best_moves = []
        for move in available_moves:
            game.make_move(move, self.letter)
            state = game.get_board_state()
            value = self.q_table.get(state, {}).get(move, 0)
            if value > max_value:
                max_value = value
                best_moves = [move]
            elif value == max_value:
                best_moves.append(move)
            game.repeal_move(move)
        if len(best_moves) > 0:
            return random.choice(best_moves)
        else:
            return None

    def update_q_table(self, game, old_state, new_state, move, reward):
        old_q_value = self.q_table.get(old_state, {}).get(move, 0)
        try:
            best_next_move_value = max(self.q_table.get(
                new_state, {}).values())
        except:
            best_next_move_value = 0.0
        new_q_value = (1 - self.learning_rate) * old_q_value + self.learning_rate * \
            (reward + self.discount_factor * best_next_move_value)
        self.q_table.setdefault(old_state, {})[move] = new_q_value

    def train(self, num_episodes):
        for i in range(num_episodes):
            if self.game_name == "TicTacToe":
                t = TicTacToe()
            elif self.game_name == "Connect4":
                t = Connect4()
            else:
                raise ValueError("game must be TicTacToe or Connect4")

            current_player = self
            another_player = AIPlayer(
                "O", self.game_name, q_table=self.q_table, exploration_rate=0)
            while t.current_winner is None:
                current_state = t.get_board_state()
                if not ' ' in current_state:
                    break
                move = current_player.get_move(t)
                t.make_move(move, current_player.letter)
                next_state = t.get_board_state()
                reward = 0
                if t.current_winner is not None:
                    if t.current_winner == self.letter:
                        reward = 1
                    else:
                        reward = -1
                if current_player == self:
                    self.update_q_table(
                        t, current_state, next_state, move, reward)
                if current_player == self:
                    current_player = another_player
                else:
                    current_player = self
