import enum


class Player(enum.Enum):
    top = 1
    bottom = 2

    def __str__(self):
        return 'top' if self == Player.top else 'bottom'

    @property
    def other(self):
        return Player.top if self == Player.bottom else Player.bottom

class Tie:
    pass


class Board:
    def __init__(self, size=7):
        self.top = []
        self.bottom = []
        self.size = size


class GameState:
    def __init__(self, board, current_player=Player.bottom):
        self.board = board
        self.current_player = current_player
        self.is_over = False

    @classmethod
    def new_game(cls, size=7):
        board = Board(size)
        board.top = [4] * (size - 1)
        board.top.append(0)
        board.bottom = [4] * (size - 1)
        board.bottom.append(0)
        return GameState(board)

    def apply_move(self, position):
        if position == 6:
            return GameState(board=self.board, current_player=self.current_player)

        if position > (self.board.size - 1):
            raise IndexError("must be smaller than board size minus end hole")

        beads_to_move = self.board.__getattribute__(str(self.current_player))[position]

        self.board.__getattribute__(str(self.current_player))[position] = 0

        for bead in range(1, beads_to_move + 1):
            counter = position + bead

            if counter < self.board.size:
                self.board.__getattribute__(str(self.current_player))[counter] += 1
                # check if last bead played and in empty hole
                if counter != 6 and \
                        self.board.__getattribute__(str(self.current_player))[counter] == 1 and \
                        bead == beads_to_move:
                    # print('bead', bead)
                    # print('beads to move', beads_to_move)
                    self.board.__getattribute__(str(self.current_player))[self.board.size - 1] \
                        += self.board.__getattribute__(str(self.current_player.other))[self.board.size - 2 - counter]
                    self.board.__getattribute__(str(self.current_player.other))[self.board.size - 2 - counter] = 0
            elif self.board.size <= counter < (self.board.size * 2):
                if self.board.__getattribute__(str(self.current_player.other))[counter - self.board.size] == 6:
                    # don't add beads to opponents mancala (end_hole)
                    counter += 1
                    self.board.__getattribute__(str(self.current_player))[counter - self.board.size * 2] += 1
                    bead += 1
                else:
                    # print(self.board.__getattribute__(str(self.current_player.other))[counter - self.board.size])
                    self.board.__getattribute__(str(self.current_player.other))[counter - self.board.size] += 1
            elif (self.board.size * 2) <= counter < (self.board.size * 3):
                self.board.__getattribute__(str(self.current_player))[counter - self.board.size * 2] += 1
                # check if last bead played and in empty hole
                if self.board.__getattribute__(str(self.current_player))[counter - self.board.size * 2] == 1 and \
                        bead == beads_to_move:
                    # print('bead', bead)
                    # print('beads to move', beads_to_move)
                    self.board.__getattribute__(str(self.current_player))[self.board.size - 1] \
                        += self.board.__getattribute__(str(self.current_player.other))[self.board.size - 2 - (counter - self.board.size * 2)]
                    self.board.__getattribute__(str(self.current_player.other))[self.board.size - 2 - (counter - self.board.size * 2)] = 0
            elif (self.board.size * 3) <= counter < (self.board.size * 4):
                if self.board.__getattribute__(str(self.current_player.other))[counter - self.board.size * 3] == 6:
                    # don't add beads to opponents mancala (end_hole)
                    counter += 1
                    self.board.__getattribute__(str(self.current_player))[counter - self.board.size * 4] += 1
                    bead += 1
                else:
                    self.board.__getattribute__(str(self.current_player.other))[counter - self.board.size * 3] += 1
            else:
                self.board.__getattribute__(str(self.current_player))[counter - self.board.size * 4] += 1

        # if the player ends with the final bead in their score bin, they go again
        if (position + beads_to_move) % 6 == 0 and (position + beads_to_move) % 12 != 0:
            return GameState(board=self.board, current_player=self.current_player)

        return GameState(board=self.board, current_player=self.current_player.other)

    def game_is_over(self):
        end_hole = self.board.size - 1
        halfway = self.board.size * 4 - 4
        if sum(self.board.top[0:end_hole]) == 0 or sum(self.board.bottom[0:end_hole]) == 0 \
                or self.board.top[end_hole] > halfway or self.board.bottom[end_hole] > halfway:
            if sum(self.board.top[0:end_hole]) == 0:
                self.board.bottom[end_hole] += sum(self.board.bottom[0:6])
                for i in range(0, end_hole):
                    self.board.bottom[i] = 0
            if sum(self.board.bottom[0:end_hole]) == 0:
                self.board.top[end_hole] += sum(self.board.top[0:6])
                for i in range(0, end_hole):
                    self.board.top[i] = 0
            return not self.is_over
        return self.is_over

    def determine_winner(self):
        if self.game_is_over():
            if self.board.top[self.board.size - 1] > self.board.bottom[self.board.size - 1]:
                return Player.top
            elif self.board.bottom[self.board.size - 1] > self.board.top[self.board.size - 1]:
                return Player.bottom
            else:
                return Tie()
        return None

    def concede(self):
        self.over = True

    def is_valid_move(self, position):
        print('current player)', self.current_player)
        if self.board.__getattribute__(str(self.current_player))[position] == 0:
            return False
        return True
