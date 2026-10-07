# Snake i Pygame — Uge 5

Sidste uge lærte slangen at dø: rammer den muren eller sig selv, er det
Game Over, og med et tryk på mellemrum kan man prøve igen. Denne uge gør
vi banen mere interessant. Vi laver **åbninger** midt i alle fire mure,
så slangen kan smutte ud i den ene side og komme ind i den modsatte —
lige hen over banen, som på kryds og tværs. Og for at det ikke bliver
for nemt, sætter vi **5 forhindringer** ud på banen, lavet af samme
mursten som muren.

## Nyt mønster: én fil, der ved, hvor muren er

Lige nu findes "muren" faktisk to forskellige steder i koden, skrevet på
to forskellige måder:

- **Tegningen** af muren bor i `snake_game.py`, i `draw_wall()` — to løkker,
  der tegner venstre/højre side og top/bund.
- **Kollisionen** med muren bor i `snake.py`, i `move_snake()`:

```python
inside_board = 1 <= new_x <= cols - 2 and 2 <= new_y <= rows - 1
```

De to steder er nødt til at være enige om, hvor muren står. Det har de
været indtil nu, fordi muren var en simpel firkant. Men nu skal der huller
i muren, og der skal forhindringer ud på banen — og så skal I rette **begge**
steder, hver gang, og huske at rette dem ens. Glemmer I det ene sted, får
I en slange, der dør i et hul, der ser åbent ud, eller som glider lige
igennem en mursten, der står og ser solid ud.

Løsningen er at samle al viden om muren ét sted: en ny fil, `board.py`
("bræt" — selve spillepladen), med én funktion, der svarer på ét
spørgsmål: *er der mur på dette felt?*

```python
def is_wall(x, y):
    ...
```

Både tegningen og kollisionen spørger fremover `is_wall()`. Så kan de
aldrig blive uenige — der er jo kun ét svar.

Det er samme tankegang som `globals.py` fra uge 3 og tommelfingerreglen om,
at hver fil ejer sin egen tilstand: `snake.py` ejer slangen og æblet,
`hud.py` ejer scoren på skærmen, og nu ejer `board.py` selve banen.

### Trin 1 — Hvor store er hullerne?

Hullernes størrelse er en indstilling, ligesom `APPLE_TIMEOUT`, så den
hører hjemme i `globals.py`. Tilføj den nederst i `init()`, **på en ny
linje** efter den afsluttende `}` i `font_img`:

```python
	global GAP_SIZE  # Bredden af åbningerne i muren
	GAP_SIZE = 4
```

*Bemærk:* `globals.py` er indrykket med **tabulator**, ikke mellemrum. Brug
også tabulator her — Python bliver sur (`TabError`), hvis man blander de to
i samme funktion.

### Trin 2 — Hvor skal hullerne sidde?

Kig på, hvordan banen er bygget op (husk, at række 0 er HUD'en med
scoren):

- Top- og bundmuren ligger i række `y = 1` og `y = 16` og går fra
  `x = 0` til `x = 23` — det er 24 felter, altså `GL.BOARD_COLUMNS`.
- Venstre og højre mur ligger i kolonne `x = 0` og `x = 23` og går fra
  `y = 1` til `y = 16` — det er 16 felter, altså `GL.BOARD_ROWS`.

Et hul på 4 felter skal sidde midt på muren. Det er præcis samme regnestykke,
som I brugte til at centrere "GAME OVER" i uge 4: *(hele bredden − det, der
skal centreres) // 2*.

- Vandret: `(24 - 4) // 2 = 10`, så hullet i top og bund er kolonne
  10, 11, 12 og 13. Der er 10 felter mur på hver side.
- Lodret: `(16 - 4) // 2 = 6` — men muren starter i række 1, ikke række 0,
  så vi skal lægge 1 til: hullet i venstre og højre side er række 7, 8, 9
  og 10. Der er 6 felter mur over og under.

