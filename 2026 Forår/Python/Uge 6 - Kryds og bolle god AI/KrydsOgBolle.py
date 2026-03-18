from datetime import datetime
import random

def find_best_moves(board, ai, human):
    # 1: Kan AI vinde denne tur?
    for i in range(9):
        if board[i] == " ":
            board[i] = ai
            if check_winner(board, ai):
                board[i] = " "
                return [i]
            board[i] = " "

    # 2: Kan mennesket vinde næste tur?
    for i in range(9):
        if board[i] == " ":
            board[i] = human
            if check_winner(board, human):
                board[i] = " "
                return [i]
            board[i] = " "

    # 3: Vælg en tilfældig placering
    return [i for i, v in enumerate(board) if v == " "]

def ai_check(board,ai,human,skridt):
    til = find_best_moves(board, ai, human)
    ai_fields = [i for i, v in enumerate(board) if v == ai]

    muligheder = []
    if len(ai_fields)==3:
        muligheder = [(t,f) for t in til for f in ai_fields]
    else:
        muligheder = [(t,None) for t in til]

    if skridt==0: return (True, muligheder)

    gode_muligheder = []

    for mulighed in muligheder:
        b2 = list(board)
        b2[mulighed[0]] = ai
        if mulighed[1] is not None: b2[mulighed[1]] = " "
        if check_winner(b2, ai): return (True,[mulighed])

        (omvendt_win,omvendt) = ai_check(b2, human, ai, skridt-1)
        if not omvendt_win: gode_muligheder.append(mulighed)

    if len(gode_muligheder)>0: return (True, gode_muligheder)
    return (False, muligheder)

def find_best_move_flyt(board, ai, human):
    (win,muligheder) = ai_check(board, ai, human, 6)
    return random.choice(muligheder)    

def print_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]}        1 | 2 | 3 ")
    print("---+---+---      ---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}        4 | 5 | 6 ")
    print("---+---+---      ---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}        7 | 8 | 9 ")
    print("\n")

def check_winner(board, player):
    winning_positions = [
        (0,1,2), (3,4,5), (6,7,8),    # Rækker
        (0,3,6), (1,4,7), (2,5,8),    # Kolonner
        (0,4,8), (2,4,6)              # Diagonaler
    ]

    for win in winning_positions:
        if board[win[0]] == player and board[win[1]] == player and board[win[2]] == player:
            return True

    return False

def get_move(board):
    while True:
        try:
            move = int(input("Vælg en placering (1–9): ")) - 1
            if move < 0 or move > 8:
                print("Ugyldig placering. Prøv igen.")
            elif board[move] != " ":
                print("Den plads er allerede taget.")
            else:
                return move
        except ValueError:
            print("Indtast venligst et gyldigt felt.")

def get_from(board, current_player):
    while True:
        try:
            move = int(input("Vælg en placering (1–9): ")) - 1
            if move < 0 or move > 8:
                print("Ugyldig placering. Prøv igen.")
            elif board[move] == " ":
                print("Der er ikke nogen brik her.")
            elif board[move] != current_player:
                print("Der er ikke din brik!")
            else:
                return move
        except ValueError:
            print("Indtast venligst et gyldigt felt.")

board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
human1 = "X"
ai = "O"

current_player = human1

start = datetime.now()
moves_taken = 0

for turn in range(6):
    print_board(board)

    print(f"Spiller {current_player}, Det er din tur.")
    
    if current_player == human1:
        # move = get_move(board)
        (move,flyt) = find_best_move_flyt(board, human1, ai)
    else:
        (move,flyt) = find_best_move_flyt(board, ai, human1)
    
    board[move] = current_player
    moves_taken += 1

    if check_winner(board, current_player):
        print_board(board)
        print(f"🎉 Spiller {current_player} vinder! Tillykke!")
        exit()

    current_player = ai if current_player == human1 else human1

while True:
    print_board(board)

    print(f"Spiller {current_player}, Det er din tur.")
    if current_player == human1:    
        # print(f"Hvilken brik skal fjernes?")
        # flyt = get_from(board, current_player)
        # print(f"Hvor skal brikken sættes?")
        # move = get_move(board)
        (move,flyt) = find_best_move_flyt(board, human1, ai)
    else:
        (move,flyt) = find_best_move_flyt(board, ai, human1)
    
    if (flyt is not None): board[flyt] = " "
    board[move] = current_player
    moves_taken += 1

    if check_winner(board, current_player):
        print_board(board)
        print(f"🎉 Spiller {current_player} vinder! Tillykke!")
        exit()

    current_player = ai if current_player == human1 else human1

    nu = datetime.now()
    elapsed_time = (nu - start).total_seconds()
    print(f"Tid brugt: {elapsed_time:.2f} sekunder, Træk taget: {moves_taken}, Træk per sekund: {moves_taken/elapsed_time:.2f}")

print_board(board)
print("Det blev uafgjort!")
