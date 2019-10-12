from mancala import Player
import random
import copy


class MonteCarloNode:
    def __init__(self, game_state, parent=None):
        self.game_state = game_state
        self.parent = parent
        self.win_counts = {
            'top': 0
        }
        self.num_rollouts = 0
        self.children = []

    def add_children(self):
        for i in range(0, self.game_state.board.size - 1):
            self.win_counts['top'] = 0
            self.num_rollouts = 0
            for j in range(1, 101):
                current_game_state = copy.deepcopy(self.game_state)
                new_game_state = current_game_state.apply_move(i)
                # print(new_game_state)
                while not new_game_state.game_is_over():
                    move = random.randint(0, 5)
                    while new_game_state.board.__getattribute__(str(new_game_state.current_player))[move] == 0:
                        move = random.randint(0, 5)
                    new_game_state = new_game_state.apply_move(move)
                    # print('top     ', new_game_state.board.top)
                    # print('bottom  ', new_game_state.board.bottom)
                if new_game_state.determine_winner() == Player.top:
                    self.win_counts['top'] += 1
                self.num_rollouts += 1
            self.children.append(self.determine_win_ratio())

    def determine_win_ratio(self):
        if self.num_rollouts > 0:
            return self.win_counts['top'] / self.num_rollouts
        return 0