# Kryds og bolle

## Resultatet

Vi skal i dag lave et simpelt kryds og bolle spil.

Når vi starter programmet vil det bede brugeren om at vælge et felt at sætte en kryds-brik i. Herefter får man lov at sætte en O-brik. Spillet slutter når en spiller har fået tre på stribe eller der ikkke er flere frie pladser.

Her nedenfor er et eksempel på afviklingen af spillet:

```
>> 
>> 
>>    |   |          1 | 2 | 3 
>> ---+---+---      ---+---+---
>>    |   |          4 | 5 | 6 
>> ---+---+---      ---+---+---
>>    |   |          7 | 8 | 9 
>> 
>> 
>> Spiller X, Det er din tur.
Vælg en placering (1–9): 1
>> 
>> 
>>  X |   |          1 | 2 | 3 
>> ---+---+---      ---+---+---
>>    |   |          4 | 5 | 6 
>> ---+---+---      ---+---+---
>>    |   |          7 | 8 | 9 
>> 
>> 
>> Spiller O, Det er din tur.
Vælg en placering (1–9): 5
>> 
>> 
>>  X |   |          1 | 2 | 3 
>> ---+---+---      ---+---+---
>>    | O |          4 | 5 | 6 
>> ---+---+---      ---+---+---
>>    |   |          7 | 8 | 9 
>> 
>> 
>> Spiller X, Det er din tur.
Vælg en placering (1–9): 9
>> 
>> 
>>  X |   |          1 | 2 | 3 
>> ---+---+---      ---+---+---
>>    | O |          4 | 5 | 6 
>> ---+---+---      ---+---+---
>>    |   | X        7 | 8 | 9 
>> 
>> 
>> Spiller O, Det er din tur.
Vælg en placering (1–9): 3
>> 
>> 
>>  X |   | O        1 | 2 | 3 
>> ---+---+---      ---+---+---
>>    | O |          4 | 5 | 6 
>> ---+---+---      ---+---+---
>>    |   | X        7 | 8 | 9 
>> 
>> 
>> Spiller X, Det er din tur.
Vælg en placering (1–9): 7
>> 
>> 
>>  X |   | O        1 | 2 | 3 
>> ---+---+---      ---+---+---
>>    | O |          4 | 5 | 6 
>> ---+---+---      ---+---+---
>>  X |   | X        7 | 8 | 9 
>> 
>> 
>> Spiller O, Det er din tur.
Vælg en placering (1–9): 4
>> 
>> 
>>  X |   | O        1 | 2 | 3 
>> ---+---+---      ---+---+---
>>  O | O |          4 | 5 | 6 
>> ---+---+---      ---+---+---
>>  X |   | X        7 | 8 | 9 
>> 
>> 
>> Spiller X, Det er din tur.
Vælg en placering (1–9): 8
>> 
>>  X |   | O        1 | 2 | 3 
>> ---+---+---      ---+---+---
>>  O | O |          4 | 5 | 6 
>> ---+---+---      ---+---+---
>>  X | X | X        7 | 8 | 9 
>> 
>> Spiller X vinder! Tillykke!
```

## Noget nyt - Funktioner
Vi skal i dag arbejde med funktioner i python. En funktion er et stykke kode som man kan køre fra forskellige dele af sin kode.

Fordelen ved en funktion er, at den kun handler om en lille del af hele programmet og derfor er lettere at overskue.

En funktion skrives som vist her:
```python
def plus(a,b):
  return a+b
```

Her har vi `def`ineret funktionen `plus`. Funktionen tager to parametre som vi kalder `a` og `b`.

Metoden kan kaldes med følgende kode:

```python
print(plus( 5 , 3 ))
```

Her bliver `a` sat til `5` og `b` til `3`. Funktionen bliver nu til `return 5+3`, hvorfor programmet skriver `8` til skærmen.

En funktion kan godt have flere linjer og kalde andre funktioner.

## Kode del 1: Udskriv spillepladen
Vi starter med en funktion der kan udskrive spillepladen:

```python
def print_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]}        1 | 2 | 3 ")
    print("---+---+---      ---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}        4 | 5 | 6 ")
    print("---+---+---      ---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}        7 | 8 | 9 ")
    print("\n")
```

Her forventer vi at spillepladen `board` er en liste af ni felter. Hver felt udskrives sammen med nogle faste tegn, så vi kan se hvor felterne er. Ved siden af spillepladen tegner vi en spilleplade med tallene 1 til 9. Dette er felternes navne, når spilleren senere skal sætte en brik. 

Vi kan teste spilleplade-funktionen med denne kode:

```python
board = [" ", " ", " ", " ", " ", " ", " ", " ", " "] # en tom plade
print_board(board) # send spillepladen til tegne-funktionen
```

Dette burde tegne en tom spilleplade.

```python
board = [" ", "X", " ", " ", "X", " ", " ", "X", "O"] # en aktiv plade
print_board(board) # send spillepladen til tegne-funktionen
```

Her tegner vi en spilleplade med nogle brikker på. Måske har `X` snydt lidt?

