# Micro:Bit Radio 2

## Resultatet

I dag har vi to forskellige opgaver. De hænger ikke sammen, og det kan derfor vælges, hvilken opgave vi starter med.

De to opgaver er:
 * Sten saks papir med to Mikro:Bit
 * Hemmelige kodler mellem Mikro:Bit

Begge opgaver kan løses i [Makecode](https://makecode.microbit.org/#).

## Opgave 1 - Hemmelige koder mellem mikrobit
Vi skal prøve at lave et program der kan sende en tekst fra en mikrobit til den anden. Dette kan gøres med blokke, som det ses her:
![Opgave 1 blokke](opg1-blocks.png)

Hvis dette program lægges ned på to Mikro:Bit kan i trykke på `A` på den ene Mikro:Bit og se at beskeden skrives på den anden Mikro:Bit.

En af de første øvelser vi lavede, handlede om at 'kryptere' en tekst så andre ikke kunne læse den. Løsningen til denne opgave kan findes [her](../Uge%202%20-%20Hemmelig%20kode/løsning.py). Beksrivelsen af hvordan vi kom frem til denne kode kan læses i [Uge 2](../Uge%202%20-%20Hemmelig%20kode/Hemmelig%20kode.md) opgaven.

 * Kan I rette koden til jeres Mikro:Bit til så den sender en "krypteret" tekst til den anden?

 * Kan i også rette koden til så den modtagne tekst bliver "af-krypteret" og vises korrekt på skærmen?
 
## Opgave 2 - Sten saks papir med to Mikro:Bit

Målet her er at lave et program der kan spille Sten saks Papir mellem to Mikro:Bit. Det var en ekstra-opgave sidste uge, men ingen nåede i mål med denne, så lad os prøve igen.

Programmet skal virke sådan at jeres Mikro:Bit skal starte op og vises et ikon der betyder `sten`. Hvis brugeren trykker på `A` skal der skiftes mellem `sten`, `saks` og `papir`.  
Når brugeren trykker `B` vælger man det skærmen viser. Man kan nu ikke længere skifte sit valg, og det valgte sendes til den andens Mikro:Bit.  
Når begge spillere har valgt noget skal skærmen om man har vist (Glad smiley) eller Tabt (Ked smiley).
Når brugeren trykker på `A` eller `B` startes et nyt spil, og skærmen viser igen en `sten` så brugeren kan vælge sit næste træk.

Det kan være en god ide at kode dette med blokke først.

Koden til at gøre dette benytter noget der hedder en `state-machine`. Det er noget kode der holder styr på hvad vi er i gang med i programmet.

I får ikke leveret noget kode til denne øvelse, men de forskellige states i får brug for er tegnet op her nedenfor.  
Firkanterne er en state, hvor vi venter på at noget sker.
Pilene med tekst på er noget der sker.
Teksten i cirklerne er det der skal ske.

```mermaid
flowchart TD
    start[Mikro:Bit starter op]
    start --> start-s1((Sæt radio kanalen)) --> start-s2((Sæt `valgt` til 1/sten)) --> start-s3((Sæt state til 1)) --> select
    select[1 - Valg af sten/saks/papir.\nBegge er i gang med at vælge]
    select -- A trykkes --> select-s1((Skift mellem sten/saks/papir\n gem valget i variablen `valgt`)) --> select
    select -- B trykkes --> select-s4((Send det valgte tal)) --> select-s5((Sæt state til 3)) --> wait
    select -- Der modtages at valg fra den anden \n  --> select-s2((Gem den andens valg i variablen `anden`)) --> select-s3((Sæt state til 2)) --> select2
    select2[2 - Valg af sten/saks/papir.\nDen anden har valgt]
    select2 -- A trykkes --> select2-s1((Skift mellem sten/saks/papir)) --> select2
    wait[3 - Du har valgt, vi venter på den anden.]
    wait -- Der modtages at valg fra den anden \n  --> wait-s1((Gem den andens valg i variablen `anden`)) --> wait-s2((Sæt state til 4)) --> check

    select2 -- B trykkes --> select-s6((Send det valgte tal)) --> select-s7((Sæt state til 4)) --> check
    check((Sammenlign variablerne `valgt` og `anden`. Vis med en smiley om der er tabt, vundet eller uafgjort.)) --> done
    done[4 - Spillet er slut]

    done -- Tryk på `A` --> select
    done -- Tryk på `B` --> select
```

I får brug for at oprette en variabel der hedder `state`. Når der sker ting (der modtages en besked over radio, eller der trykkes på en knap) er det state der skal bestemme hvad der sker.