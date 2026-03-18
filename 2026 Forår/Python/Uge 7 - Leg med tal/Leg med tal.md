# Leg med tal

## Resultatet

I dag gør vi det lidt anderledes. Vi skal se på nogle kodestumper og forså hvad de gør. Ud fra det vi lærer med disse stumper skal vi selv skrive programmer der kan lave nogle beregninger. Vi får ikke svaret leveret, men skal selv finde ud af det.

Vi skal lave følgende beregninger:
 * Plus minus gange og divider
 * Beregne fibbonachi tal
 * Beregne summen af mange tal
 * Beregne primtal

## Eksempel 1 - Sådan tæller vi:

I python findes der en funktion vi har brugt før, uden at se dybere på hvad den gør. Nu skal vi prøve at forstå hvad denne funktion gør.

Funktionen hedder `range`. Prøv at køre de enkelte stykker kode herunder og se hvad den gør.

En funktion der tæller til 10.  
Hvad er det __første__ tal den tæller med?  
Hvad er det __sidste__ tal den tæller med?
```python
for i in range(10):
    print(i)
```

En funktion der tæller fra 10 til 20:  
Hvad er det __første__ tal den tæller med?  
Hvad er det __sidste__ tal den tæller med?
```python
for i in range(10, 20):
    print(i)
```

Hvad gør så denne kode? Kan du gennemskue det?
```python
for i in range(1, 20, 2):
    print(i)
```

Og hvad med denne:

Hvad gør så denne kode? Kan du gennemskue det?
```python
for i in range(0, 20, 4):
    print(i)
```

## Eksempel 2 - Sådan kan vi regne med tal
Ligesom i matematik kan vi også lave regnestyker.
 * Addition (plus) skrives med `+`
 * Subtraktion (Minus) skrives med `-`
 * Multiplikation (gange) skrives med `*`
 * Division (divider) skrives med `/`

Her er nogle eksempler på regnestykker i kode:
```python
a = 3
b = 6
# Det samme som print( 3 + 6 )
print( a + b )
```

```python
a = 7
b = 4
# Det samme som print( 7 - 4 )
print( a - b )
```

```python
a = 7
b = 8
# Det samme som print( 7 * 8 )
print( a * b )
```

```python
a = 7
b = 2
# Det samme som print( 7 / 2 )
print( 7 / 2 )
```

Nogle gange kan matematiken godt blive lidt svær.  
Kan du gætte hvad denne kode skriver til skærmen inden du kører koden?   
Regnede du rigtig? (Svaret er __ikke__ `22`)
```python
print( 2 * 6 + 2 * 5 )
```

## Eksempel 3 - Division med heltal
Lige før så vi at Python kunne beregne `7 / 2` og fik `3.5`. Det er også rigtig beregnet. 

Nogle gange vil vi i vores kode kun regne med heltal. Et heltal er et tal der ikke har et komma i.

Vi har derfor 2 nye regne-tegn:
 * Heltalsdivision (divider heltal) `//`
 * Modulus (Find rest) `%`

Heltalsdivision virker bedst når vi snakker om ting der ikke kan deles til mindre dele end 1. Tænk på katte. Hvis to børn skal klappe 5 geder, kan hver barn klappe 2 geder og så er der en tilbage. Det giver ikke mening at klappe 2 og en halv ged. Det bliver meget blodigt at skære den sidste ged over!

Prøv at se hvad denne kode gør:
```python
for i in range(10):
    print(i)
    print(f"\t{i} / 3 = ", i / 3)
    print(f"\t{i} // 3 = ", i // 3)
    print(f"\t{i} % 3 = ", i % 3)
```

## Opgave 1 - Regnestykker med plus, minus, gange og divider.
Vi skal lave et program der laver beregninger med to tal.
I får denne kode:
```python
def tal():
    while True:
        try:
            tal = int(input("Indtast et tal:"))
            return tal
        except ValueError:
            print("Du skal indtaste et tal, prøv igen.")

a = tal()
b = tal()

print(f"De tal du indtastede var {a} og {b}.")
```

Kan du udvidde programmet til at skrive hvad disse regnestykker giver:
 * a + b
 * b + a
 * a - b
 * b - a
 * a * b
 * b * a
 * a / b
 * b / a

 Hvis jeg vælger tallene 4 og 2 kunne programmet skrive dette til skærmen:
 ```
 De tal du indtastede var 4 og 2.
4 + 2 = 6
2 + 4 = 6
4 - 2 = 2
2 - 4 = -2
4 * 2 = 8
2 * 4 = 8
4 / 2 = 2.0
2 / 4 = 0.5
 ```

### Udvidelse 1
Hvad sker der, hvis et af tallene er ´0`? Kan du finde en løsning til at programmet ikke crasher?

### Udvidelse 2
Kan du udvidder programmet til også at vise hvad regnestykket giver, hvis man bruger heltals-division og hvad resten bliver? 


## Opgave 2 - Fibbonachi tal
Fibbonachi tal er en talrække som starter med to `1`taller. Man kan altid finde det næste tal i rækken, ved at lægge de to sidste tal sammen.
```
1     1
2     1
3     2    (1+1)
4     3    (1+2)
5     5    (2+3)
6     8    (3+5)
7    13    (5+8)
8    21    (8+13)
9    34    (13+21)
10   55    (21+34)
```

Kan du skrive et program der kan beregne flere Fibbonachi tal?

Prøv at se om du kan beregne Fibbonachi tal nr 100.  
Hvis du har regnet rigtig får du: `354224848179261915075`

## Opgave 3 - Beregne summen af mange tal
Lad os forestille os vi har tallene op til 10:
```
0 1 2 3 4 5 6 7 8 9
```

Hvis vi lægger disse tal sammen får vi `45`.

Hvad nu hvis vi tager de første 100 tal?

Du kan starte med denne kode, og så beregne summen af tallene fra 0 til `a`:
```python
def tal():
    while True:
        try:
            tal = int(input("Indtast et tal:"))
            return tal
        except ValueError:
            print("Du skal indtaste et tal, prøv igen.")

