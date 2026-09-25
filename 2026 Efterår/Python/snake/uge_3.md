# Snake i Pygame — Uge 3

Denne uge starter vi med at rydde op i noget, der har luret i koden siden
uge 1: de samme tal er skrevet flere gange, i flere forskellige filer.
Det retter vi først. Bagefter fortsætter vi med det, uge 3 ellers handler
om: æblet dukker nu op på et **tilfældigt** sted, og slangen kan rent
faktisk **spise** det.

## Refactorering: delte variabler over flere filer

"At refaktorere" betyder at ændre, hvordan koden er skruet sammen indeni,
uden at ændre, hvad spillet gør udenpå — spillet skal se og opføre sig
præcis som før, bagefter. Vi gør det, fordi den nuværende opbygning gør
det let at lave en bestemt slags fejl, som bliver værre og værre, jo mere
kode vi tilføjer.

### Sådan så det ud i uge 2

Kig på toppen af de to filer, som de så ud efter uge 2:

```python
# snake_game.py
GAME_BOARD = []
CELL_SIZE = 32
BOARD_ROWS = 16
BOARD_COLUMNS = 24
```

```python
# snake.py
BOARD_COLUMNS = 24
BOARD_ROWS = 16
CELL_SIZE = 32
```

Det er **to helt forskellige variabler**, som tilfældigvis hedder det
samme og indeholder de samme tal lige nu. Python ved ikke noget om, at de
"burde" være ens — hver fil har sin egen kopi, og de er kun ens, fordi vi
selv har husket at skrive de samme tal to steder.

*Tænk over:* Hvad sker der, hvis I en dag beslutter jer for et større
bræt, og ændrer `BOARD_COLUMNS = 24` til `BOARD_COLUMNS = 32` i
`snake_game.py` — men glemmer den tilsvarende linje i `snake.py`? Spillet
vil stadig køre, helt uden fejlmeddelelser — men slangen og muren vil
pludselig arbejde ud fra to forskellige bræt-størrelser. Det er netop den
slags fejl, der er svær at opdage, fordi Python ikke advarer jer om det.

### Løsningen: én fælles fil, `globals.py`

I stedet for at gentage tallene i hver fil, samler vi dem ét sted, i en ny
fil, `globals.py`:

```python
# globals.py
def init():
    global GAME_BOARD
    GAME_BOARD = []
    global CELL_SIZE
    CELL_SIZE = 32
    global BOARD_ROWS
    BOARD_ROWS = 16
    global BOARD_COLUMNS
    BOARD_COLUMNS = 24
```

Og øverst i `snake_game.py` kalder vi den, én gang, før noget andet sker:

```python
import globals as GL
GL.init()
```

Herefter kan **alle** filer, der skriver `import globals as GL`, læse de
samme værdier — som `GL.CELL_SIZE`, `GL.BOARD_ROWS` og
`GL.BOARD_COLUMNS`. Det virker, fordi Python kun indlæser en given fil
(et "modul") **én gang**, uanset hvor mange andre filer der importerer
den — alle får fat i den samme, fælles udgave af `globals.py`.

`snake.py` har derfor **ikke længere** sine egne kopier af
`BOARD_COLUMNS`, `BOARD_ROWS` og `CELL_SIZE` — den henter dem i stedet fra
`GL`, for eksempel her, hvor vi skalerer billeder:

```python
import globals as GL

def load(filnavn):
    billede = pygame.image.load(GFX + filnavn)
    return pygame.transform.scale(billede, (GL.CELL_SIZE, GL.CELL_SIZE))
```

### Vigtigt: find og ret ALLE stederne

Det er ikke nok at oprette `globals.py` og slette de gamle linjer
`BOARD_COLUMNS = 24` osv. øverst i de to filer. I skal også igennem
**hver eneste** linje i `snake_game.py` og `snake.py`, der brugte de gamle
navne, og rette dem til `GL.BOARD_COLUMNS`, `GL.BOARD_ROWS`, `GL.CELL_SIZE`
og `GL.GAME_BOARD` — konsekvent, alle sammen, ikke kun de første par I
støder på. Det gælder fx alle de steder, hvor `CELL_SIZE` bruges til at
regne pixel-koordinater ud i `draw_grass()`, `draw_wall()` og
`draw_snake()` — hver eneste af dem skal opdateres, ikke kun toppen af
filen.

