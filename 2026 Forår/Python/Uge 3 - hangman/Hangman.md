# Hangman / Galgeleg

## Resultatet

Vi skal i dag lave en applikation, hvor man kan spille hangman eller galgeleg.

Når vi starter programmet vil det bede brugeren om at gætte et bogstav. Hvis man gætter et bogstav der er i ordet, viser den hvor i ordet bogstavet er.

Når man har bogstaver nok til at gætte ordet, kan man skrive det ord man gætter på og se om man gætter rigtig.

Her nedenfor er et eksempel på afviklingen af spillet:

```
>> 
>> Jeg kan et ord på 4 bogstaver. Kan du gætte det?
>> _ _ _ _ 
Skriv et bogstav eller gæt på et ord: u
>> Det bogstav er desværre ikke i ordet.
>> 
>> Jeg kan et ord på 4 bogstaver. Kan du gætte det?
>> _ _ _ _ 
Skriv et bogstav eller gæt på et ord: e
>> Godt gættet. Det bogstav er i ordet.
>> 
>> Jeg kan et ord på 4 bogstaver. Kan du gætte det?
>> _ _ e _ 
Skriv et bogstav eller gæt på et ord: m
>> Godt gættet. Det bogstav er i ordet.
>> 
>> Jeg kan et ord på 4 bogstaver. Kan du gætte det?
>> _ _ e m 
Skriv et bogstav eller gæt på et ord: hjem
>> Godt gættet.
```

## Kode del 1: Opret variabler til spillet
Vi skal i dat bruge to variabler:

```python
word = "gedebuk"
```

Her sætter vi variablen `ord` til det ord der skal gættes. Der kan godt laves flere muligheder senere, men lad os starte simpelt.

```python
guessed = []
```

Her sætter vi variablen `guessed` til en tom liste. Denne liste vil komme til at indeholde alle de gæt spilleren har lavet. Listen er tom, da der ikke er gættet på noget endnu.

## Kode del 2: Kommunikation med brugeren
Vi skal have skrevet til brugeren hvad der skal ske, og brugeren skal kunne komme med et gæt.

```python
print()
print("Jeg kan et ord på "+str(len(word))+" bogstaver. Kan du gætte det?")
```

Her skrives til skærmen med `print` funktionen. Den første print funktion skriver ikke noget. Det giver en tom linje på skærmen, så det er nemmere at se forskel på de forskellige gæt.

> [!TIP]  
> Kan du gennemskue hvad denne del af koden gør: `str(len(word))`?

Nu skal brugeren kunne komme med sit gæt:

```python
response = input("Skriv et bogstav eller gæt på et ord: ")
guessed.append(response)
```

Her skriver vi til brugeren at de skal komme med et gæt, og vi gemmer det brugeren har skrevet i variablen `response`.
`response` er det brugeren har gættet lige nu. For at kunne huske gættet senere, tilføjer vi det til `guessed` listen. 
Dette gøres med funktionen `Append`.

## Kode del 3: Brugeren har gættet et bogstav

Vi vedtager at et gæt på ét tegn, altid er et gæt på et bogstav og et gæt på flere tegn er et gæt på hvad ordet er.

Til at starte med laver vi noget kode til når brugeren gætter på et enkelt tegn:
```python
if (len(response))==1:  # Hvis der kun er et tegn
  if response in word: print("Godt gættet. Det bogstav er i ordet.")
  else: print("Det bogstav er desværre ikke i ordet.")
```

> [!WARNING]  
> Det er vigtigt at de to sidste linjer i blokken har noget mellemrum foran. Det er denne måde programmeringssproget ved hvad den skal gøre.

Her checker vi om `response` har en længde på 1. Hvis den har det, ved vi at det er et enkelt bogstav.

Herefter kan vi checke om det enkelte bogstav er med i `word` og skrive til brugeren om de gættede girgit eller forkert.

## Kode del 4: Brugeren har gættet på et ord

Hvis brugeren har skrevet noget der ikke er et enkelt bogstav, har de nok forsøgt at gætte ordet. Lad os kontrollere om ordet er rigtig:

```python
else: #Hvis der er noget andet end 1 tegn.
  if response==word:
    print("Godt gættet.")
  else:
    print("Nej, ordet var ikke '"+ response +"'")
```

Da vi før checkede om `response` havde en længde på 1, kan vi bruge udtrykket `else` til at se om den har en anden længde. Hvis det har en anden længde, er der gættet på et ord, og vi ser om der er gættet rigtigt.

Hvis `resonse` er det samme som `word` har brugeren gættet rigtigt.

## Kode del 5: Skriv de gættede bogstaver til skærmen
For at brugeren har en chance for at gætte rigtig, skal de kunne se hvor de gætttede bokstaver står.

Tilføj denne stump kode __FØR__ linjen med `response = input("....")`

```python
for letter in word:
  if (letter not in guessed): letter = "_" # Hvis bogstavet ikke er gættet gør vi det hemmeligt.
  print(letter, end=" ")
print()
```

Her går vi igennem alle bogstaverne i `word` et ad gangen, og kalder dem for `letter`.

For hver bogstav ser vi om det er blevet gættet. Hvis det <u>ikke</u> er blevet gættet skriver vi et `_` i stedet for.

Bogstavet skrives ud på den nederste linje. Normalt når vi bruger printer, skriver den en linje. For at den ikke gør det for hvert bogstav, har vi tilføjet `, end=" "`.  
Dette fortælle print kommandoen at den ikke skal lave et linjeskift, men bare et mellemrum mellem hver bogstav.

Til sidst laver vi en print der skriver en tom linje, for at få et linjeskift efter det sidste bogstav.

## Kode del 6: Lad brugeren gætte flere gange
Lige nu lader programmet os kun gætte en gang, og så stopper det. 

Spillet virker bedst hvis man kan gætte flere gange.

Lige efter vi har skrevet variablerne `word` og `guessed` tilføjes koden:

```
while True:
```

Og alle linjer nedenunder den indsatte linje får to mellemrum foran. Koden rykkes ind under `while` og bliver til det vi kalder en blok.

## Ekstra opgave 1 (nem) - Lad programmet vælge mellem flere ord
I stedet for koden med `ord = "gedebuk"`, tilføjes koden:

```
import random
words = [
  "hund",
  "hest",
  "hjem",
  "hule",
  "test"
  "telt",
  "trop"
]
word = random.choice(words)
```

Her laver vi en liste med navnet `words`, som indeholder en række mulige ord. Herefter vælger vi et enkelt ord fra listen.

## Ekstra opgave 2 (nem) - Tilføj endnu flere ord

Kan du selv finde en god måde at udvidde med endnu flere mulige ord?

## Ekstraopgave 3 (mellem) - Afslut spillet når der gættes rigtig.

Lige nu fortsætter spillet selv om man gætter rigtig. KAn du få spillet til at slutte når man gætter rigtig?

Udskift koden med `while True` til:

```python
response = ""
while response!=word:
```

## Ekstraopgave 3 (svær) - Giv spilleren et antal gæt.
Lige nu har man uendelig mange gæt. Lad spilleren tabe, hvis der er gættet på noget forkert 10 gange.

Her er nogle kode-stumper, men du skal selv finde ud af at sætte dem fornuftige steder i din kode.

```python
fails = 0
fails_max = 10
```

```python
while response!=word and fails!=fails_max:
```

```python
fails = fails +1
```
