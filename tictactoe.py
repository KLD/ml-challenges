import numpy as np
import random


def start_game() -> int:
    board = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    player = -1

    while not did_win(board, player):
        print_board(board)
        player *= -1
        next = play_turn(board * player, player)

        print('player {} picked {}'.format(board_fills[player], next))
        board[next] = player

    print_board(board)
    print("\n")
    if did_win(board, 1):
        print("X won")
        return 1
    elif did_win(board, -1):
        print("O won")
        return -1
    else:
        print("Tie")
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
    for i in range(9):
        print(board_fills[board[i]], end='|' if i % 3 != 2 else "\n")

    print("\n")
    print("-"*10)


def play_turn(board, player) -> int:
    i = random.randint(0, 8)

    while board[i] != 0:
        i = random.randint(0, 8)

    return i


start_game()
