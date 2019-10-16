from agent import MonteCarloNode, ComprehensiveTree
from mancala import GameState, Player
import datetime


# def construct_tree(node, game):
#     for m in range(0, game.board.size - 1):
#         if game.valid_move(m):
#             new_game_state = game.apply_move(m)
#             child = node.add_child(new_game_state, new_game_state.current_player.other)
#             if len(node.children) > 4:
#                 print('node child', node.children[4])
#                 print('node', node)
#                 print('node child parent', node.children[4].parent.parent.parent)
#             if child:
#                 construct_tree(child, new_game_state)


game = GameState.new_game(4)
top_reversed = []
for i in range(game.board.size - 2, -1, -1):
    top_reversed.append(game.board.top[i])
top_reversed.append(game.board.top[game.board.size - 1])

print('welcome to mancala')
print('game size will be six moving holes and one mancala')
print('starting board is shown below')
print('top     ', top_reversed[0:game.board.size - 1])
print('bottom  ', game.board.bottom[0:game.board.size - 1])
choice = int(input('do you want top (1) or bottom(2): '))
player = Player.bottom if choice == 1 else Player.top

node = MonteCarloNode(game, None, player)
# construct_tree(node, game)
tree = ComprehensiveTree()
# stop = datetime.datetime.now() + datetime.timedelta(seconds=10)
# while datetime.datetime.now() < stop:
tree.construct_tree(node, game)
print('treeeeee')
print('tree', tree)
print('node', node)
print('node children', node.children)
for c in node.children:
    print(c.win_counts)
print(node.win_counts)
# print('node child', node.children[1].children)
# print('node', node)
# print('node child parent', node.children[0].parent)
# while node.can_add_child():
#     for m in range(0, game.board.size - 1):
#         print('current player', game.current_player)
#         print(game.board.size)
#         if game.is_valid_move(m):
#             child = node.add_child(game.apply_move(m), player, m)
#             print('child', child)
#             child.add_child()



#
# print(node)
# print(node.children)
# print(node.determine_win_counts())





#
# while not game.game_is_over():
#     if (agent == Player.top and game.current_player == Player.bottom) or (agent == Player.bottom and game.current_player == Player.top):
#         move = input("enter between 1 and 6: ")
#         move = int(move)
#         while move < 1 or move > 6 or not game.is_valid_move(move - 1):
#             move = input("enter between 1 and 6 (non zero): ")
#             move = int(move)
#         # remove array indexing consideration while playing
#         move -= 1
#     else:
#
# #         mc = MonteCarloNode(game, player=agent)
# #         mc.determine_win_probabilities()
# #         print(mc.probabilities)
# #         move = mc.determine_best_move(game)
# #     # while game.board.__getattribute__(str(game.current_player))[move] == 0:
# #     #     move = random.randint(0, 5)
# #     game = game.apply_move(move)
# #     top_reversed = []
# #     for i in range(5, -1, -1):
# #         top_reversed.append(game.board.top[i])
# #     top_reversed.append(game.board.top[6])
# #     print('top     ', top_reversed[0:game.board.size - 1], '  points: ', top_reversed[game.board.size - 1:])
# #     print('bottom  ', game.board.bottom[0:game.board.size - 1], '  points: ', game.board.bottom[game.board.size - 1:])
# # if game.determine_winner() == Player.bottom:
# #     print('bottom wins!')
# # elif game.determine_winner() == Player.top:
# #     print('top wins!')
# # else:
# #     print('its a draw')
#
# end_time = datetime.now()
#
# print('time diff', end_time - start_time)