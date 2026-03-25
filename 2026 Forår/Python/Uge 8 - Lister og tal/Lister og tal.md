# Lister og tal

## Resultatet

I dag gør vi det lige som sidste gang. Vi skal se på nogle kodestumper og forså hvad de gør. Ud fra det vi lærer med disse stumper skal vi selv skrive programmer der kan lave nogle beregninger. Vi får ikke svaret leveret, men skal selv finde ud af det.

Vi skal lave følgende øvelser:
 * Finde det største tal
 * Finde det mindste tal
 * Finde gennemsnittet af en række tal
 * Sortere en liste af tal

## Eksempel 1 - Hvad er en liste

I python findes der en datatype der hedder en liste. En liste kan indeholde flere forskellige værdier.

Hvis vi vil oprette en liste med tallene `2`, `3`, `5` og `7`, kan det gøres med koden:
```python
liste = [2, 3, 5, 7]
print(liste)
```

Vi kan tilføje flere værdier til en liste ved at bruge funktionen `append`, som det kan ses her:
```python
liste = [2, 3, 5, 7]
liste.append(11)
print(liste)
liste.append(13)
print(liste)
``` 

Man kan også fjerne en værdi fra listen ved at bruge funktionen `remove`, som det kan ses her:
```python
liste = [2, 3, 5, 7, 5, 3, 2]
print(liste)
liste.remove(3)
print(liste)
``` 
> [!TIP]
> Bemærk at remove kun fjerner den første værdi der matcher. Der bliver kun fjernet et `3`-tal.

Man kan få længden af en liste ved at benytte `len` funktionen:
```python
liste = [2, 3, 5, 7, 11, 13, 17]
print("Antal elementer i listen:")
print(len(liste))
``` 

Man kan få fat i et bestemt element i listen med `[]`. Her finder vi element nummer `0` (Det første) og `4` (Det 5. tal i listen).
```python
liste = [2, 3, 5, 7, 11, 13, 17]

print("Det første element (index=0) i listen er:")
print(liste[0])

print("Det femte element (index=4) i listen er:")
print(liste[4])
``` 

Der er to måder at gennemgå en liste og udskrive værdierne:
```python
liste = [2, 3, 5, 7, 5, 3, 2]

# Tæl igennem listen med index og udskriv værdien.
for index in liste:
    print(f"Index: {index}, Value: {liste[index]}")

# Tæl igennem listen og udskriv værdien uden at kende index.
for value in liste:
    print(f"Value: {value}")
```

Der er også andre muligheder med lister, men nu kan i det vigtigeste. Spørg, hvis i har brug for at kunne noget mere med lister.

## Opgave 1 - Find det mindste tal
Start et nyt projekt, hvor der ikke er noget kode, og kopier det nedenstående ind:

```python
import random

def random_list(n):
    return [random.randint(1, 100) for _ in range(n)]

def minimum(liste):
    return liste[0]

liste = random_list(10)
print("Liste:", liste)
liste_min = minimum(liste)
print("Minimum:", liste_min)
liste_korrekt_min = min(liste)
print("Korrekt minimum:", liste_korrekt_min)
print("Er det korrekt?", liste_min == liste_korrekt_min)
```

I koden er der funktionen `minimum`. Den beregner ikke minimum rigtigt lige nu, men returnerer blot det første tal i listen.

Kan du rette koden til, så den returnerer det rigtige tal, __uden__ at bruge funktionen `min`?

## Opgave 2 - Find det største tal
Her skal du arbejde videre med koden fra opgave 1. 

Kan du rette koden til så den finder det største tal i stedet for det mindste?

> [!TIP]  
> Ud over at rette din egen kode til, skal funktionen `min` også rettes til `max`.  
> Måske du også bør rettet noget af teksten der udskrives til skærmen?

## Opgave 3 - Find gennemsnittet
Ligesom under opgave 1, skal vi starte med noget ny kode. Denne kode har allerede delene til at beregne gennemsnit, men lige nu gætter den altid på `50`.

Kan du rette koden i funktionen `gennemsnit` til, så den regner gennemsnittet rigtigt uden at benytte `statistics.mean` funktionen?

Her er koden til programmet:
```python
import random
import statistics

def random_list(n):
    return [random.randint(1, 100) for _ in range(n)]

def gennemsnit(liste):
    return 50

liste = random_list(10)
print("Liste:", liste)
liste_sorteret = gennemsnit(liste)
print("Gennemsnit:", liste_sorteret)
liste_korrekt_gennemsnit = statistics.mean(liste)
print("Korrekt Gennemsnit:", liste_korrekt_gennemsnit)
print("Er det korrekt?", liste_sorteret == liste_korrekt_gennemsnit)
```

## Opgave 4 - Sorter en liste.
Ligesom under opgave 1, skal vi starte med noget ny kode. Denne kode har allerede delene til at sortere en liste, men lige nu sorterer den ikke rigtigt.

Kan du rette koden i funktionen `sorter` til, så den sorterer rigtigt, uden at benytte funktionen `sorted` eller `sort`?

Her er koden til programmet:

```python
import random
import statistics

def random_list(n):
    return [random.randint(1, 100) for _ in range(n)]

def sorter(liste):
    return liste

liste = random_list(10)
print("Liste:", liste)
liste_sorteret = sorter(liste)
print("Sorteret Liste:  ", liste_sorteret)
liste_korrekt_sorteret = sorted(liste)
print("Korrekt Sorteret:", liste_korrekt_sorteret)
print("Er det korrekt?", liste_sorteret == liste_korrekt_sorteret)
```

> [!TIP]  
> Der findes mange måder en computer kan sortere på. Nogle er hurtigere, nogle sparer på hukommelse og nogle er fjollede.  

Her er nogle links til algoritmer der kan sortere en liste:
 * [Merge sort](https://sortvisualizer.com/mergesort/)
 * [Quick sort](https://sortvisualizer.com/quicksort/)
 * [Heap sort](https://sortvisualizer.com/heapsort/)
 * [Selection sort](https://sortvisualizer.com/selectionsort/)
 * [Bubble sort](https://sortvisualizer.com/bubblesort/)
 * [Insertion sort](https://sortvisualizer.com/insertionsort/)
 * [Cycle sort](https://www.geeksforgeeks.org/dsa/cycle-sort)
 * [3 Way Merge sort](https://www.geeksforgeeks.org/dsa/3-way-merge-sort)

 Og nogle lidt fjollede sorteringer:
  * [Bogo sort](https://sortvisualizer.com/bogosort/)
  * [Stalin sort](https://www.youtube.com/shorts/W6WTCJwdWMo)