from mancala import Player
import copy
import random


class AlphaBetaPruner:
    def __init__(self, game_state, player=Player.top,
                 search_depth=10):
        self.game_state = copy.deepcopy(game_state)
        self.player = player
        self.search_depth = search_depth

    def evaluate_position(self, game_state):
        if self.player == Player.top:
            return float(game_state.board.top[-1] - game_state.board.bottom[-1]) * 5 #+ float(sum(game_state.board.top) - sum(game_state.board.bottom))
        else:
            return float(game_state.board.bottom[-1] - game_state.board.top[-1]) * 5 #+ float(sum(game_state.board.bottom) - sum(game_state.board.top))

    def is_invalid_move(self, game_state, player, move):
        if game_state.board.__getattribute__(str(player))[move] == 0:
            return True
        return False

    def get_random_valid_move(self):
        move = random.randint(0, self.game_state.board.size - 2)
        while self.is_invalid_move(self.game_state, self.player, move):
            move = random.randint(0, self.game_state.board.size - 2)
        return move

    def ab_max(self, game_state, depth, alpha, beta):
        if depth == 0:
            return self.evaluate_position(game_state)
        current_value = float("-inf")
        for m in range(game_state.board.size - 2, -1, -1):
            current_game_state = copy.deepcopy(game_state)
            if self.is_invalid_move(current_game_state, self.player, m):
                continue
            new_game_state = current_game_state.apply_move(m)
            if new_game_state.game_is_over():
                if new_game_state.determine_winner == self.player:
                    return float("inf")
                else:
                    continue
            if new_game_state.current_player == self.player:
                return self.ab_max(new_game_state, depth - 1, alpha, beta)
            possible_new_value = self.ab_min(new_game_state, depth - 1, alpha, beta)
            current_value = current_value if current_value > possible_new_value else possible_new_value
            if current_value >= beta:
                return current_value
            alpha = alpha if alpha > current_value else current_value
        return current_value

    def ab_min(self, game_state, depth, alpha, beta):
        if depth == 0:
            return self.evaluate_position(game_state)
        current_value = float("inf")
        for m in range(game_state.board.size - 2, -1, -1):
            current_game_state = copy.deepcopy(game_state)
            if self.is_invalid_move(current_game_state, self.player.other, m):
                continue
            new_game_state = current_game_state.apply_move(m)
            if new_game_state.game_is_over():
                if new_game_state.determine_winner != self.player:
                    return float("-inf")
                else:
                    continue
            if new_game_state.current_player != self.player:
                return self.ab_min(new_game_state, depth - 1, alpha, beta)
            possible_new_value = self.ab_max(new_game_state, depth - 1, alpha, beta)
            current_value = current_value if current_value < possible_new_value else possible_new_value
            if current_value <= alpha:
                return current_value
            beta = beta if beta < current_value else current_value
        return current_value

    def ab_prune(self, alpha=float("-inf"), beta=float("inf")):
        move = self.get_random_valid_move()
        for m in range(self.game_state.board.size - 2, -1, -1):
            current_game_state = copy.deepcopy(self.game_state)
            if self.is_invalid_move(current_game_state, self.player, m):
                continue
            new_game_state = current_game_state.apply_move(m)
            if new_game_state.game_is_over():
                if new_game_state.determine_winner == self.player:
                    return m
                else:
                    continue
            if new_game_state.current_player == self.player:
                current_value = self.ab_max(new_game_state, self.search_depth - 1, alpha, beta)
                if current_value < beta:
                    beta = current_value
                    move = m
            current_value = self.ab_min(new_game_state, self.search_depth - 1, alpha, beta)
            if current_value > alpha:
                alpha = current_value
                move = m
        return move

