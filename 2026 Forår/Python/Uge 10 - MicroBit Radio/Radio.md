# Micro:Bit Radio

## Resultatet

I dag skal vi lege med muligheden for at sende beskeder mellem forskellige Micro:Bit. Hver Micro:Bit har en indbygget radio som kan forbinde til andre Micro:Bit og de kan sende data til hinanden.  
Dette kan vi bruge til at lave små spil og lege.

Det er muligt at lave øvelserne både som grafisk eller Python programmering. Brug gerne Python delen, da vi i næste uge ikke vil kunne lave det grafisk (det bliver i hvert faldet svært!)

## Indledende øvelser

Vi får brug for at kunne arbejde sammen. Det er nemmest hvis man har sine egne ting klar fra start.  

Vi skal have oprettet flere små projekter. På siden [MakeCode](https://makecode.MicroBit.org/) kan man have flere forskellige projekter samtidig.

Start med at gennemføre disse projekter, så du har noget kode klar at arbejde videre med:
1. [Terning med tal](https://MicroBit.org/projects/make-it-code-it/dice/?editor=python) eller  [Grafisk terning](https://MicroBit.org/projects/make-it-code-it/graphical-dice/?editor=python)  
   Man må godt lave begge to, hvis man har lyst.

2. [Sten saks papir](https://MicroBit.org/projects/make-it-code-it/rock-paper-scissors/?editor=python)s

## Radio øvelser

Her får i brug for at arbejde sammen 2 og 2.

Vi starter med nogle nemme radio øvelser. Dette er projekter som bare kan kopieres ind, så vi kan se hvordan det virker med radio i Micro:Bit.  
I øvelsen ser i den følgende linje:
```python
radio.config(group=2)
```
Her skal i vælge jeres eget tal mellem 0 og 256. Tallet skal være det samme hos dig og den makker du arbejder sammen med. Jeg valgte 42, så koden blev:
```python
radio.config(group=42)
```

Prøv at se om i kan få disse projekter til at virke:
1. [Send et smil](https://MicroBit.org/projects/make-it-code-it/send-a-smile/?editor=python)
2. [Teleporterende and](https://MicroBit.org/projects/make-it-code-it/teleporting-duck/?editor=python)

## Sæt det sammen 1 - Flere terninger

Nu er der ikke mere kode til at hjælpe, så nu skal i selv have sat noget af det i har lavet sammen.  

Vi skal stadig arbejde 2 og 2.

Til at starte med skal vi bruge vores terning program vi lavede tidligere. Kan i koble jeres 2 Micro:Bit sammen, så når den ene slår et nyt tal, så gør den anden det også?

Hvis Lasse og Lise har en Micro:Bit, skal vi kunne ryste Lises Micro:Bit, og så kommer der et nyt tal på både Lise og Lasses Micro:Bit. Også uden at vi rører Lasses Micro:Bit.  
Kan vi også få det til at virke, hvis det er Lasses Micro:Bit der rystes?

Når i har det til at virke, kan i prøve at se om det virker med flere terninger samtidig? Kan vi få det til at virke med 3, 4 eller 10 Micro:Bit?

## Sæt det sammen 2 - Svær! - Sten saks papir mod hinanden.

Her skal man stadig arbejde sammen 2 og 2.

Kan i rette sten, saks papir programmet til så det gør følgende:
1. Når programmet starter kan man skifte mellem sten, saks og papir ved at trykke på 'A'.
2. Man vælger det skærmen viser ved at trykke på 'B'.
3. Når begge spillere har valgt noget, skal vinderens skærm vise en glad smiley og taberens skærm skal vise en sur smiley.
4. Ved at ryste sin Micro:Bit nulstiller skærmen og starter et nyt spil.