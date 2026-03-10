# Kryds og bolle

## Resultatet

Sidste gang lavede vi et Kryds og bolle spil. Til de der ikke kom helt i mål, eller som ikke fik gemt koden, findes der en løsning fra sidste uge [Her](../Uge%204%20-%20Kryds%20og%20bolle/KrydsOgBolle%201.py).

I dag skal vi tilføje en AI som man kan spille mod.

Der kommer til at være noget kode der kan kopieres, men for at få det til at virke godt, vil i få brug for at lave noget kode selv.

## Kode del 1: Omdøb spiller 2 til "AI":
Start med koden fra sidste gang. Hvis det skal være nemt, kan i hente koden [Her](../Uge%204%20-%20Kryds%20og%20bolle/KrydsOgBolle%201.py).

I koden fra sidste uge, har vi en variabel der hedder `human2`:

```python
human2 = "O"
```

Vi vil nu gerne lave koden om til at spilleren med `O` brikkerne er en AI.

Omdøb variablen `human2` til `ai`, så linjen bliver til:
```python
ai = "O"
```

Ændringen vil medføre fejl i jeres spil så det ikke virker. Prøv selv at finde og rette fejlene :-).

## Kode del 2: tilføj en AI funktion:


Selv om spilleren er omdøbt til AI, fungerer det stadig som en menneskelig spiller. Lad os tilføje en AI-funktion.

Funktionen skal kopieres ind i koden. En god ide er over `print_board` funktionen:

```python
def find_best_move(board, ai, human):
    # 1: Kan AI vinde denne tur?
    for i in range(9):
        if board[i] == " ":
            board[i] = ai
            if check_winner(board, ai):
                board[i] = " "
                return i
            board[i] = " "

    # 2: Kan mennesket vinde næste tur?
    for i in range(9):
        if board[i] == " ":
            board[i] = human
            if check_winner(board, human):
                board[i] = " "
                return i
            board[i] = " "

    # 3: Vælg en tilfældig placering
    return random.choice([i for i, v in enumerate(board) if v == " "])
```

## Kode del 3: Kald AI funktionen

Selv om der er tilføjet en AI funktion, bliver den ikke brugt endnu. Det skal vi selv bede spillet om.

I spillet har vi dette kode der spørger efter en handling:
```python
    print(f"Spiller {current_player}, Det er din tur.")
    move = get_move(board)
```

Her skal vi nu rette koden til at lade computeren selv tage sine ture. Det kan gøres mde denne kode:

```python
    if current_player == human1:
        move = get_move(board)
    else:
        move = find_best_move(board, ai, human1)
```

Nu kan vi spille de første træk mod computeren. 

Prøv at spille spillet. Pludselig holder AI'en op med at tage ture.

## Kode del 4: Kald AI funktionen når vi flytter brikker

Når vi har sat vores tre brikker, holder AI op med at virke. Det er fordi det er noget andet kode til at flytte brikkerne.

Find denne kode i dit projekt:
```python
    print(f"Spiller {current_player}, Det er din tur.")
    print(f"Hvilken brik skal fjernes?")
    flyt = get_from(board, current_player)
    print(f"Hvor skal brikken sættes?")
    move = get_move(board)
```

Og udskift den med:
```python
    print(f"Spiller {current_player}, Det er din tur.")
    if current_player == human1:
        print(f"Hvilken brik skal fjernes?")
        flyt = get_from(board, current_player)
        print(f"Hvor skal brikken sættes?")
        move = get_move(board)
    else:
        move = find_best_move(board, ai, human1)
        flyt = None
```

Nu kan computeren spille videre - men der er noget galt.

Kan du se hvad der er galt med spillet?

## Kode del 5: AI flytter brikker

For at AI ikke bliver ved med at sætte brikker skal vi finde denne kode i vores projekt:

```python
        move = find_best_move(board, ai, human1)
        flyt = None
```

Og rette den til: 
```python
        (move,flyt) = find_best_move_flyt(board, ai, human1)
```

Og så skal vi have lavet en ny funktion til at beregne et flyt af en brik. Sæt denne funktion ind i koden. En god ide er over `print_board` funktionen:

```python
def find_best_move_flyt(board, ai, human):
    til = find_best_move(board, ai, human)
    ai_fields = [i for i, v in enumerate(board) if v == ai]
    fra = random.choice(ai_fields)
    return (til,fra)
```

Nu kan AI finde ud af at flytte en brik. Kan du vinde over den?

## Ekstra opgave 1 (mellem): AI mod AI
Kan du få computeren til at spille mod sig selv?

## Ekstra opgave 2 (svær): Gør AI bedre
Lige nu kan man godt vinde over AI. Når den flytter en brik, flytter den en tilfældig brik. Er man tålmodig og venter på den laver en fejl, kan man let vinde.

Kan du rette AI-koden til, så AI ikke taber så let?

> [!TIP]
> Koden her nedenunder giver et oplæg til hvordan man kan strukturere koden.

```python
def find_best_move_flyt(board, ai, human):
    til = find_best_move(board, ai, human)
    ai_fields = [i for i, v in enumerate(board) if v == ai]

    # 1: Kan AI vinde denne tur?
    .... kode ....
    
    # 2: Kan AI tabe ved at flytte den forkerte brik?
    .... kode ....

    fra = random.choice(ai_fields)
    return (til,fra)
```

Med mindre man er MEGET god, vil AI stadig kunne snydes så man kan vinde over den. Men den begynder at blive god.

Næste gang kan vi se på at gøre AI uovervindelig.