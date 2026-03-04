import random

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
human2 = "O"

current_player = human1

for turn in range(6):
    print_board(board)

    print(f"Spiller {current_player}, Det er din tur.")
    move = get_move(board)
    
    board[move] = current_player

    if check_winner(board, current_player):
        print_board(board)
        print(f"🎉 Spiller {current_player} vinder! Tillykke!")
        exit()

    current_player = human2 if current_player == human1 else human1

while True:
    print_board(board)

    print(f"Spiller {current_player}, Det er din tur.")
    print(f"Hvilken brik skal fjernes?")
    flyt = get_from(board, current_player)
    print(f"Hvor skal brikken sættes?")
    move = get_move(board)
    
    board[flyt] = " "
    board[move] = current_player

    if check_winner(board, current_player):
        print_board(board)
        print(f"🎉 Spiller {current_player} vinder! Tillykke!")
        exit()

    current_player = human2 if current_player == human1 else human1

print_board(board)
print("Det blev uafgjort!")