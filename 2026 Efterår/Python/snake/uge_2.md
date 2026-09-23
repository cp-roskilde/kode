# Snake i Pygame — Uge 2

Sidste uge byggede vi spillepladen og en tekst-HUD. Denne uge starter vi med
at give brættet en fysisk kant — en **mur** — og bygger derefter videre til
det store skridt: **slangen** kommer på skærmen, vi kan style den med
piletasterne, og den bevæger sig selv, hele tiden, hen over gitteret.

## Muren: en fysisk grænse omkring brættet

Lige nu er græsset bare et rektangel, der stopper, uden nogen tydelig kant.
Vi tilføjer en **mur**, tegnet af en ny sprite, `wall.png`, rundt om hele
spillepladen — dels fordi det ser bedre ud, dels fordi det bliver den
grænse, slangen faktisk skal støde ind i, når vi bygger rigtig kollision i
uge 4.

*Antagelse:* Vi går ud fra, at `wall.png` — ligesom de andre grafik-filer —
ligger i `Resources/gfx/`, og er en almindelig, ikke-transparent flise i
samme stil som de øvrige billeder. Er den ikke `40 × 40` pixel, skal I bare
justere skaleringen, som I allerede kender fra sidste uges Opgave 2.

**Sådan tegner vi muren**

Vi tilføjer dette til `snake_game.py`, lige under `draw_grass()`:

```python
wall_image = pygame.transform.scale(
    pygame.image.load("Resources/gfx/wall.png"),
    (CELL_SIZE, CELL_SIZE)
)

def draw_wall():
    # Venstre og højre mur
    for y in range(1, BOARD_ROWS + 1):
        screen.blit(wall_image, (0, y * CELL_SIZE))
        screen.blit(wall_image, ((BOARD_COLUMNS - 1) * CELL_SIZE, y * CELL_SIZE))

    # Top og bund
    for x in range(BOARD_COLUMNS):
        screen.blit(wall_image, (x * CELL_SIZE, 1 * CELL_SIZE))
        screen.blit(wall_image, (x * CELL_SIZE, BOARD_ROWS * CELL_SIZE))
```

