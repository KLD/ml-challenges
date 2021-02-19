board = [0, 0, 0, 0, 0, 0, 0, 0, 0]


def start_game():
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    turn = 0
    player = 1


0, 1, 2
3, 4, 5
6, 7, 8


def did_win(board, player_sign):
    for i in range(3):
        if(board[i*3] == board[(i*3)+1] == board[(i*3)+2] == player_sign):
            return True

        if(board[(i*3)+i] == board[((i+1)*3)+1] == board[((i+2)*3)+2] == player_sign):
            return True

    if(board[0] == board[4] == board[8] == player_sign):
        return True

    if(board[2] == board[4] == board[6] == player_sign):
        return True

    return False
