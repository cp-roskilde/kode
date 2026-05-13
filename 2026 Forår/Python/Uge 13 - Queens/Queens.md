# Queens

## Resultatet

I dag skal vi ikke bruge Micro:Bit, men blot skrive noget python kode. Hvis man er kreativ kan man også godt få koden til at virke til at vise resultatet på en Micro:Bit.

I skak er den brik der kan mest dronningen. En dronning i skak kan rykke til siderne, frem og tilbage eller på skrå. I et normalt skakspil er der 8 x 8 felter. Det er muligt på disse felter at sætte 8 dronninger, så ingen af dem kan slå hinanden.

Vi skal lave et program der kan finde løsninger på at placere dronnignerne på brættet.

# Et lille skak-spil

Hvis nu vi forestiller os et mindre skakspil med kun 4 x 4 felter, så er det lidt nemmere.

```python
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
```

Her er lidt hjælpe-kode til at lave et skakspil og sætte/fjerne dronnigner.

Kan i finde på noget kode der kan regne en løsning ud hvor der her kan sættes 4 dronninger uden at nogen bliver slået hjem?

## Større spil

Kan i også løse det med 5 (det kan vises på en Micro:Bit) eller 8?