`draw_wall()` tegner mur-fliser hele vejen rundt om kanten af det bræt, vi
allerede har: kolonne `0` og kolonne `BOARD_COLUMNS - 1` (venstre/højre),
samt række `1` og række `BOARD_ROWS` (top/bund — husk at række `0` er
HUD'ets række, så spillepladen starter ved række `1`). Vi kalder
`draw_wall()` **efter** `draw_grass()`, så mur-fliserne tegnes oven på
græsset i stedet for at blande sig med det:

```python
draw_hud_text(screen, score)
draw_grass()
draw_wall()
```

*Bemærk:* Muren "spiser" af det bræt, vi allerede havde — de yderste
rækker og kolonner er nu mur i stedet for spilleplads. Det betyder, at det
**rigtige** spilleområde for slangen bliver en tand mindre, end det var.
Det retter vi i Trin 6 nedenfor, når vi opdaterer `move_snake()`.

---

## Nyt begreb: retning som et par tal

Vi har brug for en måde at beskrive "hvilken vej" på. I stedet for at skrive
"op", "ned", "venstre" og "højre" som tekst, bruger vi et lille par af tal —
en **vektor** — der fortæller, hvor meget vi skal flytte os i **x** og
**y** for hvert skridt:

| Retning  | Vektor   | Betyder                          |
|----------|----------|-----------------------------------|
| Højre    | `(1, 0)` | +1 i x, 0 i y                     |
| Venstre  | `(-1, 0)`| -1 i x, 0 i y                     |
| Ned      | `(0, 1)` | 0 i x, +1 i y (ned er **plus** y!)|
| Op       | `(0, -1)`| 0 i x, -1 i y                     |

Det er værd at bide mærke i, at "ned" er `+1` og ikke `-1` — det er fordi
skærm-koordinater i pygame starter i **øverste venstre hjørne** (0, 0), og
y-værdien vokser nedad. Det er modsat af, hvad man normalt tegner grafer med
i matematik, så det snyder de fleste i starten.

---

## Slangen: grafik, styring og bevægelse

**Mål for ugen:**
- Repræsentere slangen som en liste af gitter-positioner (koordinater)
- Indlæse billeder for hoved, krop og hale, og vise det rigtige billede alt
  efter hvilken vej slangen vender
- Styre slangens retning med piletasterne
- Få slangen til at bevæge sig på gitteret — i sit eget tempo, uafhængigt af
  hvor mange billeder i sekundet spillet tegner

### Projektstruktur (opdateret)

Vi tilføjer en ny fil, `snake.py`, som holder styr på alt, hvad der har med
slangen at gøre — akkurat som `hud.py` holder styr på HUD'et:

```
snake_projekt/
├── snake_game.py       <- selve spillet (hovedprogrammet)
├── hud.py              <- alt der har med HUD'et at gøre
├── snake.py             <- alt der har med slangen at gøre (NY)
└── Resources/
    └── gfx/             <- billederne til slangen, æblet og muren
```

### Grafikken (`Resources/gfx/`)

I skal bruge disse filer, som allerede ligger klar:

| Fil                       | Bruges til                                          |
|----------------------------|------------------------------------------------------|
| `head_up.png` / `head_down.png` / `head_left.png` / `head_right.png` | Hovedet, alt efter hvilken vej slangen bevæger sig |
| `body_horizontal.png`      | En krop-del på en lige, vandret strækning              |
| `body_vertical.png`        | En krop-del på en lige, lodret strækning               |
| `body_topleft.png` / `body_topright.png` / `body_bottomleft.png` / `body_bottomright.png` | En krop-del, hvor slangen **drejer** (bonus-opgave)   |
| `tail_up.png` / `tail_down.png` / `tail_left.png` / `tail_right.png` | Halespidsen, alt efter hvilken vej den "peger"     |
| `apple.png`                | Æblet (bruges i denne uges bonus-opgave, og for alvor i uge 3) |
| `wall.png`                 | Muren omkring brættet (se afsnittet ovenfor) |

Alle billederne er `40 × 40` pixel, men vores gitter bruger `CELL_SIZE = 32`
(fra sidste uge). Derfor skal vi **skalere** hvert billede ned, når vi
indlæser det, med `pygame.transform.scale()` — akkurat som I gjorde med
tal-billederne i sidste uges Opgave 2.

### `snake.py`

**Trin 1 — Indlæs billederne**

Vi laver tre "opslagsbøger" (dictionaries): én for hovedet, én for halen, og
én for de lige krop-stykker. Nøglen er retnings-vektoren, og værdien er det
færdig-indlæste og skalerede billede:

```python
import pygame

CELL_SIZE = 32
GFX = "Resources/gfx/"

def load(filnavn):
    billede = pygame.image.load(GFX + filnavn)
    return pygame.transform.scale(billede, (CELL_SIZE, CELL_SIZE))

head_images = {
    (1, 0):  load("head_right.png"),
    (-1, 0): load("head_left.png"),
    (0, 1):  load("head_down.png"),
    (0, -1): load("head_up.png"),
}

tail_images = {
    (1, 0):  load("tail_right.png"),
    (-1, 0): load("tail_left.png"),
    (0, 1):  load("tail_down.png"),
    (0, -1): load("tail_up.png"),
}

body_images = {
    "horizontal": load("body_horizontal.png"),
    "vertical":   load("body_vertical.png"),
}
```

Vi har lavet vores egen lille funktion, `load()`, i stedet for at skrive
`pygame.image.load(...)` og `pygame.transform.scale(...)` otte gange i
træk. Det er samme idé som at dele kode op i filer: vi undgår at gentage os
selv.

**Trin 2 — Slangens data**

Slangen er bare en **liste af positioner** på gitteret — én position pr.
segment af kroppen. Hovedet er altid **først** i listen (index 0):

```python
snake_body = [(12, 8), (11, 8), (10, 8)]
direction = (1, 0)   # slangen starter med at bevæge sig mod højre
```

Her har slangen 3 segmenter: hovedet står på kolonne 12, række 8, og de to
resterende krop-stykker ligger til venstre for det — fordi slangen bevæger
sig mod højre.

**Trin 3 — Skift retning**

```python
def change_direction(new_direction):
    global direction
    opposite = (-direction[0], -direction[1])
    if new_direction != opposite:
        direction = new_direction
```

Vi tjekker, at den nye retning ikke er den **modsatte** af den, vi allerede
bevæger os i — ellers ville slangen kunne vende 180 grader og køre lige ind
i sig selv med det samme. `opposite` regner vi ud ved at gange begge tal i
`direction` med `-1`.

**Trin 4 — Flyt slangen**

```python
def move_snake():
    global snake_body
    head_x, head_y = snake_body[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    snake_body = [new_head] + snake_body[:-1]
```

Ideen bag at "bevæge" en slange er smart, men simpel: vi regner ud, hvor det
**nye hoved** skal stå (den gamle hoved-position plus retningen), og
sætter det forrest i listen. Samtidig fjerner vi det **sidste** element i
listen med `[:-1]` (alt undtagen det sidste). Resultatet er, at hele
slangen rykker ét skridt frem — uden at blive længere. (Uge 3 handler om,
hvordan vi springer over at fjerne halen, når slangen har spist et æble.)

**Trin 5 — Tegn slangen**

```python
def draw_snake(screen):
    for index, segment in enumerate(snake_body):
        x, y = segment
        pixel_pos = (x * CELL_SIZE, y * CELL_SIZE)

        if index == 0:
            screen.blit(head_images[direction], pixel_pos)

        elif index == len(snake_body) - 1:
            prev_x, prev_y = snake_body[index - 1]
            tail_direction = (x - prev_x, y - prev_y)
            screen.blit(tail_images[tail_direction], pixel_pos)

        else:
            prev_x, prev_y = snake_body[index - 1]
            if prev_y == y:
                screen.blit(body_images["horizontal"], pixel_pos)
            else:
                screen.blit(body_images["vertical"], pixel_pos)
```

Vi løber igennem `snake_body` med `enumerate()`, som giver os både
**indexet** (0, 1, 2, …) og selve segmentet i samme ombæring. Det bruger vi
til at afgøre, hvilket billede der skal tegnes:
- **Index 0** er altid hovedet → vi slår op i `head_images` med den retning,
  slangen bevæger sig i lige nu.
- **Det sidste index** er halen → vi kigger på segmentet *foran* halen (tættere
  på hovedet) og regner ud, hvilken vej halen "peger" væk fra kroppen.
- **Alt midt imellem** er almindelig krop → vi kigger på, om nabo-segmentet har
  samme række (`prev_y == y`) — i så fald er stykket vandret, ellers lodret.

*Bemærk:* Så længe slangen kører i en lige linje, ser det helt rigtigt ud.
Men i et sving (hvor slangen drejer) vil krop-stykket i hjørnet stadig blive
tegnet som "lige" — det er præcis det, Opgave 1 nedenfor retter.

**Trin 6 — Bliv inden for muren**

Lige nu kan slangen bare fortsætte lige ind i muren — eller ud af vinduet —
hvis man styrer den ud over kanten. Det retter vi ved at tjekke, om det
**nye hoved** stadig er inden for det spilbare område, *før* vi rykker
slangen. `snake.py` skal først kende brættets størrelse — akkurat som
`CELL_SIZE`, gentager vi tallene her:

```python
BOARD_COLUMNS = 24
BOARD_ROWS = 16
```

Og så udvider vi `move_snake()` fra Trin 4:

```python
def move_snake():
    global snake_body
    head_x, head_y = snake_body[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    new_x, new_y = new_head

    inside_board = 1 <= new_x <= BOARD_COLUMNS - 2 and 2 <= new_y <= BOARD_ROWS - 1
    if not inside_board:
        return  # ramte muren - lad slangen stå stille i stedet

    snake_body = [new_head] + snake_body[:-1]
```

- `1 <= new_x <= BOARD_COLUMNS - 2` holder slangen væk fra venstre mur
  (kolonne `0`) og højre mur (kolonne `BOARD_COLUMNS - 1`).
- `2 <= new_y <= BOARD_ROWS - 1` holder slangen væk fra top-muren (række
  `1`) og bund-muren (række `BOARD_ROWS`). Tallene er en tand strammere
  end sidst, netop fordi den yderste ring nu er mur og ikke spilleplads.
- Vi `return`'er *før* vi rører `snake_body`, så listen ikke ændrer sig —
  slangen "banker imod muren" og bliver stående, indtil man styrer den en
  anden vej.

*Bemærk:* Det er bevidst en midlertidig løsning. Den bruger murens
**position** til at vide, hvor grænsen går — men det er stadig kun et
tal-tjek, ikke en rigtig kollision med selve slangens **egen krop**. Den
tester vi i uge 4.

### `snake_game.py` (opdateret)

```python
import pygame
pygame.init()

from hud import draw_hud_img
from snake import draw_snake, move_snake, change_direction

GAME_BOARD = []
CELL_SIZE = 32
BOARD_ROWS = 16
BOARD_COLUMNS = 24

WIDTH = BOARD_COLUMNS * CELL_SIZE
HEIGHT = BOARD_ROWS * CELL_SIZE

score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT + CELL_SIZE))
pygame.display.set_caption("Snake")

def draw_grass():
    for x in range(BOARD_COLUMNS):
        for y in range(1, BOARD_ROWS + 1):
            # Vi tegner nu græsset. For at give det mere liv, skifter vi farve, for hver celle.
            if (x + y) % 2 == 0:
                rect_color = pygame.Color("green3")
            else:
                rect_color = pygame.Color("lawngreen")
            grass = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, rect_color, grass)

wall_image = pygame.transform.scale(
    pygame.image.load("Resources/gfx/wall.png"),
    (CELL_SIZE, CELL_SIZE)
)

def draw_wall():
    for y in range(1, BOARD_ROWS + 1):
        screen.blit(wall_image, (0, y * CELL_SIZE))
        screen.blit(wall_image, ((BOARD_COLUMNS - 1) * CELL_SIZE, y * CELL_SIZE))

    for x in range(BOARD_COLUMNS):
        screen.blit(wall_image, (x * CELL_SIZE, 1 * CELL_SIZE))
        screen.blit(wall_image, (x * CELL_SIZE, BOARD_ROWS * CELL_SIZE))

# Lav en helt ny slags "begivenhed" (event), som kun vi selv bruger
SNAKE_MOVE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_MOVE, 150)  # send begivenheden hvert 150. millisekund

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SNAKE_MOVE:
            move_snake()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                change_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                change_direction((1, 0))

    draw_hud_img(screen, score)
    draw_grass()
    draw_wall()
    draw_snake(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

Det vigtigste nye i denne fil er `SNAKE_MOVE`, og det er værd at forstå
**hvorfor** vi laver det på den måde:

Vores spil tegner skærmen 60 gange i sekundet (`clock.tick(60)`), fordi det
skal se jævnt og flydende ud. Men hvis slangen flyttede sig ét gitter-felt
**hver eneste** af de 60 gange, ville den flyve hen over skærmen så hurtigt,
at man ikke kunne se noget. Vi vil have, at *tegningen* kører hurtigt, men
at *slangens bevægelse* kører langsommere og i faste skridt.

Løsningen er at bede pygame om at sende en **speciel besked** ind i
event-køen med jævne mellemrum:

- `pygame.USEREVENT` er et tal, pygame har reserveret til, at vi selv kan
  opfinde vores egne begivenheder. Vi gemmer det i variablen `SNAKE_MOVE`,
  så koden er til at læse.
- `pygame.time.set_timer(SNAKE_MOVE, 150)` betyder: "hvert 150. millisekund,
  put en `SNAKE_MOVE`-begivenhed ind i event-køen" — den samme kø, som
  `pygame.QUIT` og tastetryk allerede lander i.
- I `for event in pygame.event.get():`-løkken behandler vi den nøjagtigt
  som alle andre begivenheder: `if event.type == SNAKE_MOVE: move_snake()`.

På den måde kører tegning og bevægelse **hver sit tempo**, uden at vi
behøver at tælle billeder eller bruge `if`-sætninger med tællere.

Til sidst tilføjer vi tastetryk: `pygame.KEYDOWN` er selve begivenheden
"en tast blev trykket ned", og `event.key` fortæller **hvilken** tast. Vi
sammenligner med pygames indbyggede konstanter (`pygame.K_UP` osv.) og
kalder `change_direction()` med den tilsvarende retnings-vektor.

### Prøv selv

1. Opret `snake.py`, og opdatér `snake_game.py` som vist ovenfor.
2. Sørg for, at `Resources/gfx/`-mappen med billederne ligger, hvor koden
   forventer den.
3. Kør spillet. Styr slangen med piletasterne.
4. Prøv at ændre tallet `150` i `pygame.time.set_timer(SNAKE_MOVE, 150)` —
   hvad sker der, hvis det er `50`? Hvad med `400`?
5. Prøv at fjerne `if new_direction != opposite:`-tjekket i
   `change_direction()` — og se (forsigtigt!) hvad der sker, hvis man vender
   180 grader.

### Opgaver

#### Opgave 1 — Runde hjørner

Lige nu bruger `draw_snake()` kun `body_horizontal.png` og
`body_vertical.png`. Det ser forkert ud i et sving. Brug i stedet de fire
hjørne-billeder (`body_topleft.png`, `body_topright.png`,
`body_bottomleft.png`, `body_bottomright.png`), så et sving ser rundt og
rigtigt ud.

*Tip:* For et krop-segment, der hverken er hoved eller hale, skal I kigge på
**to** naboer: segmentet før det (tættere på hovedet) og segmentet efter
det (tættere på halen). Sammen fortæller de to retninger jer, om slangen
går lige igennem feltet, eller om den drejer — og i så fald, hvilken af de
fire hjørne-billeder der passer. Tegn det op på papir med pile, hvis det er
svært at se for jer i koden.

**Hints**

Er I kørt fast, så prøv jer frem i denne rækkefølge:

**Hint 1 — Hent begge naboer**

I har allerede `prev_x, prev_y = snake_body[index - 1]` fra den nuværende
kode. I skal bruge *samme* trick én gang til, for naboen på den anden side:

```python
prev_pos = snake_body[index - 1]   # nærmere hovedet
next_pos = snake_body[index + 1]   # nærmere halen
```

**Hint 2 — Lav en funktion, der finder "hvilken kant"**

I stedet for at skrive den samme sammenligning af x'er og y'er hver gang,
er det en god idé at samle den logik ét sted, i en lille funktion. Giv den
to positioner, og lad den svare med `"top"`, `"bottom"`, `"left"` eller
`"right"` — altså: hvilken kant af feltet ligger `to_pos` ved, set fra
`from_pos`?

```python
def edge_towards(from_pos, to_pos):
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]
    if dx == 1:
        return "right"
    if dx == -1:
        return "left"
    if dy == 1:
        return "bottom"
    if dy == -1:
        return "top"
