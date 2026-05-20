size = 5

def make_board(size):
    board = []
    for y in range(size):
        row = []
        for x in range(size):
            row.append(0)
        board.append(row)
    return board        

def print_board(board):
    for row in board:
        for field in row:
            if field == 1:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()
    print()

def place_queen(board, x, y):
    board[y][x] = 1

def remove_queen(board, x, y):
    board[y][x] = 0

def has_queen(board, x, y):
    return board[y][x] == 1

def check_board(board):
    positions = []
    for row in board:
        if 1 not in row: 
            return False
        if sum(row) > 1:
            return False
        positions.append(row.index(1))
    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            if i == j:
                return False
            if abs(positions[i] - positions[j]) == abs(i - j):
                return False
    return True

board = make_board(size)

place_queen(board,0,0)
place_queen(board,1,1)
place_queen(board,1,2)

def guess(board, x):
    for y in range(size):
        place_queen(board, x, y)
        
        if x == size - 1:
            if check_board(board):
                print_board(board)
        else:
            guess(board, x + 1)
        
        remove_queen(board, x, y)

guess(board, 0)