Fordi top og bund bruger **de samme** kolonner, sidder de to huller lige
over for hinanden — og det samme gælder venstre og højre. Det er vigtigt:
slangen skal jo kunne fortsætte lige ud, når den kommer ind på den anden
side.

### Trin 3 — `board.py`

Opret en ny fil, `board.py`, ved siden af de andre:

```python
import pygame
import globals as GL

wall_image = pygame.transform.scale(
    pygame.image.load("Resources/gfx/wall.png"),
    (GL.CELL_SIZE, GL.CELL_SIZE)
)

# Åbningerne i muren - centreret, og ens i hver side
gap_start_x = (GL.BOARD_COLUMNS - GL.GAP_SIZE) // 2           # 10
gap_columns = range(gap_start_x, gap_start_x + GL.GAP_SIZE)   # 10, 11, 12, 13

gap_start_y = 1 + (GL.BOARD_ROWS - GL.GAP_SIZE) // 2          # 7 (muren starter i række 1)
gap_rows = range(gap_start_y, gap_start_y + GL.GAP_SIZE)      # 7, 8, 9, 10

def is_wall(x, y):
    left_or_right = x == 0 or x == GL.BOARD_COLUMNS - 1
    top_or_bottom = y == 1 or y == GL.BOARD_ROWS

    if left_or_right and y not in gap_rows:
        return True
    if top_or_bottom and x not in gap_columns:
        return True
    return False

def draw_wall(screen):
    for x in range(GL.BOARD_COLUMNS):
        for y in range(1, GL.BOARD_ROWS + 1):
            if is_wall(x, y):
                screen.blit(wall_image, (x * GL.CELL_SIZE, y * GL.CELL_SIZE))
```

Læg mærke til, at `draw_wall()` ikke længere selv ved, hvordan muren ser
ud. Den går bare hen over **hvert eneste felt** på banen og spørger
`is_wall()`: "skal der en mursten her?". Ændrer I senere på, hvor muren er,
følger tegningen automatisk med.

`wall_image` og `draw_wall()` er flyttet hertil fra `snake_game.py`. Så i
`snake_game.py` skal I nu **slette** `wall_image = ...` og hele den gamle
`def draw_wall():`, og i stedet importere den nye:

```python
from board import draw_wall
```

Den nye `draw_wall()` skal have skærmen med, ligesom `draw_snake(screen)`
og `draw_apple(screen)`, så i hovedløkken bliver kaldet til:

```python
draw_wall(screen)
```

Start spillet: nu er der fire huller i muren, ét midt på hver side. Græsset
kan ses igennem dem, fordi `draw_grass()` allerede tegner græs under hele
muren.

### Trin 4 — Kollisionen skal også spørge `is_wall()`

Kør ind i et af hullerne. Slangen dør — for `move_snake()` bruger stadig
sin gamle firkant-regel, `inside_board`, som ikke kender noget til huller.
Det er præcis det problem, vi talte om øverst: to steder, der er uenige.

Øverst i `snake.py`, under `import globals as GL`:

```python
from board import is_wall
```

Og i `move_snake()` udskifter I hele `inside_board`-tjekket med:

```python
    if is_wall(new_x, new_y):
        game_over = True
        return False
```

Prøv igen: nu kan slangen køre ind i hullet... og videre ud af skærmen,
hvor den forsvinder for altid. Det er opgave 1.

---

## Uge 5 — Tunneller og forhindringer

**Mål for ugen:**
- Slangen, der kører ud gennem et hul, kommer ind igen gennem hullet på
  den modsatte side
- Slangen ser rigtig ud, også mens den er halvvejs gennem en tunnel
- Der står 5 forhindringer på banen, og slangen dør, hvis den rammer dem
- (Bonus) Forhindringerne står et nyt, tilfældigt sted hvert spil

### Opgave 1 — Ud på den ene side, ind på den anden

Når slangens nye hoved havner uden for banen, skal det flyttes over på den
modsatte side. Kører slangen ud til venstre (`x` bliver `-1`), skal den
komme ind yderst til højre (`x = 23`). Kører den ud foroven, skal den komme
ind forneden — og omvendt.

