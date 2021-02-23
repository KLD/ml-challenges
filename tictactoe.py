import numpy as np
import random
import json
from os import path


memoryPath = "asskicker7.json"
import pandas as pd
import csv
import json 

newRow = []

def start_game() -> int:
    board = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    player = -1
    turn = 0
    newRow = []

    while not did_win(board, player) and turn < 9:
        turn += 1
        # print_board(board)
        player *= -1
        next = play_turn(board * player, player, turn)

        # print('player {} picked {}'.format(board_fills[player], next))
        board[next] = player

    # print_board(board)
    # print("\n")
    if did_win(board, 1):
        # print("X won")
        return 1
    elif did_win(board, -1):
        # print("O won")
        return -1
    else:
        # print("Tie")
        return 0

# 0, 1, 2
# 3, 4, 5
# 6, 7, 8

def did_win(board, player_sign) -> bool:
    for i in range(3):
        if(board[i*3] == board[(i*3)+1] == board[(i*3)+2] == player_sign):
            return True

        if(board[i] == board[i+3] == board[i+6] == player_sign):
            return True

    if(board[0] == board[4] == board[8] == player_sign):
        return True

    if(board[2] == board[4] == board[6] == player_sign):
        return True
    return False

board_fills = [' ', 'X', 'O']

def print_board(board):
    pass
    for i in range(9):
        print(board_fills[board[i]], end='|' if i % 3 != 2 else "\n")
    print("\n")
    print("-"*10)


def play_turn(board, player, turn) -> int:
    # if player == 1:
    # i = random.randint(0, 8)
    # while board[i] != 0:
    #     i = random.randint(0, 8)
    # return i
    # print_board(board)
    # return int(input('Enter your spot: '))

    # game_states = state_variation(to_game_state(board))
    game_state = to_game_state(board)

    global memory
    # for game_state in game_states:
    if not game_state in memory:
        memory[game_state] = [10 if i == 0 else 0 for i in board]
        # continue

    v = max(memory[game_state])

    indexes = [index
               for (index, value) in enumerate(memory[game_state]) if value == v]

    i = indexes[random.randint(0, len(indexes)-1)]

    # i = random.randint(0, 8)
    # while board[i] != 0:
    #     i = random.randint(0, 8)

    if player == 1:
        path_x.append({
            'state': game_state,
            'choice': i
        })
    else:
        path_o.append({
            'state': game_state,
            'choice': i
        })

    newRow.append(i)
    return i


def to_game_state(board):
    return "".join(["{}".format(i + 1) for i in board])


def simulate():
    global path_x, path_o, memory, memoryPath

    if path.exists(memoryPath):
        file = open(memoryPath, "r")
        memory = json.loads(file.read())
        file.close()
    else:
        memory = {}

    # wins = 0
    # loses = 0
    history = []

    max_epoc = 500000
    for i in range(max_epoc):
        path_x = []
        path_o = []

        if i % (max_epoc/100) == 0:
            print("%{:2}".format(i / (max_epoc/100)))

        results = start_game()
        for i, p in enumerate(path_o):
            memory[p['state']][p['choice']] = max(min(
                memory[p['state']][p['choice']] * (1.0+(0.5/(4-i))) if results == -1 else 1.0+(
                    0.5/(4-i)) if results == 0 else 1.0-(0.5/(4-i)), 20), 0.01)
        for i, p in enumerate(path_x):
            memory[p['state']][p['choice']] = max(min(
                memory[p['state']][p['choice']] * 1.0+(0.5/(5-i)) if results == 1 else 1 if results == 0 else 1 - (0.2/(5-i)), 20)/(5-i), 0.01)

        # if results == 1:
        #     wins += 1
        # elif results == -1:
        #     loses += 1
        # history.append("{:2f}".format(wins/(loses+wins)))

    f = open(memoryPath, "w")
    f.write(json.dumps(memory, indent=2))
    f.close()


def state_variation(s):
    p = []

    p.append(s)
    p.append(rotate_90(s))
    p.append(rotate_180(s))
    p.append(rotate_270(s))

    h = flip_horizontal(s)
    p.append(h)
    p.append(rotate_90(h))
    p.append(rotate_180(h))
    p.append(rotate_270(h))

    v = flip_horizontal(s)
    p.append(v)
    p.append(rotate_90(v))
    p.append(rotate_180(v))
    p.append(rotate_270(v))

    hv = flip_vertical(flip_horizontal(s))
    p.append(hv)
    p.append(rotate_90(hv))
    p.append(rotate_180(hv))
    p.append(rotate_270(hv))

    return list(set(p))


def rotate_90(p):
    # 6,3,0
    # 7,4,1
    # 8,5,2
    return "".join([p[6], p[3], p[0], p[7], p[4], p[1], p[8], p[5], p[2]])


def rotate_180(p):
    # 8,7,6
    # 5,4,3
    # 2,1,0
    return "".join([p[8], p[7], p[6], p[5], p[4], p[3], p[2], p[1], p[0]])


def rotate_270(p):
    # 2,5,8
    # 1,4,7
    # 0,3,6
    return "".join([p[2], p[5], p[8], p[1], p[4], p[7], p[0], p[3], p[6]])


def flip_vertical(p):
    # 2,1,0
    # 5,4,3
    # 8,7,6
    return "".join([p[2], p[1], p[0], p[5], p[4], p[3], p[8], p[7], p[6]])


def flip_horizontal(p):
    # 6,7,8
    # 3,4,5
    # 0,1,2
    return "".join([p[6], p[7], p[8], p[3], p[4], p[5], p[0], p[1], p[2]])



def learn_game():
    global newRow
    
    tree = {}
    
    for i in range(1000):
        newRow= []
        result = start_game()

        print(newRow, result)
        

        build_tree(tree, 0, newRow, result)
        with open('tictac.csv', 'a', newline='') as f:
            thewriter = csv.writer(f)
            thewriter.writerow(newRow)

    with open('tree.json', 'w', newline='') as f:
        f.write(json.dumps(tree, indent=4))


def build_tree(tree, depth, row, result):
    if(len(row)-1 == depth):
        tree[row[depth]] = result
        return
    if not row[depth] in tree:
        tree[row[depth]] = {}
    build_tree(tree[row[depth]], depth+1, row, result)
    return tree 

learn_game()

# newRow.append(player_sign)
#             with open('tictac.csv', 'w', newline='') as f:
#                 thewriter = csv.writer(f)
#                 thewriter.writerow(newRow)
                # thewriter.writerow(newRow)

# import csv
# newRow = ['']
# with open('tictac.csv', 'w', newline='') as f:
#     thewriter = csv.writer(f)
#     thewriter.writerow(newRow)



# tree = {}
# tree[1] = {}
# if 1 in tree[4] 
# type(x) is int 




# if (did_win) or:
#     return result.append()
# return 