```

Kald den to gange pr. segment — én gang med `prev_pos`, én gang med
`next_pos` — så får I to kant-navne, fx `"bottom"` og `"left"`. De to
tilsammen fortæller *præcis*, hvilket af de fire hjørne-billeder der passer.

**Hint 3 — Hvorfor `frozenset`?**

Et almindeligt Python-`set` (og dets "frosne", uforanderlige udgave,
`frozenset`) er en samling, hvor **rækkefølgen ikke betyder noget** — kun
hvad der er i den:

```python
>>> frozenset({"bottom", "left"}) == frozenset({"left", "bottom"})
True
```

Det er lige præcis, hvad I har brug for: det er ligegyldigt, om det var
`prev_pos`, der lå mod bunden, eller om det var `next_pos` — resultatet
`{"bottom", "left"}` skal give det samme hjørne uanset hvad. Med et
almindeligt par, `("bottom", "left")`, ville I skulle tjekke **begge**
rækkefølger selv; med `frozenset` løser Python det for jer. Og fordi en
`frozenset` (modsat et almindeligt `set`) ikke kan ændres, må den gerne
bruges som nøgle i en dictionary — det kan et almindeligt `set` ikke.

Byg jeres opslagsbog med `frozenset` som nøgler:

```python
corner_images = {
    frozenset({"top", "left"}):     load("body_topleft.png"),
    frozenset({"top", "right"}):    load("body_topright.png"),
    frozenset({"bottom", "left"}):  load("body_bottomleft.png"),
    frozenset({"bottom", "right"}): load("body_bottomright.png"),
}
```

**Hint 4 — Sæt det sammen i `draw_snake()`**

Nu har I byggeklodserne. I `else`-grenen (det midterste segment), find
begge kanter, og saml dem i ét `set`:

```python
edge_to_prev = edge_towards(segment, prev_pos)
edge_to_next = edge_towards(segment, next_pos)
edges = {edge_to_prev, edge_to_next}
```

Herfra er der tre muligheder — prøv selv at skrive `if`/`elif`/`else` for
dem, før I kigger på facit:
- `edges` er `{"left", "right"}` → lige, vandret stykke
- `edges` er `{"top", "bottom"}` → lige, lodret stykke
- ellers → det er et hjørne, og `frozenset(edges)` er nøglen ind i
  `corner_images`

<details>
<summary>Facit for else-grenen (kig kun her, hvis I har prøvet selv)</summary>

```python
if edges == {"left", "right"}:
    screen.blit(body_images["horizontal"], pixel_pos)