*Tip 1:* Rettelsen skal ske i `move_snake()`, lige efter I har regnet
`new_x` og `new_y` ud, og **før** tjekket med `is_wall()` og tjekket af, om
slangen rammer sig selv. Begge tjek skal jo se på det felt, hovedet
*faktisk* ender på. Husk også at lave `new_head` om bagefter, så den
passer med de nye værdier: `new_head = (new_x, new_y)`.

*Tip 2:* Den simpleste udgave er fire `if`-sætninger:

```python
    if new_x < 0:
        new_x = cols - 1
    ...
```

Skriv de tre andre selv. Pas på med de lodrette: banen går fra række `1`
til række `rows` (16), ikke fra `0` — række 0 er HUD'en, og den må slangen
aldrig komme ind i.

*Tænk over (for de nysgerrige):* Python har en operator, `%` ("modulo"),
som giver resten ved en division. `25 % 24` er `1`, `24 % 24` er `0`, og —
lidt overraskende — `-1 % 24` er `23`. Det betyder, at én linje kan klare
begge vandrette tilfælde på én gang:

```python
    new_x = new_x % cols
```

Prøv at regne efter med `new_x = -1`, `new_x = 5` og `new_x = 24`. Virker
samme trick lodret, med `new_y % rows`? (Hint: hvad sker der, når slangen
kører ud foroven og `new_y` bliver `0`? Og hvad med række 16?) Kan I
justere det, så det passer med, at banen starter i række 1?

*Tænk over:* Hvad sker der, hvis slangen er inde i hullet foroven (i række
1) og drejer til siden? Er det en fejl, at den dør efter et par felter —
eller er det sådan, det skal være?

Når opgave 1 virker, så kør ud gennem et hul. Spillet crasher med en
fejlbesked i stil med `KeyError: frozenset({None, 'left'})`. Det er
opgave 2.

### Opgave 2 — Slangen i to stykker

Selve bevægelsen er rigtig nu — det er **tegningen**, der går galt. Kig på
`edge_towards()` fra uge 2:

```python
def edge_towards(from_pos, to_pos):
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]
    if dx == 1:  return "right"
    if dx == -1: return "left"
    if dy == 1:  return "bottom"
    if dy == -1: return "top"
```

Funktionen går ud fra, at to naboled i slangen altid ligger lige ved siden
af hinanden, så forskellen er `1` eller `-1`. Men forestil jer slangen, der
lige er kørt ud til venstre: hovedet er på `x = 23`, og leddet bag det er
stadig på `x = 0`. Forskellen er `23`! Ingen af de fire `if`-sætninger
passer, funktionen returnerer `None`, og `corner_images` har ikke noget
billede for "hjørnet mellem `None` og venstre".

*Tænk over:* Når leddet på `x = 0` har sin nabo på `x = 23` — hvilken vej
ligger naboen så **reelt**, når man tænker på, at slangen er gået igennem
tunnelen? Til højre (den lange vej hen over skærmen) eller til venstre
(gennem hullet)?

*Tip 1:* Skriv en lille hjælpefunktion, der "retter" en forskel, som er
for stor, til den rigtige retning:

```python
def step(d):
    if d > 1:
        return -1
    if d < -1:
        return 1
    return d
```

En forskel på `23` bliver til `-1`, en forskel på `-23` bliver til `1`, og
almindelige forskelle (`-1`, `0`, `1`) får lov at være i fred. Brug den på
`dx` og `dy` i `edge_towards()`.

*Tip 2:* Der er ét sted mere i `draw_snake()`, hvor der regnes en forskel
ud mellem to led. Find det — ellers crasher spillet igen, når **halen** når
frem til tunnelen.

*Tip 3:* Hovedet skal ikke rettes. Det tegnes ud fra `direction`, og den er
altid en af de fire rigtige retninger.

### Opgave 3 — 5 forhindringer

