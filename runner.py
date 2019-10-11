from mancala import GameState
import random
from datetime import datetime

top_wins = 0
bottom_wins = 0
draws = 0
start_time = datetime.now()

for i in range(1, 1001):
    game = GameState.new_game(7)
    while not game.game_is_over():
        move = random.randint(0, 5)
        if sum(game.board.__getattribute__(str(game.current_player))[0:6]) == 0:
            game.current_player = game.current_player.other
        while game.board.__getattribute__(str(game.current_player))[move] == 0:
            move = random.randint(0, 5)
        game = game.apply_move(move)
        print('top     ', game.board.top)
        print('bottom  ', game.board.bottom)
    if game.board.bottom[6] > game.board.top[6]:
        bottom_wins += 1
        print('bottom wins!')
    elif game.board.bottom[6] < game.board.top[6]:
        top_wins += 1
        print('top wins!')
    else:
        draws += 1
        print('its a draw')

end_time = datetime.now()

print('top wins', top_wins)
print('bottom wins', bottom_wins)
print('draws', draws)
print('time diff', end_time - start_time)

