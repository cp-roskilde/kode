# Kryds og bolle med god ai

## Resultatet

Sidste gang lavede vi et Kryds og bolle spil med en AI. Til de der ikke kom helt i mål, eller som ikke fik gemt koden, findes der en løsning fra sidste uge [Her](../Uge%205%20-%20Kryds%20og%20bolle%20AI/KrydsOgBolle%201_ai.py).

I dag skal vi forbedre vores AI, så den ikke kan tabe.

Der kommer til at være noget kode der kan kopieres, men i får selv brug for at finde ud af hvordan det skal sættes ind.

## Kode del 1: Brug kun __1__ AI metode.

Lige nu er der to AI metoder:

 * Der er `find_best_move` som vælger et sted at sætte en brik.
 * Der er `find_best_move_flyt` som vælger at flytte en brik fra et sted til et andet.

Det er næsten det samme de to metoder gør, så vi vil gerne kunne gøre det hele med den samme metode.

Vi vælger metoden `find_best_move_flyt`, da det er denne der kan mest. Den returnerer to tal, som er feltet der skal flyttes til og feltet der skal flyttes fra. Hvis der ikke skal fjernes en brik, kan vi bruge den særlige værdi `None`.

I metoden `find_best_move_flyt` under linjen der ser hvor AI har brikker stående:
```python
    ai_fields = [i for i, v in enumerate(board) if v == ai]
```

Tilføjes den ekstra kode:
```python
    if len(ai_fields)<3: return (til,None)
```

Denne kode siger at hvis AI ikke har tre brikker i spil, skal den bare sætte en brik uden at fjerne noget.

Der hvor vi tidligere kaldte metoden `find_best_move`, kan vi nu bruge find_best_move_flyt i stedet:

Udskift koden:

```python
    if current_player == human1:
        move = get_move(board)
        # move = find_best_move(board, ai, human1)
    else:
        move = find_best_move(board, ai, human1)
```

med:

```python
    if current_player == human1:                                  
        move = get_move(board)                                    
        # (move,flyt) = find_best_move_flyt(board, human1, ai)    
    else:                                                         
        (move,flyt) = find_best_move_flyt(board, ai, human1)      
```

Spillet burde stadig virke på samme måde som før. Gør det?

## Kode del 2: Lad AI kende alle sine muligheder.

I metoden `find_best_move`, vælger vi en plads ud fra tre muligheder. To af mulighederne giver kun et felt der kan vælges. Den sidste mulighed vælger et tilfældigt tomt felt.

Vi vil gerne have at `find_best_move` bare giver mulighederne men ikke selv vælger et felt.

I metoden `find_best_move` skiftes denne kode:

```python
return i
```

med:

```python
return [i]
```

> [!WARNING]
> Der skal være det samme antal mellemrum foran. Måske det er bedre at redigere koden selv, end at bruge copy-paste.

Samtidig skal koden ikke selv vælge et tilfældigt frit felt, men bare give alle frie felter. Det gør vi ved at fjerne `random.choice` delen.  
Udskift
```python
    return random.choice([i for i, v in enumerate(board) if v == " "])
```
Med
```python
    return [i for i, v in enumerate(board) if v == " "]
```

Nu får vi en liste af muligheder tilbage. Men man må stadig kun sætte en brik et sted. Spillet vil lige nu ikke virke, hvis vi prøver det.

## Kode del 3: Få bedste flyt fra en ai funktion

Vores metode `find_best_move_flyt` er endnu ikke blevet bedre. AI koden gør stadig de samme valg.

Vi får brug for at lægge den klogere AI i en ny metode. Tilføj denne metode til koden:
```python
def ai_check(board,ai,human,skridt):
    til = find_best_moves(board, ai, human)
    ai_fields = [i for i, v in enumerate(board) if v == ai]

    muligheder = []
    if len(ai_fields)==3:
        muligheder = [(t,f) for t in til for f in ai_fields]
    else:
        muligheder = [(t,None) for t in til]

    if skridt==0: return (False, muligheder)

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
```

Denne kode er i stand til at se flere skridt frem i spillet og se om den kan vinde eller om den vil tabe. Hvis der er et træk der sikrer den vinder, vælges det, hvis der er et træk der er sikkert på at tabe vælges det, og ellers vælges et tilfældigt muligt træk.

For at benytte AI metoden her ovenfor, rettes `find_best_move_flyt` til at indeholde følgende, og den gamle metode slettes:

```python
def find_best_move_flyt(board, ai, human):
    (win,muligheder) = ai_check(board, ai, human, 3)
    return random.choice(muligheder)    
```

Her henter vi AI mulighederne og vælger en af de foreslåede muligheder som vores handling.

Prøv at spille mod AI et par gange. Er AI blevet bedre?

## Kode del 4: Gør AI uovervindelig

Lige nu er det stadig muligt at vinde over vores AI. Det skyldes denne linje:

```python
(win,muligheder) = ai_check(board, ai, human, 3)
```

Linjen siger at AI skal se 3 træk frem. Det virker fint når spillet er i gang. Men når et spil starter, kan den ikke se langt nok frem, hvis man lægger en fælde for den.

Prøv at gøre tallet `3` højere og se om AI bliver bedre.

Hvad sker der hvis man bruger tallet `10` i stedet for?

Hvad er et godt tal for at gøre AI bedst?