Glemmer I én linje et sted, sker der en af to ting, og det er værd at
kende forskel på:

- **Den gode udgave:** Har I slettet den gamle `CELL_SIZE = 32` helt, vil
  Python brokke sig højlydt med en `NameError: name 'CELL_SIZE' is not
  defined`, lige så snart den linje bliver kørt. Det er faktisk en
  **fordel** — I får besked med det samme, og kan se præcis, hvilken
  linje der mangler at blive rettet til `GL.CELL_SIZE`.
- **Den snigende, farlige udgave:** Har I i stedet kun **glemt at slette**
  den gamle `CELL_SIZE = 32` i en af filerne (fordi det er let at overse,
  når man retter mange linjer), får I **ingen fejl** — men I er lige
  tilbage i det problem, refactoreringen skulle løse: den fil har igen
  sin egen, uafhængige kopi af tallet, som stille og roligt kan komme ud
  af trit med `GL`'s udgave, uden at nogen advarer jer om det.

Derfor: når I refaktorerer, skal I gøre begge dele, i denne rækkefølge —
først rette **alle** brugssteder til at bruge `GL.`, og først *til sidst*
slette de gamle, øverste variabel-linjer i hver fil. Kør spillet igen
bagefter, og bekræft, at det stadig ser og opfører sig helt som før — det
er sådan, I ved, at refactoreringen er lykkedes.

### Hvorfor en `init()`-funktion, og ikke bare variabler direkte i filen?

I kunne godt spørge: hvorfor ikke bare skrive

```python
# globals.py
GAME_BOARD = []
CELL_SIZE = 32
BOARD_ROWS = 16
BOARD_COLUMNS = 24
```

direkte i `globals.py`, uden nogen funktion omkring det? Det ville faktisk
også virke rent teknisk — men vi har valgt `init()`-udgaven, og det er
faktisk et mønster, I allerede kender. Kig på den allerførste linje i
`snake_game.py`:

```python
import pygame
pygame.init()
```

Vi importerer `pygame`, og **derefter** kalder vi eksplicit
`pygame.init()`, for at sætte pygame ordentligt op, før vi bruger det. Vi
har gjort nøjagtig det samme med vores eget modul: `import globals as GL`,
og derefter `GL.init()`. Det gør det tydeligt, **hvornår** de delte
værdier bliver sat — på en bestemt linje, vi selv kan se — i stedet for at
det bare "sker" som en usynlig bivirkning af import-linjen.

Der er også en praktisk gevinst: hvis I i uge 4 skal kunne **starte
spillet forfra** efter "Game Over", kan I genbruge `GL.init()` til at
nulstille de delte værdier. Det kan man ikke på samme måde, hvis
værdierne bare stod som almindelige linjer øverst i filen — de bliver kun
kørt allerførste gang, filen importeres, og aldrig igen, uanset hvor mange
gange man skriver `import globals` et andet sted.

### Hvad hører til i `globals.py` — og hvad gør ikke?

Bemærk, at vi **ikke** har flyttet `score`, `snake_body` eller `direction`
ind i `globals.py`, selvom `snake_body` og `direction` også bruges af
flere funktioner. Der er en vigtig forskel:

- `CELL_SIZE`, `BOARD_ROWS` og `BOARD_COLUMNS` er **opsætning** — tal, vi
  bestemmer os for, én gang, ved start, og som ikke ændrer sig, mens
  spillet kører. De hører hjemme i `globals.py`.
- `score`, `snake_body` og `direction` er **spillets tilstand** — de
  ændrer sig hele tiden, mens spillet kører, og det er vigtigt, at det kun
  er den fil, der "ejer" dem, som må ændre dem: `snake.py` ejer
  `snake_body` og `direction` (og bruger `global` til at ændre dem inde i
  sine egne funktioner, akkurat som I kender fra `change_direction()`), og
  `snake_game.py` ejer `score`. De bliver, hvor de allerede er.

