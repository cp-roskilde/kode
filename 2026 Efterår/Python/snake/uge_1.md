# Snake i Pygame

Vi bygger det klassiske spil **Snake** sammen, skridt for skridt, uge for uge.
Undervejs lærer vi ikke kun at lave et spil, men også hvordan man deler et
Python-projekt op i **flere filer**, og hvordan filerne taler sammen ved
hjælp af `import` og punktum-notation (`modul.funktion()`).

## Projektstruktur

I stedet for at have al kode i én stor fil, deler vi den op efter hvad koden
gør:

```
snake_projekt/
├── snake_game.py       <- selve spillet (hovedprogrammet)
└── hud.py              <- alt der har med "HUD'et" (point på skærmen) at gøre
```

`snake_game.py` er den fil vi rent faktisk kører. Den henter funktioner
fra `hud.py` med:

```python
from hud import draw_hud_text
```

Det betyder: "gå ind i filen `hud.py`, og hent funktionen `draw_hud_text`,
så vi kan bruge den herfra, som var den skrevet i vores egen fil."

Man kunne også have skrevet:

```python
import hud
...
hud.draw_hud_text(screen, score)
```

Her bruger vi **punktum-notation** (`hud.draw_hud_text`) i stedet for at
hente funktionen ud for sig selv. Begge måder virker — vi bruger den første
i vores kode, men det er godt at kende begge.

---

## Uge 1 — Spillebræt og HUD (tekst-udgave)

**Mål for ugen:**
- Forstå hvorfor vi deler kode i flere filer
- Lære at bruge `import` mellem egne filer
- Tegne spillepladen (græsset)
- Vise spillerens point øverst på skærmen med almindelig tekst

### `hud.py`

```python
import pygame
pygame.init()

font = pygame.font.SysFont("couriernew", 28)

def draw_hud_text(screen, score):
    score = max(0, min(score, 999))  # klem score til 0-999
    text = f" SCORE {score:03d}"      # nul-udfyld til 3 cifre, fx 0 -> "000", 42 -> "042"
    rendered = font.render(text, True, (255, 255, 255))
    screen.blit(rendered, (0, 0))
```

### `snake_game.py`

```python
import pygame
pygame.init()

from hud import draw_hud_text

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
    rect_color = pygame.Color("green3")
    for x in range(BOARD_COLUMNS):
        for y in range(1, BOARD_ROWS + 1):
            grass = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, rect_color, grass)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        # Luk spillet
        if event.type == pygame.QUIT:
            running = False

    draw_hud_text(screen, score)
    draw_grass()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

### Prøv selv

1. Opret de to filer i samme mappe.
2. Kør `snake_game.py`.
3. Prøv at ændre `score` til et andet tal — se hvordan HUD'et opdaterer sig.
4. Prøv at ændre `BOARD_ROWS` eller `BOARD_COLUMNS` — hvad sker der med
   vinduets størrelse?

### Opgaver

#### Opgave 1 — Skaktern-græs

Lige nu har alle græs-celler samme farve. Ændr `draw_grass()`, så cellerne
skifter mellem **to forskellige grønne nuancer** i et skaktern-mønster (som
et skakbræt) — altså sådan at nabo-celler (vandret og lodret) aldrig har
samme farve.

*Tip:* Du har allerede `x` og `y` for hver celle i løkken. Hvad kan du sige
om summen `x + y`, når du skifter mellem to farver hver anden celle?
Pygame har flere indbyggede grønne farvenavne, fx `"green3"` og `"green4"` —
prøv `pygame.Color("green4")` som den anden nuance.

#### Opgave 2 — HUD med billeder i stedet for tekst

Lige nu tegner `draw_hud_text` point med pygames egen skrifttype. I mappen
`Resources/font/Individual/` ligger der i stedet et lille billede for hvert
tegn (`0.png`, `1.png`, …, `Upper_S.png` for "S", osv.).

For at vide hvilket filnavn der hører til hvilket tegn, skal I bruge denne
dictionary. Indsæt den øverst i jeres `hud.py`, sammen med `draw_hud_text`:

```python
font_img = {
    '0': 'Resources/font/Individual/0.png',
    '1': 'Resources/font/Individual/1.png',
    '2': 'Resources/font/Individual/2.png',
    '3': 'Resources/font/Individual/3.png',
    '4': 'Resources/font/Individual/4.png',
    '5': 'Resources/font/Individual/5.png',
    '6': 'Resources/font/Individual/6.png',
    '7': 'Resources/font/Individual/7.png',
    '8': 'Resources/font/Individual/8.png',
    '9': 'Resources/font/Individual/9.png',
    'S': 'Resources/font/Individual/Upper_S.png',
    'C': 'Resources/font/Individual/Upper_C.png',
    'O': 'Resources/font/Individual/Upper_O.png',
    'R': 'Resources/font/Individual/Upper_R.png',
    'E': 'Resources/font/Individual/Upper_E.png',
    ':': 'Resources/font/Individual/_Colon.png',
}
```

Bemærk at nøglerne er de tegn, I kan møde i teksten `"SCORE 042"` (tallene,
bogstaverne S/C/O/R/E, og kolon) — men **ikke** mellemrum. Det skal I selv
tage stilling til, hvordan I håndterer.

Jeres opgave er at lave en ny funktion, der tegner HUD'et ved at slå hvert
tegn op i `font_img` og sætte billederne sammen ét tegn ad gangen, i stedet
for at bruge `font.render()`.

Tre pygame-værktøjer I får brug for:

- **`pygame.image.load(sti)`** — indlæser et billede fra disken og giver
  jer det som et *surface* (en flade, I kan tegne på skærmen). Ligesom
  `font.render()` giver jer et surface med tekst, giver `image.load` jer
  et surface med et billede.

  ```python
  img = pygame.image.load("Resources/font/Individual/5.png")
  ```

- **`pygame.transform.scale(surface, (bredde, højde))`** — ændrer
  størrelsen på et surface. Billederne har måske ikke den størrelse, I vil
  vise dem i — brug denne til at gøre dem alle lige store.

  ```python
  img = pygame.transform.scale(img, (20, 32))
  ```

- **`screen.blit(surface, (x, y))`** — "klistrer" et surface fast på
  `screen` ved position `(x, y)`. Det er den samme metode, I allerede
  bruger til at vise teksten fra `draw_hud_text`.

  ```python
  screen.blit(img, (0, 0))
  ```

*Tænk over:*
- Hvordan får I fat i det rigtige billede for hvert tegn i teksten
  `"SCORE 042"`? (Kig på hvordan `font_img`-dictionary'et er sat op.)
- Hvor langt til højre skal det næste tegn placeres, hvis hvert billede er
  20 pixels bredt?
- Skal I springe noget over, hvis tegnet er et mellemrum?

I skal ikke bruge `font.render()` i denne opgave — kun `image.load`,
`transform.scale` og `blit`.

---

## Kommende uger (planlagt)

De næste uger bygger vi videre oven på det, vi allerede har:

- **Uge 2** — Slangen: tegne den, styre den med piletaster, få den til at
  bevæge sig på gitteret.
- **Uge 3** — Mad og vækst: slangen bliver længere og point tælles op.
- **Uge 4** — Kollision og "Game Over": væg og sig selv.
- **Uge 5** — HUD fra sprite-sheet (`draw_hud_sheet`): samme idé som
  billed-HUD'et fra Opgave 2, men hurtigere, fordi alle tegn ligger i ét
  billede i stedet for mange små filer.

*(Denne liste opdateres løbende, efterhånden som vi bliver enige om det
præcise indhold for hver uge.)*
