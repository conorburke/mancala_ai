from mancala import Player
import random
import copy


class MonteCarloNode:
    def __init__(self, game_state, parent=None, player=Player.top, move=None):
        self.game_state = game_state
        self.parent = parent
        self.player = player
        self.win_counts = {
            'top': 0,
            'bottom': 0
        }
        self.num_rollouts = 0
        self.probabilities = []
        self.children = []
        self.move = move

    def add_child(self, game_state, player):
        # print('appending')
        move = self.get_random_valid_move(game_state)
        current_game_state = copy.deepcopy(self.game_state)
        new_game_state = current_game_state.apply_move(move)
        child_node = MonteCarloNode(new_game_state, self, player.other, move)
        # print('self children', self.children)
        self.children.append(child_node)
        return child_node

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

    # def play_move(self, move):
    #     new_game_state = self.game_state.apply_move(move)
    #     if new_game_state.determine_winner() == Player.top:
    #         self.win_counts['top'] += 1
    #     elif new_game_state.determine_winner() == Player.bottom:
    #         self.win_counts['bottom'] += 1
    #     self.num_rollouts += 1

    def determine_win_ratio(self, player):
        if self.num_rollouts > 0:
            if player == Player.top:
                return self.win_counts['top'] / self.num_rollouts
            else:
                return self.win_counts['bottom'] / self.num_rollouts
        return 0

    def determine_win_counts(self):
        top_wins = self.win_counts['top']
        bottom_wins = self.win_counts['bottom']
        for c in self.children:
            top_wins += c.win_counts['top']
            bottom_wins += c.win_counts['bottom']
        return self.determine_win_ratio(self.player)

    def get_random_valid_move(self, gs):
        move = random.randint(0, gs.board.size - 2)
        while self.is_invalid_move(gs, self.player, move):
            move = random.randint(0, gs.board.size - 2)
        return move

    def determine_best_move(self, game_state):
        move = self.probabilities.index(max(self.probabilities))
        while not game_state.valid_move(move):
            if max(self.probabilities) == 0:
                move = 0
                print('Player wins')
                exit()
                break
            self.probabilities[self.probabilities.index(max(self.probabilities))] = 0
            move = self.probabilities.index(max(self.probabilities))
        return move

    def is_invalid_move(self, gs, player, move):
        if gs.board.__getattribute__(str(player))[move] == 0:
            return True
        return False

    def can_add_child(self):
        # print('xxxxx', self.game_state.board.__getattribute__(str(self.player))[0:6])
        if sum(self.game_state.board.__getattribute__(str(self.player))[0:6]) == 0:
            return False
        return True


class ComprehensiveTree:
    def __init__(self):
        pass

    def construct_tree(self, node, game):
        # stop = datetime.datetime.now() + datetime.timedelta(seconds=1)
        # while stop > datetime.datetime.now():
        for m in range(0, game.board.size - 1):
        #     m = random.randint(0, game.board.size - 2)
        #     print('m', m)
            new_game_state = copy.deepcopy(game)
            if game.valid_move(m):
                # stop = datetime.datetime.now() + datetime.timedelta(seconds=30)
                updated_game_state = new_game_state.apply_move(m)
                # print('updated game state top', updated_game_state.board.top)
                # print('updated game state bottom', updated_game_state.board.bottom)
                child = node.add_child(updated_game_state, updated_game_state.current_player.other)
                # print('node children', node.children)
                # if len(node.children) > 1:
                    # print('node child', node.children[1])
                    # print('node', node)
                    # print('node child parent', node.children[1].parent)
                if child and not child.game_state.game_is_over():
                    self.construct_tree(child, updated_game_state)
                if child and child.game_state.game_is_over():
                    # print('winner', child.game_state.determine_winner())
                    if child.game_state.determine_winner() == Player.top:
                        child.win_counts['top'] += 1
                        while child.parent is not None:
                            child.parent.win_counts[str(Player.top)] += 1
                            child = child.parent
                        # print(child.win_counts)
                    elif child.game_state.determine_winner() == Player.bottom:
                        child.win_counts['bottom'] += 1
                        while child.parent is not None:
                            child.parent.win_counts[str(Player.bottom)] += 1
                            child = child.parent
                        # print(child.win_counts)


class MonteCarloTree:
    def __init__(self):
        pass

    def construct_tree(self, node, game, rounds):
        # stop = datetime.datetime.now() + datetime.timedelta(seconds=1)
        # while stop > datetime.datetime.now():
        for r in range(0, rounds):
            m = random.randint(0, game.board.size - 2)
            print('m', m)
            while not game.valid_move(m):
                m = random.randint(0, game.board.size - 2)
            updated_game_state = copy.deepcopy(game).apply_move(m)
            child = node.add_child(updated_game_state, updated_game_state.current_player.other)
            while not updated_game_state.game_is_over():
                m = random.randint(0, game.board.size - 2)
                while not updated_game_state.valid_move(m):
                    m = random.randint(0, game.board.size - 2)
                updated_game_state.apply_move(m)
                if child and not child.game_state.game_is_over():
                    self.construct_tree(child, copy.deepcopy(updated_game_state), rounds)
            if updated_game_state.game_is_over():
                # print('winner', child.game_state.determine_winner())
                if child.game_state.determine_winner() == Player.top:
                    child.win_counts['top'] += 1
                    while child.parent is not None:
                        child.parent.win_counts[str(Player.top)] += 1
                        child = child.parent
                    print(child.win_counts)
                elif child.game_state.determine_winner() == Player.bottom:
                    child.win_counts['bottom'] += 1
                    while child.parent is not None:
                        child.parent.win_counts[str(Player.bottom)] += 1
                        child = child.parent
                    print(child.win_counts)