En tommelfingerregel: **konstant opsætning, brugt flere steder →
`globals.py`. Data, der ændrer sig, og som styres ét sted → bliver i den
fil, der styrer den.**

### En anden måde at dele værdier på: parametre

`globals.py` er ikke den eneste måde, I allerede har brugt til at dele
værdier mellem filer. Kig på `move_snake()` i `snake.py`:

```python
def move_snake(cols, rows):
    ...
```

Den henter **ikke** `BOARD_COLUMNS` og `BOARD_ROWS` fra `GL` direkte — i
stedet sender `snake_game.py` dem med, hver gang funktionen kaldes:

```python
move_snake(GL.BOARD_COLUMNS, GL.BOARD_ROWS)
```

Det er lige så gyldig en måde at dele en værdi på: som **parameter** til
en funktion, i stedet for som et opslag i et fælles modul. Fordelen ved
parametre er, at man kan se **præcis**, hvad en funktion har brug for,
bare ved at kigge på dens definition — man behøver ikke vide noget om
`globals.py` for at forstå, at `move_snake(cols, rows)` bruger `cols` og
`rows`. Ulempen er, at det bliver upraktisk, hvis mange forskellige
funktioner i mange forskellige filer har brug for den samme værdi — så
skal man sende den videre overalt, hver gang.

Derfor bruger vi begge dele i vores kode: `GL` til de værdier, der bruges
bredt (som `CELL_SIZE`, i stort set alle tegne-funktioner), og parametre
dér, hvor det giver mening at se det tydeligt i selve kaldet, som med
`move_snake()`. Det er ikke en fejl, at koden blander de to stilarter —
det er et bevidst valg, alt efter hvad der giver den mest læselige kode
det pågældende sted.

---

## Nyt begreb: tilfældige tal med `random`

Python har et indbygget modul, `random`, som kan give os tilfældige tal.
Vi skal bruge `random.randint(a, b)`, som giver et tilfældigt **heltal**
mellem `a` og `b` — **begge grænser inklusive**:

```python
import random

x = random.randint(0, 5)   # x bliver 0, 1, 2, 3, 4 eller 5 — aldrig 6
```

Det er præcis det, vi skal bruge til at finde et tilfældigt gitter-felt til
æblet.

---

## Uge 3 — Mad og vækst

**Mål for ugen:**
- Placere æblet på et tilfældigt felt på brættet, som ikke allerede er
  optaget af slangen
- Opdage, hvornår slangens hoved rammer æblets felt
- Give slangen et nyt æble, et nyt tilfældigt sted, når det gamle er spist

Vi bygger videre på `snake.py`, som den ser ud efter uge 2's `draw_apple()`
og refactoreringen ovenfor.

### Trin 1 — Find et tilfældigt, ledigt felt

Vi laver en funktion, `place_apple()`, som finder et tilfældigt felt og
gemmer det i en variabel, `apple_pos` — akkurat som `snake_body` og
`direction` er variabler, `snake.py` selv holder styr på.

Brættet har en **mur** rundt om kanten, og `move_snake()` holder allerede
slangen inden for det spilbare område med grænserne `1 <= x <= cols - 2`
og `2 <= y <= rows - 1`. Æblet skal selvfølgelig heller ikke kunne havne
inde i muren, så vi genbruger præcis de samme grænser — men her henter vi
dem direkte fra `GL`, i stedet for som parametre (se afsnittet ovenfor om,
hvornår vi bruger det ene frem for det andet):

```python
import random

apple_pos = (0, 0)  # midlertidig værdi - erstattes med det samme af place_apple()

def place_apple():
    global apple_pos
    while True:
        x = random.randint(1, GL.BOARD_COLUMNS - 2)
        y = random.randint(2, GL.BOARD_ROWS - 1)
        if (x, y) not in snake_body:
            apple_pos = (x, y)
            return

place_apple()  # kald funktionen med det samme, så der er et æble fra start
```

Det interessante her er `while True:` — en løkke, der aldrig stopper af sig
selv. Vi bruger den, fordi vi ikke på forhånd ved, hvor mange gange vi skal
"gætte", før vi rammer et felt, som er frit. Hver gang rundt i løkken:

