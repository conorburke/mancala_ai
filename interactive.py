from mancala import GameState, Player
import random
from datetime import datetime

top_wins = 0
bottom_wins = 0
draws = 0
start_time = datetime.now()

game = GameState.new_game(7)
top_reversed = []
for i in range(5, -1, -1):
    top_reversed.append(game.board.top[i])
top_reversed.append(game.board.top[6])

print('welcome to mancala')
print('game size will be six moving holes and one mancala')
print('starting board is shown below')
print('top     ', top_reversed[0:game.size - 1])
print('bottom  ', game.board.bottom[0:game.size - 1])
print('you are the bottom player...')
while not game.game_is_over():
    if game.current_player == Player.bottom:
        move = input("enter between 1 and 6: ")
        move = int(move)
        while move < 1 or move > 6:
            move = input("enter between 1 and 6: ")
            move = int(move)
        move -= 1
    else:
        move = random.randint(0, 5)
    # if sum(game.board.__getattribute__(str(game.current_player))[0:6]) == 0:
    #     game.current_player = game.current_player.other
    while game.board.__getattribute__(str(game.current_player))[move] == 0:
        move = random.randint(0, 5)
    game = game.apply_move(move)
    top_reversed = []
    for i in range(5, -1, -1):
        top_reversed.append(game.board.top[i])
    top_reversed.append(game.board.top[6])
    print('top     ', top_reversed[0:game.size - 1], '  points: ', top_reversed[game.size - 1:])
    print('bottom  ', game.board.bottom[0:game.size - 1], '  points: ', game.board.bottom[game.size - 1:])
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