elif edges == {"top", "bottom"}:
    screen.blit(body_images["vertical"], pixel_pos)
else:
    screen.blit(corner_images[frozenset(edges)], pixel_pos)
```

</details>

#### Opgave 2 — Tegn æblet

I `Resources/gfx/` ligger `apple.png`. Lav en lille funktion
`draw_apple(screen)` i `snake.py`, der bruger `load()` til at indlæse
billedet én gang, og som tegner det på et **fast** gitter-felt, fx `(18, 4)`.
Kald funktionen fra `snake_game.py`, ligesom `draw_snake(screen)`.

Slangen skal **ikke** spise æblet eller vokse endnu — det er hele emnet for
uge 3. Denne opgave handler kun om at få billedet på skærmen på det rigtige
sted.

#### Opgave 3 — Sværhedsgrad

Få slangen til at blive hurtigere, jo længere spillet varer — fx ved at
kalde `pygame.time.set_timer(SNAKE_MOVE, nyt_tal)` igen inde i løkken, med
et lavere tal end 150, efter et vist antal sekunder er gået (brug
`pygame.time.get_ticks()` til at måle, hvor lang tid spillet har kørt).

---

## Kommende uger (planlagt)

- **Uge 3** — Mad og vækst: slangen spiser det æble, vi tegnede i Opgave 2,
  bliver længere, og point tælles op.
- **Uge 4** — Kollision og "Game Over": væg og sig selv.
- **Uge 5** — HUD fra sprite-sheet (`draw_hud_sheet`): samme idé som
  billed-HUD'et fra uge 1's Opgave 2, men hurtigere, fordi alle tegn ligger i
  ét billede i stedet for mange små filer.

*(Denne liste opdateres løbende, efterhånden som vi bliver enige om det
præcise indhold for hver uge.)*