Nu kommer gevinsten ved `is_wall()`. Læg en liste med 5 forhindringer i
`board.py`, under `gap_rows`:

```python
obstacles = [(4, 4), (19, 4), (4, 13), (19, 13), (16, 5)]
```

Hvert punkt er et felt `(x, y)` på banen, hvor der skal stå en mursten. I
må gerne vælge jeres egne pladser — men læs reglerne nedenfor først.

*Tip 1:* Udvid `is_wall()`, så den **også** svarer `True`, hvis `(x, y)`
er i listen `obstacles`. Brug `in`, ligesom I gjorde med `snake_body` i
uge 4.

*Tænk over:* Hvor mange andre steder i koden skal I rette, for at
forhindringerne bliver **tegnet**? Og for at slangen **dør**, når den
rammer dem? Prøv at starte spillet og se efter — inden I begynder at rette
noget.

*Tip 2:* Der er dog ét sted, der ikke spørger `is_wall()` endnu:
`place_apple()`. Lige nu kan et æble godt lande oven i en forhindring, og
så kan slangen aldrig spise det. Udvid tjekket
`if (x, y) not in snake_body:`, så æblet heller ikke må ligge på et felt,
hvor der er mur.

*Regler for gode pladser:*
- Felterne skal ligge **inde** på banen: `x` fra 1 til 22, `y` fra 2 til 15.
- Undgå de to "tunnel-baner" på kryds hen over banen — kolonne 10–13 og
  række 7–10. Ellers kan en forhindring stå lige foran et hul, så man dør
  i samme øjeblik, man kommer ud af tunnelen.
- Slangen starter på række 8 og kører mod højre. En forhindring dér ville
  dræbe spilleren, før man overhovedet har nået at reagere. (Overholder I
  reglen ovenfor, er I allerede dækket ind — række 8 er jo en tunnel-bane.)

### Opgave 4 (bonus) — Nye forhindringer hvert spil

Faste forhindringer er nemme at lære udenad. Gør det sådan, at der kommer 5
nye, tilfældige forhindringer, hver gang et nyt spil starter.

*Tip 1:* Skriv en funktion i `board.py`, fx `place_obstacles(snake_body)`,
der tømmer `obstacles` og fylder den op igen med 5 tilfældige felter. Den
kan bygges næsten som `place_apple()`: en løkke med `random.randint()`,
der bliver ved, indtil der er fundet nok gode felter. Husk `import random`
og `global obstacles` i funktionen.

*Tip 2:* Et felt er kun "godt", hvis det overholder reglerne fra opgave 3,
**og** hvis det ikke allerede står en forhindring der. `x in gap_columns`
og `y in gap_rows` fortæller jer, om feltet ligger i en tunnel-bane.

*Tip 3:* Hvorfra skal `place_obstacles()` kaldes? Den skal kaldes, hver
gang spillet nulstilles — altså fra `reset()` i `snake.py`. Tænk grundigt
over **rækkefølgen** inde i `reset()`:
- Forhindringerne må ikke lande oven på slangen — så hvad skal være
  sat op, *før* I placerer dem?
- Æblet må ikke lande oven på en forhindring — så hvad skal være sat op,
  *før* I placerer æblet?

*Tænk over:* Hvorfor er det helt i orden, at `snake.py` kalder
`place_obstacles()` — hænger det sammen med tommelfingerreglen om, at hver
fil kun nulstiller sin egen tilstand? (Hvem ændrer egentlig på listen
`obstacles` — `snake.py` eller `board.py`?)

*Tænk over:* `snake.py` importerer `is_wall` — en funktion — og ikke
`obstacles` direkte. Husk "Tænk over" fra uge 4 om `is_game_over()`: hvad
ville der ske med en importeret `obstacles`-liste, når `place_obstacles()`
laver en helt ny liste i `board.py`?

---

## Kommende uger (planlagt)

*(Indholdet af de næste uger er endnu ikke fastlagt. Listen opdateres
løbende, efterhånden som vi bliver enige om det præcise indhold for hver
uge.)*