- Vi gætter et tilfældigt `x` (en kolonne) og `y` (en række) — inden for
  det **spilbare** område, altså uden for muren.
- Vi tjekker `(x, y) not in snake_body` — altså "er denne position **ikke**
  en del af slangen?".
- Hvis feltet er frit, gemmer vi positionen i `apple_pos` og bruger
  `return` til at **afslutte funktionen** — og dermed også løkken, for der
  er ikke mere kode at køre bagefter.
- Hvis feltet **ikke** var frit (slangen lå der), sker der ingenting med
  `return`, og løkken prøver bare igen med to nye tilfældige tal.

*Bemærk:* `place_apple()` kalder vi allerede nu, nederst i filen, uden for
nogen funktion — det sørger for, at der ligger et æble på brættet, **før**
spillet overhovedet starter.

### Trin 2 — Tegn æblet det rigtige sted

`draw_apple()` fra uge 2 tegner lige nu altid på det faste felt `(18, 4)`.
Den skal nu bruge `apple_pos` i stedet:

```python
def draw_apple(screen):
    x, y = apple_pos
    screen.blit(apple_image, (x * GL.CELL_SIZE, y * GL.CELL_SIZE))
```

`apple_image` er stadig den samme, allerede indlæste billede-variabel fra
sidste uge — den rører vi ikke ved.

### Trin 3 — Opdag at slangen spiser æblet

Nu skal vi udvide `move_snake()`, så den opdager, om slangens **nye**
hoved lander præcis der, hvor æblet ligger. Bemærk, at funktionens to
parametre, `cols` og `rows`, er uændrede fra sidste uge:

```python
def move_snake(cols, rows):
    global snake_body
    head_x, head_y = snake_body[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    new_x, new_y = new_head

    inside_board = 1 <= new_x <= cols - 2 and 2 <= new_y <= rows - 1
    if not inside_board:
        return False  # ramte muren - og den spiste heller ikke noget

    ate_apple = new_head == apple_pos

    snake_body = [new_head] + snake_body[:-1]

    if ate_apple:
        place_apple()

    return ate_apple
```

To ting er nye her:

- `ate_apple = new_head == apple_pos` — vi regner det ud, **før** vi
  rykker slangen, og gemmer resultatet (`True` eller `False`) i en
  variabel, så vi kan bruge det bagefter.
- Funktionen **returnerer** nu `ate_apple` til den, der kaldte den — det
  vil sige `snake_game.py`. På den måde kan hovedprogrammet finde ud af,
  om der lige blev spist et æble, uden selv at skulle kende til
  `apple_pos` eller `snake_body`.

Læg mærke til, at når `ate_apple` er `True`, kalder vi `place_apple()` med
det samme, så der ligger et nyt æble klar et andet, tilfældigt sted.

*Bemærk:* Slangen bliver **ikke** længere endnu — `snake_body[:-1]` fjerner
stadig altid det sidste segment, lige meget om der blev spist et æble eller
ej. Det er netop det, Opgave 1 nedenfor handler om at rette.

### Trin 4 — Ret krasch ved hurtige retningsskift

Der er en fejl i `change_direction()`, som kan få spillet til at gå ned,
hvis man banker hurtigt på flere piletaster (eller WASD) lige efter
hinanden. Det viser sig som en `KeyError`, når `draw_snake()` prøver at
slå et hjørne-billede op i `corner_images`, den ikke kan finde.

**Hvad går galt?**

Se på `change_direction()`, som den ser ud nu:

```python
def change_direction(new_direction):
    global direction
    opposite = (-direction[0], -direction[1])
    if new_direction != opposite:
        direction = new_direction
```

Den tjekker, om den nye retning er den modsatte af `direction` — men
`direction` er den samme variabel, som funktionen selv lige har ændret.
Det er fint, så længe spilleren kun trykker **én** tast mellem hvert
`move_snake()`-skridt. Men trykker spilleren **to** taster hurtigt efter
hinanden — inden for det samme 150-millisekunders skridt — bliver
`change_direction()` kaldt to gange, før slangen når at flytte sig
overhovedet. Og anden gang tjekker den op imod den retning, **den selv
lige har sat** ved det første tryk — ikke imod den retning, slangen
*faktisk* er ved at bevæge sig i.

