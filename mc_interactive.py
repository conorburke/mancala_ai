from agent import MonteCarloNode
from mancala import GameState, Player
from datetime import datetime

game = GameState.new_game(7)

mc = MonteCarloNode(game)
mc.add_children()
print(mc.determine_win_ratio())
print(mc.win_counts)
print(mc.determine_win_ratio())
print(mc.children)

start_time = datetime.now()

game = GameState.new_game(7)
top_reversed = []
for i in range(5, -1, -1):
    top_reversed.append(game.board.top[i])
top_reversed.append(game.board.top[6])

print('welcome to mancala')
print('game size will be six moving holes and one mancala')
print('starting board is shown below')
print('top     ', top_reversed[0:game.board.size - 1])
print('bottom  ', game.board.bottom[0:game.board.size - 1])
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
        mc = MonteCarloNode(game)
        mc.add_children()
        move = mc.children.index(max(mc.children))
    # while game.board.__getattribute__(str(game.current_player))[move] == 0:
    #     move = random.randint(0, 5)
    game = game.apply_move(move)
    top_reversed = []
    for i in range(5, -1, -1):
        top_reversed.append(game.board.top[i])
    top_reversed.append(game.board.top[6])
    print('top     ', top_reversed[0:game.board.size - 1], '  points: ', top_reversed[game.board.size - 1:])
    print('bottom  ', game.board.bottom[0:game.board.size - 1], '  points: ', game.board.bottom[game.board.size - 1:])
if game.board.bottom[6] > game.board.top[6]:
    print('bottom wins!')
elif game.board.bottom[6] < game.board.top[6]:
    print('top wins!')
else:
    print('its a draw')

end_time = datetime.now()

print('time diff', end_time - start_time)
