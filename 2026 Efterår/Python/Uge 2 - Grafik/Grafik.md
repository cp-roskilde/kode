# Grafiske spil

## Resultatet

I dag skal vi se på at lave grafik på skærmen i Python. Det gør vi med to små spil. Koden til spilene er allerede skrevet, men der er udvidelser der kan laves.

Vi har to spil i dag. Det ene arbejder med tastaturet og det andet med musen.

## Forudsætninger
Vi skal bruge et library der hedder `pygamme`. Få en instruktør til at hjælpe med at lægge det ind i dit udviklings-miljø.  

## Tastatur spil
I tastatur spillet har vi en cirkel, som vi kan rykke rundt på skærmen med piletasterne. Koden til spillet kan findes i filen [tastatur.py](tastatur.py)

### Opgave 1 - Sæt en anden hastighed
Lige nu bevæger cirklen sig lidt langsomt. Kan du få den til at bevæge sig hurtigere (så man stadig kan styre den)?

> [!TIP]
> Se efter en variabel der hedder noget med `speed`.  
> Kan du finde den rigtige?

### Opgave 2 - Farve
Kan du finde ud af hvordan du giver cirklen en anden farve?

> [!TIP]
> Se efter en variabel der hedder noget med `color`.  

Kan du gøre cirklen gul?

### Opgave 3 - Størrelse
Cirklen kan være lidt lille. Kan du gøre den større?  
Til den næste opgave vil en størrelse på 50 måske gøre det nemmere.

> [!TIP]
> Se efter en variabel der hedder noget med `size`.

### Opgave 4 - Bliv på banen
Lige nu kan man gå helt udenfor skærmen. Kan du rette koden til så cirklen bliver sat tilbage til midten af skærmen, hvis den rører siden?

> [!TIP]
> Det er nemmest at lave der hvor der står `# Handlinger` i koden.

Kan du få cirklen til at komme tilbage lige så snart den rører siden, og ikke først når midten af cirklen kommer udenfor banen?

## Mus spil
I mus spillet kommer der cirkler frem på skærmen, som vi skal klikke på med musen. Koden til spillet kan findes i filen [mus.py](mus.py)

### Opgave 1 - Flere cirkler
Nogle gange bliver der lidt kedeligt at vente på der kommer en cirkel. Kan du gøre så der kommer flere cirkler?

> [!TIP]
> Se efter en variabel der hedder noget med `circle_chance`.

Hvis du sætter tallet for højt, kan der komme _mange_ cirkler meget hurtigt.  
Sæt eventuelt en begrænsning på hvor mange cirkler der må være.

> [!TIP]
> Det kan gøres med koden `if random.random()<=new_circle_chance and len(circles)<10:`, men hvor skal det stå?

### Opgave 2 - Skift farve
Det er lidt kedeligt med kun en farve.

Kan du få cirklerne til at skifte farve så de små er gule. Når de bliver større skal de skifte til orange og når de er store skal de blive røde?

Dette er en lidt svær opgave man skal tænke over.