a = tal()
```

Hvis man indtaster tallet 33, kunne programmet skrive:
```
Tallene er:  0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33
Summen af tallene er:  561
```

Det er mest resultatet `561` vi er ude efter.

## Opgave 4 - Primtal
Der findes nogle tal vi kalder for primtal. Et primtal er et tal, som ikke kan deles med andre tal og give et heltal.

Har man `7` stykker kage, kan man kun fordele dem til `1` eller `7` børn, hvis alle skal have lige mange stykker.  
Har man `2`, `3`, `4`, `5` eller `6` børn, får de ikke lige mange stykker, eller også bliver der stykker til overs.

De første 10 primtal er:
```
2
3
5
7
11
13
17
19
23
29
```

Kan du skrive et program der kan teste om et tal er et primtal?

Du kan starte med denne kode, og så beregne om `a` er et primtal:
```python
def tal():
    while True:
        try:
            tal = int(input("Indtast et tal:"))
            return tal
        except ValueError:
            print("Du skal indtaste et tal, prøv igen.")

a = tal()

```

Jeg har to eksempler på kørsler af programmet og det svar vi gerne vil have:
```
Indtast et tal:89
89 er et primtal.
```

```
Indtast et tal:99
99 er et primtal.
```

### Udvidelse - Find primtal selv

Når først du kan beregne om et tal er et primtal kan du også beregne flere primtal.

I stedet for at lade brugeren skrive et tal, kan vi undersøge alle tal op til 100:
```python
for a in range(2,100):
    # Check om det er et primtal
```

Hvis det virker, burde koden udskrive noget i retning af:
```
2 er et primtal.
3 er et primtal.
4 er ikke et primtal.
5 er et primtal.
6 er ikke et primtal.
7 er et primtal.
8 er ikke et primtal.
9 er ikke et primtal.
10 er ikke et primtal.
11 er et primtal.
12 er ikke et primtal.
13 er et primtal.
14 er ikke et primtal.
15 er ikke et primtal.
16 er ikke et primtal.
17 er et primtal.
18 er ikke et primtal.
19 er et primtal.
20 er ikke et primtal.
21 er ikke et primtal.
22 er ikke et primtal.
23 er et primtal.
24 er ikke et primtal.
25 er ikke et primtal.
26 er ikke et primtal.
27 er ikke et primtal.
28 er ikke et primtal.
29 er et primtal.
30 er ikke et primtal.
31 er et primtal.
32 er ikke et primtal.
33 er ikke et primtal.
34 er ikke et primtal.
35 er ikke et primtal.
36 er ikke et primtal.
37 er et primtal.
38 er ikke et primtal.
39 er ikke et primtal.
40 er ikke et primtal.
41 er et primtal.
42 er ikke et primtal.
43 er et primtal.
44 er ikke et primtal.
45 er ikke et primtal.
46 er ikke et primtal.
47 er et primtal.
48 er ikke et primtal.
49 er ikke et primtal.
50 er ikke et primtal.
51 er ikke et primtal.
52 er ikke et primtal.
53 er et primtal.
54 er ikke et primtal.
55 er ikke et primtal.
56 er ikke et primtal.
57 er ikke et primtal.
58 er ikke et primtal.
59 er et primtal.
60 er ikke et primtal.
61 er et primtal.
62 er ikke et primtal.
63 er ikke et primtal.
64 er ikke et primtal.
65 er ikke et primtal.
66 er ikke et primtal.
67 er et primtal.
68 er ikke et primtal.
69 er ikke et primtal.
70 er ikke et primtal.
71 er et primtal.
72 er ikke et primtal.
73 er et primtal.
74 er ikke et primtal.
75 er ikke et primtal.
76 er ikke et primtal.
77 er ikke et primtal.
78 er ikke et primtal.
79 er et primtal.
80 er ikke et primtal.
81 er ikke et primtal.
82 er ikke et primtal.
83 er et primtal.
84 er ikke et primtal.
85 er ikke et primtal.
86 er ikke et primtal.
87 er ikke et primtal.
88 er ikke et primtal.
89 er et primtal.
90 er ikke et primtal.
91 er ikke et primtal.
92 er ikke et primtal.
93 er ikke et primtal.
94 er ikke et primtal.
95 er ikke et primtal.
96 er ikke et primtal.
97 er et primtal.
98 er ikke et primtal.
99 er ikke et primtal.
```

### Udvidelse - Hvor hurtigt kan dit program finde alle primtal under 1000?

Hvis du sætter disse to linjer ind i toppen af dit program:
```python
from datetime import datetime
start = datetime.now()
```

Og disse to linjer ind i bunden af programmet:
```python
slut = datetime.now()
print(f"Det tog {slut - start} at køre programmet.")
```

Så vil programmet når det er færdigt skrive hvor lang tid det tog om at lave alle beregningerne.

Jeg startede med at kunne beregne 10.000 primtal på `4,22` sekund.
Efter nogle optimeringer kom det ned på, `0.8` sekund.

Hastigheden afhænger meget af computeren. Det spændende er hvor meget hurtigere den bliver end første gang.