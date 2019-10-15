from mancala import Player
import random
import copy


class MonteCarloNode:
    def __init__(self, game_state, parent=None, player=Player.top, move=0):
        self.game_state = game_state
        self.parent = parent
        self.player = player
        self.move = move
        self.win_counts = {
            'top': 0,
            'bottom': 0
        }
        self.num_rollouts = 0
        self.probabilities = []
        self.children = []

    def add_child(self, game_state, parent, player, move):
        pass

    def determine_win_probabilities(self):
        for i in range(0, self.game_state.board.size - 1):
            self.win_counts = {
                'top': 0,
                'bottom': 0
            }
            self.num_rollouts = 0
            for j in range(1, 1001):
                current_game_state = copy.deepcopy(self.game_state)
                new_game_state = current_game_state.apply_move(i)
                # print(new_game_state)
                while not new_game_state.game_is_over():
                    move = self.get_random_valid_move(new_game_state)
                    new_game_state = new_game_state.apply_move(move)
                    # print('top     ', new_game_state.board.top)
                    # print('bottom  ', new_game_state.board.bottom)
                if new_game_state.determine_winner() == Player.top:
                    self.win_counts['top'] += 1
                elif new_game_state.determine_winner() == Player.bottom:
                    self.win_counts['bottom'] += 1
                self.num_rollouts += 1
            self.probabilities.append(self.determine_win_ratio(self.player))

    def determine_win_ratio(self, player):
        if self.num_rollouts > 0:
            if player == Player.top:
                return self.win_counts['top'] / self.num_rollouts
            else:
                return self.win_counts['bottom'] / self.num_rollouts
        return 0

    def get_random_valid_move(self, game_state):
        move = random.randint(0, 5)
        while game_state.board.__getattribute__(str(self.player))[move] == 0:
            move = random.randint(0, 5)
        return move

    def determine_best_move(self, game_state):
        move = self.probabilities.index(max(self.probabilities))
        while not game_state.is_valid_move(move):
            if max(self.probabilities) == 0:
                move = 0
                print('Player wins')
                exit()
                break
            self.probabilities[self.probabilities.index(max(self.probabilities))] = 0
            move = self.probabilities.index(max(self.probabilities))
        return move


class MonteCarloAgent:
    pass