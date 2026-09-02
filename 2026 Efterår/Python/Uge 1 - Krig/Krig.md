# Kortspil: Krig

## Resultatet

I dag skal vi lave en simulation af kortspillet krig. Hvis du ikke kender spillet, er det beskrevet her: [Wikipedia - Krig (Kortspil)](https://da.wikipedia.org/wiki/Krig_(kortspil)).

Det er et rimelig simpelt spil, som giver os mulighed for at arbejde med nogle lidt mere komplekse koncepter og se hvordan de virker.

## Vores første klasse
Vi skal i dag arbejde med det der hedder klasser. En klasse er noget kode som beskriver et koncept. Dette koncept kan såm genbruges igen og igen. Et koncept kan være hvad som helst; en bil, et hus, et hjul, en sten. Typisk de ting vi beskriver med navneord. En klasse kan godt indeholde andre klasser (en bil har hjul).

Da vi skal lave et kortspil skal vi have en klasse der beskriver et kort. 

Start med at kopier denne kode ind i dit projekt:
```python
class Card:

    suit = [
        "hjerter","ruder","klør","spar"
    ]

    def __init__(self, value):
        self.value = value
        self.suitValue = value // 13
        self.numberValue = value % 13

    def __str__(self):
        return Card.suit[self.suitValue]+ " " + (
            "es" if self.numberValue == 0 else
            "konge" if self.numberValue == 12 else
            "dame" if self.numberValue == 11 else
            "bonde" if self.numberValue == 10 else
            str(self.numberValue+1)
        )
```

Her beskriver vi klassen kort. Vi beskriver et kort som en talværdi. I et sæt spillekort uden jokere er der 52 kort. Så vi bruger et tal mellem 0 og 51 til at beskrive et kort. Dette tal er det vi kalder `value`.

Værdien fra `value` bliver regnet om til to andre værdier:
```python
self.suitValue = value // 13
```
Her bliver suitValue sat til værdien (heltals)divideret med 4. Det gør at vi får et af tallene 0, 1, 2 eller 3. Dette beskriver typen af kort. Som i kan se har vi en liste af kort-typer som vi kalder `suit`. Her vil `0` bliver oversat til `hjerter`, `1` bliver oversat til `ruder`, `2` bliver oversat til `klør` og `3` bliver oversat til `spar`.

```python
self.numberValue = value % 13
```
Her bliver numberValue sat til det der er til overs når vi har divideret med 13. Dette passer med at hver kulør har 13 værdier. Es (1), 2, 3, 4, 5, 6, 7, 8, 9, 10, bonde, dronning, konge. I numberValue husker vi bare tallet for hvad det er. 

> [!TIP]  
> Husk at computere tæller fra 0 og ikke 1. Så værdien `0` er `es` og værdien `1` er kortet `2`.

Værdierne for kortet sættes i metoden `__init__`, som er en metode i alle klasser. Det er denne metode der bruges når man laver en ny instans a klassen. En klasse beskriver bare hvad et kort er. En instans er et enkelt kort, og har man flere kort, har man flere instanser af samme klasse.

Der er også en `__str__` metode. Denne bruges når vi ønsker at udskrive kortet til skærmen. Denne kan vi afprøve med et par forskellige.

Prøv at tilføje og kør nedenstående kode:
```python

if __name__=="__main__":
  kort1 = Card(22) # Lav et kort med værdien 22 og kald det for kort1
  print(kort1)     # Udskriv kortet til skærmen

  kort2 = Card(42) # Lav et kort med værdien 42 og kald det for kort2
  print(kort2)     # Udskriv kortet til skærmen
```

## Endnu en klasse
Nu kan vi beskrive et kort. Men i krig har hver spiller en bunke af kort. En bunke af kort er også en ting, og kan også beskrives som en klasse. Her kalder vi den `Deck`:
```python
class Deck:
    def __init__(self, cards=None, name = "Bunke"):
        self.name = name
        self.cards = cards if cards is not None else []

    @classmethod
    def allCards(cls):
        cls([Card(x) for x in range(52)])

    def split(self, players):
        result = [Deck([],"Spiller "+str(x+1)) for x in range(players)]
        while self.cards:
            for player in result:
                player.addCard(self.cards.pop())
        return result

    def shuffle(self):
        random.shuffle(self.cards)

    def addCard(self, card):
        self.cards.append(card)

    def removeCard(self, card):
        self.cards.remove(card)

    def pickCard(self):
         card = self.cards[0]
         self.removeCard(card)
         return card

    def __len__(self):
      return len(self.cards)

    def __str__(self):
        return "'"+self.name+"' med "+str(len(self.cards))+" kort"
```

Som det kan ses kort-klassen noget mere. Kad os tage det fra toppen af:

`__init__` metoden er den der bruges til at oprette en ny bunke af kort. Den tager imod to parametre.
 * cards  - En liste ad de kort der skal være i bunken.
 * name   - Navnet på bunken af kort så vi ved hvilken bunke det er.

 `allCards` er en særlig metode. Da der står `@classmethod` foran, betyder det at det er en metode der kan kaldes på klassen `Deck` og ikke på en enkelt bunke. Denne metode returnerer en bunke med alle 52 kort i.  
 Hvis dette lyder lidt forvirrende er det okay. Det skal vi nok lære på et tidspunkt.

 `shuffle` tillader at vi kan blande kortene i bunken.

 `split` deler bunken i et antal lige store _nye_ bunker. Hvis 52 kort deles til 2 spillere får de 26 hver. Hvis der er 3 spiller vil den første få 18 kort og de to sidste vil få 17 kort hver. Værdien `players` er antallet af spillere der skal deles ud til.

 `addCard` Lægger et kort nederst i bunken.

 `removeCard` Leder hele bunken igennem og fjerner et bestemt kort, hvis det er der.

 `pickCard` Tager det øverste kort i bunken, fjerner det fra bunken og returnerer det. 

 `__len__` er en særlig Python metode der bruges til at få størrelsen på noget. Her bruger vi den til at give størrelsen på bunken af kort. Den returnerer hvor mange kort der er i bunken.

 `__str__` kender vi allerede fra Card. Her skriver den navnet på bunken i stedet for og hvor mange kort der er i bunken.

 ## En klasse i selv skal udfylde på
 Endelig får vi brug for en klasse som beskriver spillet krig. Et spil er også en ting og derfor også noget der kan beskrives med en klasse.

 Start med at kopiere denne kode ind:
 ```python
 class Krig:
    def __init__(self, players=2):
        self.round = 0                    # Vi starter med der ikke er spillet nogen runder endnu
        
        d = Deck.allCards()               # Tag et kortspil
        d.shuffle()                       # Bland korspillet
        self.players = d.split(players)   # Del kortene ud til spillerne
        self.table = Deck([],"bordet")    # Dette er en tom bunke der består af de kort der ligger på bordet

    def finished(self):
       """
       Denne metode skal returnere True hvis der kun er en spiller tilbage med kort i sin bunke
       """
       pass

       # Skriv kode her så det virker.

    def action(self):
        """
        Denne metode skal spille en runde af spillet.
         - Alle spillere trækker et kort og lægger det på bordet.
         - Den spiller der har det højeste kort får alle kortene fra bordet.
         - Es er det højeste kort
         - 2 er det laveste koret

        Hvis to spillere trækker samme kort er der krig.
        """
        if self.finished(): return True

        self.round += 1
        print("Runde "+str(self.round))

        # Skriv kode her så det virker.
 ```

Som det kan ses er der to metoder her der ikke er udfyldt. KAn du finde ud af at skrive denne kode?

For `action` metoden kan reglerne for når der kommer "krig" være lidt besværlige. Til at starte med kan det her vælges bare at lade kortene ligge på bordet og lade vinderen af næste runde få dem. Når det virker kan man så prøve at lave de rigtige regler.

For at teste programmet tilføjes denne kode til sidst:
```python
if __name__=="__main__":
    k = Krig()
    while not k.finished():
        result = k.action()
```

## Udvidelser til spillet - del 1
Kan du få spillet til at spille afvikle krig mellem to spillere rigtigt, hvor hver spiller lægger 3 kort først, og så vender et kort for at se hvem der vinder?
 * Hvad sker der hvis en af spillerne ikke har kort nok?
 * Hvad sker der hvis hvis det bliver uafgjort igen?
 * Hvad sker der hvis alle spillerne i en krig løber tør for kort samtidig?

 ## Udvidelser til spillet - del 2
 Hver gang en runde spilles, tælles dette op i koden. Kan du få dit program til at spille 10 spil og skrive hvor mange træk der var i hvert spil?
  * Hvor mange kort skal man i gennemsnit vende for at vinde et spil?
  * Bliver tallene noget andet med 4 spillere i stedet for 2? 