Et eksempel: Slangen bevæger sig **højre**, `direction = (1, 0)`.
Spilleren trykker hurtigt **ned**, og derefter, med det samme, **venstre**:

1. **Ned** trykkes: er `(0, 1)` modsat af `(1, 0)`? Nej → tilladt.
   `direction` bliver `(0, 1)`.
2. **Venstre** trykkes, med det samme: er `(-1, 0)` modsat af `(0, 1)`?
   Nej → *også* tilladt. `direction` bliver `(-1, 0)`.

Hvert enkelt tryk var lovligt for sig — men tilsammen har slangen skiftet
fra **højre** til **venstre**, en fuld 180-graders vending, uden at
`move_snake()` nåede at flytte den bare én gang imellem. Når
`move_snake()` endelig kører, kører slangen lige ind i sin egen hals, og
to segmenter i `snake_body` havner på **samme** felt.

Det er dét, der får `edge_towards()` til at give et mærkeligt resultat:
for et krop-segment, hvor både naboen før *og* naboen efter nu ligger på
nøjagtig samme felt, regner `edge_towards()` en forskel på `(0, 0)` ud —
og ingen af dens `if`-linjer matcher `dx == 0` og `dy == 0`. Funktionen
returnerer derfor ingenting (`None`) for begge naboer. `edges`-mængden
bliver dermed til `{None}` — ét enkelt "ikke-resultat" i stedet for to
rigtige kant-navne — og `corner_images[frozenset(edges)]` fejler, fordi
`None` slet ikke findes som nøgle i opslagsbogen. Det er krashet.

**Løsningen: valider imod den retning, slangen faktisk bevæger sig i**

Fejlen opstår, fordi vi validerer imod en variabel, der kan nå at ændre
sig **flere gange** mellem to skridt. Løsningen er at holde styr på **to**
variabler i stedet for én:

- `direction` — den retning, slangen **faktisk** bevæger sig i lige nu.
  Den må kun ændre sig **inde i `move_snake()`**, én gang pr. skridt.
- `next_direction` — den retning, spilleren **senest har bedt om**. Det
  er den, `change_direction()` opdaterer, hver gang en tast trykkes.

```python
direction = (1, 0)        # den retning, slangen faktisk bevæger sig i lige nu
next_direction = (1, 0)   # den retning, spilleren senest har bedt om

def change_direction(new_direction):
    global next_direction
    opposite = (-direction[0], -direction[1])
    if new_direction != opposite:
        next_direction = new_direction

def move_snake(cols, rows):
    global snake_body, direction
    direction = next_direction

    head_x, head_y = snake_body[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    new_x, new_y = new_head

    inside_board = 1 <= new_x <= cols - 2 and 2 <= new_y <= rows - 1
    if not inside_board:
        return False  # ramte muren - og den spiste heller ikke noget

    ate_apple = new_head == apple_pos

    snake_body = [new_head] + snake_body[:-1]

    if ate_apple:
        place_apple()

    return ate_apple
```

Læg mærke til, at `change_direction()` **stadig** tjekker imod
`direction` — men nu er `direction` "frosset" mellem hvert skridt, fordi
kun `move_snake()` må ændre den, og det gør den kun **én** gang pr. kald,
allerførst i funktionen. Prøv eksemplet igen med den nye kode:

1. **Ned** trykkes: er `(0, 1)` modsat af `direction`, som stadig er
   `(1, 0)`? Nej → tilladt. `next_direction` bliver `(0, 1)`.
2. **Venstre** trykkes, med det samme: er `(-1, 0)` modsat af
   `direction`? `direction` er **stadig** `(1, 0)` (den er jo ikke rørt
   endnu) — og `(-1, 0)` *er* modsat af `(1, 0)` → **afvist**.
   `next_direction` forbliver `(0, 1)`.

