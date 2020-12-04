from math import inf

cpu = "o"
human = "x"

def any_moves_left(board):
    """Returns True if there are moves remaining on the board, else returns False. """
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                return True
    return False

def evaluate(board):
    """Checks the board to see if either X or O have won. Returns 10 if the player has won, -10 if the opponent has won or 0 is neither have won."""
    # check columns and rows
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            if board[i][0] == cpu:
                return 10
            elif board[i][0] == human:
                return -10
        if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            if board[0][i] == cpu:
                return 10
            elif board[0][i] == human:
                return -10

    # check diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == cpu:
            return 10
        elif board[0][0] == human:
            return -10
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == cpu:
            return 10
        elif board[0][2] == human:
            return -10

    # if neither have won return 0
    return 0
    
def minimax(board, depth, is_max):
    """Goes through all possible moves on the board and returns their values."""
    score = evaluate(board)

    if score == 10:
        return score + depth
    if score == -10:
        return score - depth
    if not any_moves_left(board):
        return 0

    if is_max:
        best = -inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == None:
                    board[i][j] = cpu
                    best = max(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = None
        return best

    else:
        best = inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == None:
                    board[i][j] = human
                    best = min(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = None
        return best

def find_best_move(board):
    best_value = -inf
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                board[i][j] = cpu
                move_value = minimax(board, 0, False)
                board[i][j] = None

                if move_value > best_value:
                    best_move = (j, i)
                    best_value = move_value

    return best_move

if __name__ == "__main__":

    board = [
    ["o", None, "x"],
    ["o", None, "x"],
    ["x", None, None]
    ]

    move = find_best_move(board)
    print(f"The best move is {move}")