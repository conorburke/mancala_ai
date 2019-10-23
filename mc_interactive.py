from agent import MonteCarloNode
from mancala import GameState, Player
from datetime import datetime

game = GameState.new_game(7)

# mc = MonteCarloNode(game)
# mc.add_children()
# print(mc.determine_win_ratio())
# print(mc.win_counts)
# print(mc.determine_win_ratio())
# print(mc.children)

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
# print('you are the bottom player...')
choice = int(input('do you want top (1) or bottom(2): '))
agent = Player.bottom if choice == 1 else Player.top
while not game.game_is_over():
    if (agent == Player.top and game.current_player == Player.bottom) or (agent == Player.bottom and game.current_player == Player.top):
        move = input("enter between 1 and 6: ")
        move = int(move)
        while move < 1 or move > 6 or not game.valid_move(move - 1):
            move = input("enter between 1 and 6 (non zero): ")
            move = int(move)
        # remove array indexing consideration while playing
        move -= 1
    else:
        mc = MonteCarloNode(game_state=game, player=agent)
        mc.determine_win_probabilities()
        print(mc.probabilities)
        move = mc.determine_best_move(game)
    # while game.board.__getattribute__(str(game.current_player))[move] == 0:
    #     move = random.randint(0, 5)
    game = game.apply_move(move)
    top_reversed = []
    for i in range(5, -1, -1):
        top_reversed.append(game.board.top[i])
    top_reversed.append(game.board.top[6])
    print('top     ', top_reversed[0:game.board.size - 1], '  points: ', top_reversed[game.board.size - 1:])
    print('bottom  ', game.board.bottom[0:game.board.size - 1], '  points: ', game.board.bottom[game.board.size - 1:])
if game.determine_winner() == Player.bottom:
    print('bottom wins!')
elif game.determine_winner() == Player.top:
    print('top wins!')
else:
    print('its a draw')

end_time = datetime.now()

print('time diff', end_time - start_time)