Uanset hvor mange taster spilleren banker på mellem to skridt, er der kun
**én** stabil retning at sammenligne imod, indtil `move_snake()` selv
vælger at opdatere den. Det gør det umuligt at "snige" en 180-graders
vending igennem ved at gå via en mellemliggende retning.

*Bemærk:* Denne rettelse ændrer ikke noget ved, hvordan spillet opfører
sig, hvis man trykker taster i normalt tempo — det er præcis samme
spilfølelse som før. Det er kun den helt specifikke, hurtige
tast-kombination, der nu bliver håndteret korrekt.

### Trin 5 — Ryd HUD'et, inden vi tegner de nye point

Der gemmer sig en fejl i `draw_hud_img()` i `hud.py`, som vi ikke har
kunnet se endnu — fordi `score` altid har været `0`, har den tegnet
nøjagtig de samme cifre, på nøjagtig de samme pixels, 60 gange i
sekundet, uge efter uge. Så snart `score` rent faktisk ændrer sig (Opgave
1 nedenfor), bliver fejlen synlig.

Sådan ser `draw_hud_img()` ud lige nu:

```python
def draw_hud_img(screen, score):
    score = max(0, min(score, 999))
    text = f"SCORE {score:03d}"
    for idx, i in enumerate(text):
        if i == ' ':
            continue
        img = pygame.image.load(Path(font_img[i])).convert_alpha()
        img = pygame.transform.scale(img, FIXED_SIZE)
        screen.blit(img, ((idx + 1) * 20, 2))
```

`screen.blit()` **tegner oven på** det, der allerede er på skærmen — den
sletter ikke noget i forvejen. Hver gang `draw_hud_img()` kaldes, tegner
den de nye ciffer-billeder oven på de gamle, uden nogensinde selv at
rydde op først. Så længe cifrene var ens fra frame til frame, var det
usynligt — det nye billede dækkede simpelthen præcis det gamle, pixel for
pixel. Men i det øjeblik et ciffer skifter (fx fra `0` til `1`), passer de
to billeders "form" ikke længere sammen, og rester af det gamle ciffer
bliver stående synligt rundt om det nye — det er det, der ser "mudret" ud.

Løsningen er at **rydde** HUD-rækken, før vi tegner noget som helst nyt
derinde — akkurat som `draw_grass()` "rydder op" ved at tegne frisk græs
hen over hele spillepladen, hver eneste frame, før slangen og æblet
tegnes oven på det:

```python
def draw_hud_img(screen, score):
    score = max(0, min(score, 999))
    text = f"SCORE {score:03d}"

    hud_area = (0, 0, screen.get_width(), FIXED_SIZE[1])
    screen.fill((0, 0, 0), hud_area)  # ryd HUD-rækken, før vi tegner de nye cifre

    for idx, i in enumerate(text):
        if i == ' ':
            continue
        img = pygame.image.load(Path(font_img[i])).convert_alpha()
        img = pygame.transform.scale(img, FIXED_SIZE)
        screen.blit(img, ((idx + 1) * 20, 2))
```

`screen.fill(farve, omraade)` er den samme funktion, I allerede kender til
at farvelægge en hel overflade — men her giver vi den et ekstra, valgfrit
andet argument: et rektangel, `(x, y, bredde, højde)`, der fortæller
pygame, at den kun skal farvelægge **den del** af skærmen, ikke det hele.
`screen.get_width()` spørger selve skærm-overfladen, hvor bred den er, så
rektanglet altid dækker hele HUD-rækkens bredde, uanset hvor mange
kolonner brættet har. Højden, `FIXED_SIZE[1]`, er den samme højde, cifrene
selv tegnes med (`32` pixel) — nøjagtig HUD-rækkens højde, hverken mere
eller mindre.

*Bemærk:* farven `(0, 0, 0)` (sort) er kun et forslag — vælg selv en
farve, der passer til, hvordan I gerne vil have HUD-rækken til at se ud.

### `snake_game.py` (opdateret)

Vi skal bruge det, `move_snake()` nu returnerer:

```python
if event.type == SNAKE_MOVE:
    ate_apple = move_snake(GL.BOARD_COLUMNS, GL.BOARD_ROWS)
    if ate_apple:
        pass  # her skal I selv løse Opgave 1
```