## Kode del 2: Spørg spilleren hvor vi skal sætte en brik
Spilleren skal have mulighed for at sætte en brik. Vi har 9 felter, så vi vil gerne have et tal mellem 1 og 9.

Hvis spilleren skriver noget der ikke giver mening skal vi spørge igen.

```python
def get_move(board):
    while True: # Bliv ved med at spørge
        try: # Vi prøver at køre noget kode der kan fejle 
            move = int(input("Vælg en placering (1–9): "))
            if move < 1 or move > 9:
                print("Ugyldig placering. Prøv igen.")
            elif board[move] != " ":
                print("Den plads er allerede taget.")
            else:
                return move
        except ValueError: # Hvis koden fejlede, så har brugeren ikke skrevet et tal
            print("Indtast venligst et gyldigt felt.")
```

Denne funktion vil bede brugeren om at angive et felt.

Vi kan teste funktionen med denne kode:

```python
board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
human = "X"
print_board(board)
move = get_move(board)
board[move] = current_player
print_board(board)
```

Hvis vi kører koden får vi nu lov til at sætte en `X` brik et sted på spillepladen.

> [!WARNING]
> Spillet sætter brikken på et forkert felt. Hvis man sætter en brik på felt 1, skulle den være øverst til venstre.  
> I skal selv finde ud af hvordan i får den til at placere brikken rigtigt.

> [!TIP]  
> Se på kode-linjen herunder. Den kan vise hvad der er galt:


```python
    print(f" {board[0]} | {board[1]} | {board[2]}        1 | 2 | 3 ")
```

Nu skal brugeren kunne komme med sit gæt:

## Kode del 3: Er der en der har vundet?
Vi får brug for at se om nogen har vundet, hver gang en brik bliver sat.

Vi laver endnu en funktion til dette:

```python
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
```

Vi laver en liste `winning_positions` der beskriver de måder man kan få tre på stribe.

> [!TIP]
> Bemærk at vi bruger tallene 0-8 og ikke 1-9. Det er fordi computere starter med at tælle fra 0 og ikke fra 1 ligesom mennesker.

For hver samling af felter, ser vi om alle tre felter har samme brik på.

Vi kan teste funktionen med disse stykker kode:

Vi har en tom spilleplade - ingen vinder:
```python
board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
print_board(board)
if (check_winner(board, 'X')): print("X har vundet!")
elif (check_winner(board, 'O')): print("O har vundet!")
else: print("ingen har vundet :-(")
```

Kryds har vundet på skrå:
```python
board = ["X", " ", " ", " ", "X", " ", " ", " ", "X"]
print_board(board)
if (check_winner(board, 'X')): print("X har vundet!")
elif (check_winner(board, 'O')): print("O har vundet!")
else: print("ingen har vundet :-(")
```

Bolle har vundet lodret:
```python
board = ["O", " ", " ", "O", " ", " ", "O", " ", " "]
print_board(board)
if (check_winner(board, 'X')): print("X har vundet!")
elif (check_winner(board, 'O')): print("O har vundet!")
else: print("ingen har vundet :-(")
```

## Kode del 4: Sæt det hele samme

Til sidst sætter vi vores funktioner sammen med selve spillet.

> [!WARNING]
> Før vi tilføjer koden er det en god ide at rydde op i det vi allerede har lavet. Vi skla kun gemme funktionerne. Alt det kode vi har brugt til at teste funktionerne kan slettes igen.

```python

board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
human1 = "X"
human2 = "O"

current_player = human1

for turn in range(9):
    print_board(board)

    print(f"Spiller {current_player}, Det er din tur.")
    move = get_move(board)
    
    board[move] = current_player

    if check_winner(board, current_player):
        print(f"🎉 Spiller {current_player} vinder! Tillykke!")
        exit()

    current_player = human2 if current_player == human1 else human1

print_board(board)
print("Det blev uafgjort!")

```

Test om jeres spil virker.

## Ekstraopgave 1 (middel): Kan man lave rammer omkring spillet?

Lige nu ser spillet sådan ud:

```
>>  X |   |          1 | 2 | 3 
>> ---+---+---      ---+---+---
>>    | O |          4 | 5 | 6 
>> ---+---+---      ---+---+---
>>    |   | X        7 | 8 | 9 
```

Kan du få det til at se sådan her ud:

```
>> +---+---+---+      +---+---+---+
>> | X |   |   |      | 1 | 2 | 3 |
>> +---+---+---+      +---+---+---+
>> |   | O |   |      | 4 | 5 | 6 |
>> +---+---+---+      +---+---+---+
>> |   |   | X |      | 7 | 8 | 9 |
>> +---+---+---+      +---+---+---+
```

## Ekstraopgave 2 (svær): Kan man flytte brikker
Lige nu kan man kun sætte brikker. Spillepladen bliver hurtigt fyldt.

Kan spillet rettes til så hver spiller kun kan sætte tre brikker, og herefter flytte brikker fra et felt til et andet?