`pass` er et python-nøgleord, der bogstaveligt talt ikke gør noget — det
bruges som en "pladsholder", når man syntaktisk skal skrive noget inde i et
`if`, men endnu ikke er klar til at skrive den rigtige kode. I skal
erstatte `pass` med jeres løsning på Opgave 1.

### Prøv selv

1. Opdatér `snake.py` og `snake_game.py` som vist ovenfor.
2. Kør spillet. Kør slangen hen over æblet — det skulle gerne springe til
   et nyt, tilfældigt sted.
3. Kør spillet et par gange, og se om I nogensinde oplever, at æblet dukker
   op **oven i** slangen. Hvorfor sker det ikke, med den kode vi har
   skrevet?
4. Prøv midlertidigt at fjerne `if (x, y) not in snake_body:`-tjekket i
   `place_apple()` (så den bare gemmer det første gæt) — kør spillet, og se
   om I kan få æblet til at dukke op inden i slangen.

---

## Opgaver

#### Opgave 1 — Slangen vokser, og point tælles op

Lige nu bliver slangen ikke længere, selv om `move_snake()` godt opdager,
at æblet er spist — og `score` i `snake_game.py` bliver aldrig ændret.
Ret det, så:

- Slangen får **ét ekstra segment**, hver gang den spiser et æble.
- `score` stiger med et passende antal point (fx `10`), hver gang der
  spises et æble.

*Tip 1:* Se på linjen `snake_body = [new_head] + snake_body[:-1]` i
`move_snake()`. `[:-1]` er det, der fjerner halen. Hvad ville der ske, hvis
I **ikke** fjernede halen, netop den gang slangen spiser et æble?

*Tip 2:* `score` er en variabel i `snake_game.py`, men den bliver ændret
inde i `if ate_apple:`-blokken, som I selv skrev i afsnittet ovenfor. Husk,
at hvis en funktion skal **ændre** en variabel, der er defineret uden for
funktionen, skal I bruge `global` — akkurat som `move_snake()` og
`change_direction()` gør med `snake_body` og `direction` i `snake.py`.

*Tip 3:* Husk også rettelsen af `draw_hud_img()` fra Trin 5 ovenfor — uden
den vil de nye, skiftende point stadig se mudrede ud på skærmen, selvom
selve optællingen er korrekt.

#### Opgave 2 — Æblet har en tidsfrist

For at gøre spillet sværere, skal æblet nu forsvinde af sig selv, hvis
slangen ikke når at spise det inden for **10 sekunder** efter, det er
dukket op.

*Tip 1:* Brug `pygame.time.get_ticks()` — den giver jer, hvor mange
millisekunder der er gået, siden pygame blev startet. Gem tidspunktet, hvor
æblet blev placeret, i en ny variabel, hver gang `place_apple()` kaldes.

*Tip 2:* Et sted i spillets hovedløkke (eller i en ny funktion, I selv
kalder derfra) skal I løbende sammenligne "nu" (`pygame.time.get_ticks()`)
med det gemte placerings-tidspunkt. Når forskellen bliver større end
`10 000` millisekunder (10 sekunder), er tiden udløbet.

*Tænk over:* Hvad skal der helt præcist ske, når tiden løber ud? Skal der
med det samme dukke et nyt æble op et andet sted (altså bare kalde
`place_apple()` igen)? Eller skal brættet stå helt uden æble et stykke tid,
så man som spiller virkelig mærker, at man "gik glip af" det? Der er ikke
ét rigtigt svar her — vælg selv, og vær klar til at forklare hvorfor, I
valgte som I gjorde.

---

## Kommende uger (planlagt)

- **Uge 4** — Kollision og "Game Over": slangen rammer væggen eller sig
  selv.
- **Uge 5** — Vi sætter nu et antal forhindringer op, når spillet starter. Disse forhindringer kan placeres på samme sted, hver gang. Eller de kan placeres tilfældigt (random)

*(Denne liste opdateres løbende, efterhånden som vi bliver enige om det
præcise indhold for hver uge.)*
