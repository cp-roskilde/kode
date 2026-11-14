# Snake i Pygame — Uge 7

Snake er færdigt. Man kan selv spille, eller man kan se AI'en spille. Men
prøv det her: spil et rigtig godt spil, luk vinduet, og start spillet igen.
Hvor blev jeres flotte score af? Den er væk. Alt, hvad spillet ved, ligger i
variabler, og variabler forsvinder, når programmet slutter.

I denne uge laver vi en **highscore-liste** i gammeldags arkadestil: de 10
bedste spil med initialer, score og dato, gemt i en fil, så listen stadig er
der i morgen.

*Udgangspunkt:* I bygger videre på jeres egen kode fra bonusugen. Har I ikke
været her, eller virker jeres kode ikke, så start fra `kode_uge_6_bonus`.

## Nyt begreb: En liste med ordbøger

Hver linje på highscore-listen har tre ting: et navn, en score og en dato.
En ordbog (`dict`) er perfekt til én linje. I kender ordbøger fra
***font_img*** i `globals.py`, hvor et tegn peger på et filnavn:

```python
entry = {"name": "BOS", "score": 120, "date": "11-11-2026"}
```

Nu kan vi skrive `entry["score"]` og få `120`. Hele listen er så bare en
liste med 10 af den slags ordbøger, hvor nummer 1 står først:

```python
highscores = [
    {"name": "BOS", "score": 120, "date": "11-11-2026"},
    {"name": "ANN", "score": 90,  "date": "04-11-2026"},
]
```

`highscores[0]` er den bedste, og `highscores[-1]` er den sidste på listen.
Det er præcis samme `-1`-trick, som I brugte i `snake_body[:-1]`.

## Nyt begreb: json

En liste i Python forsvinder, når programmet lukkes. Derfor gemmer vi den i
en fil. **json** er en måde at skrive lister og ordbøger ned som tekst, så
Python kan læse dem igen næste gang. I har allerede set det i bonusugen, hvor
AI'ens hjerne blev gemt i `q_table.json`.

- `json.dump(highscores, f)` skriver listen ned i filen ***f***.
- `json.load(f)` læser den op igen og giver os listen tilbage.

## Nyt begreb: None

Når man skriver sine initialer, skal spillet vide, *hvilken* linje man
skriver i. Det gemmer vi som et tal, fx `3` for fjerde linje. Men hvad når
man ikke skriver i nogen linje? Så bruger vi **None**, som er Pythons måde at
sige "ingenting" på. `None` er ikke det samme som `0`, for `0` er jo en
rigtig linje, nemlig den øverste.

```python
edit_row = None        # vi skriver ikke i nogen linje
edit_row = 0           # vi skriver i den øverste linje
edit_row is not None   # True, hvis vi er i gang med at skrive
```

---

## Uge 7 — Highscore

**Mål for ugen:**
- Highscore-listen bliver gemt i `highscore.json` og hentet igen, når spillet starter.
- Kommer man på listen, bliver ens score sat ind på den rigtige plads.
- Man skriver sine 3 initialer direkte på highscore-skærmen, og Enter låser linjen.
- Kun spillere kan komme på listen, ikke AI'en.

### Projektstruktur (opdateret)

```
snake/
├── snake_game.py
├── snake.py
├── board.py
├── hud.py
├── globals.py
├── highscore.py      <- NY: ejer highscore-listen
├── highscore.json    <- NY: laves automatisk første gang, nogen kommer på listen
├── ai.py
├── ai_train.py
├── q_table.json
└── Resources/
```

Husk tommelfingerreglen fra uge 3: **data, der ændrer sig, og som styres ét
sted, bliver i den fil, der styrer det.** Highscore-listen får derfor sin egen
fil, `highscore.py`, og kun den fil må ændre i listen. Alle andre filer
spørger den om lov.

### Trin 1 — Et nyt tegn i fonten

Datoer skrives som `11-11-2026`, og de tomme pladser i initialerne vises som
`-`. Men vores bitmap-font kender ikke tegnet `-` endnu. Billedet findes
allerede i `Resources/font/Individual/`. Det står bare ikke i ***font_img***.

Tilføj én linje i `globals.py`, lige under punktum:

```python
		'.': 'Resources/font/Individual/_Period.png',
		'-': 'Resources/font/Individual/_Hyphen.png',  # Uge 7 - til datoer og initialer
		}
```

*Bemærk:* Prøver man at skrive et tegn, der ikke står i ***font_img***, går
spillet ned med en `KeyError`. Det er derfor, vi tilføjer tegnet først.

### Trin 2 — `highscore.py`

Lav en ny fil, `highscore.py`. Vi bygger den i små bidder.

**Øverst: konstanter og tilstand**

```python
import json
from pathlib import Path
from datetime import date

HIGHSCORE_FILE = "highscore.json"
MAX_ENTRIES = 10                              # vi viser 10 pladser, ligesom på en arkademaskine
ALLOWED_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

highscores = []    # liste med én ordbog pr. plads: {"name": ..., "score": ..., "date": ...}
edit_row = None    # den række, der skrives navn i lige nu (None = ingen)
```

- ***HIGHSCORE_FILE*** er navnet på filen, ligesom ***BRAIN_FILE*** i `ai.py`.
- ***ALLOWED_LETTERS*** er de bogstaver, man må bruge i sine initialer. Vi
  skriver dem selv, så æ, ø og å ikke kommer med. Dem har fonten ikke.
- `datetime` er en del af Python og kan fortælle os dagens dato.

**Hent og gem**

```python
def load_highscores():
    global highscores
    if Path(HIGHSCORE_FILE).exists():
        with open(HIGHSCORE_FILE) as f:
            highscores = json.load(f)

def save_highscores():
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(highscores, f, indent=2)
```

Første gang spillet startes, findes filen ikke. Uden
`Path(HIGHSCORE_FILE).exists()` ville **open()** så give en fejl. Med tjekket
beholder vi bare den tomme liste. `indent=2` gør filen pæn at læse for et
menneske, med én ting pr. linje.

**Getters**

```python
def get_highscores():
    return highscores

def get_edit_row():
    return edit_row

def is_editing():
    return edit_row is not None
```

Samme mønster som **is_game_over()** fra uge 4 og **get_snake_body()** fra
bonusugen: andre filer må gerne *kigge* på listen, men de ændrer den ikke.

**Kommer scoren på listen?**

```python
def is_highscore(score):
    if score == 0:
        return False                          # 0 point kommer aldrig på listen
    if len(highscores) < MAX_ENTRIES:
        return True                           # der er stadig ledige pladser
    return score > highscores[-1]["score"]    # bedre end den sidste på listen?
```

Når listen er fuld, behøver vi kun at sammenligne med den *sidste*. Er man
bedre end nummer 10, er man med.

**Sæt scoren ind på den rigtige plads**

```python
def insert_score(score):
    global edit_row
    pos = 0
    # Gå ned gennem listen, så længe dem på listen har mindst lige så mange point
    while pos < len(highscores) and highscores[pos]["score"] >= score:
        pos += 1

    today = date.today().strftime("%d-%m-%Y")  # fx "11-11-2026"
    entry = {"name": "", "score": score, "date": today}
    highscores.insert(pos, entry)
    del highscores[MAX_ENTRIES:]              # smid nummer 11 ud, hvis der er en
    edit_row = pos
```

Lad os prøve med en liste, hvor scorerne er `[120, 90, 40]`, og man har fået
`70` point:

| ***pos*** | `highscores[pos]["score"]` | `>= 70`? | Hvad sker der? |
|---|---|---|---|
| 0 | 120 | ja | gå videre |
| 1 | 90 | ja | gå videre |
| 2 | 40 | nej | stop, ***pos*** er `2` |

**insert()** sætter den nye linje ind på plads `2` og skubber `40` en plads
ned, så listen bliver `[120, 90, 70, 40]`. Var listen fuld, ville der nu være
11, og `del highscores[MAX_ENTRIES:]` sletter alt fra plads 10 og frem, altså
nummer 11.

Navnet starter som en tom tekst `""`, for det har spilleren ikke skrevet
endnu. Til sidst husker vi i ***edit_row***, hvilken linje der skal skrives i.

**strftime()** laver en dato om til tekst: `%d` er dagen, `%m` er måneden, og
`%Y` er året med fire cifre.

**Skriv et bogstav**

```python
def add_letter(text):
    letter = text.upper()                     # "b" bliver til "B"
    if len(letter) != 1 or letter not in ALLOWED_LETTERS:
        return                                # ikke et bogstav fra A til Z
    entry = highscores[edit_row]
    if len(entry["name"]) < 3:
        entry["name"] += letter
```

**upper()** laver små bogstaver om til store, så både `b` og `B` bliver til
`B`. Skriver man `bos`, står der altså `BOS`.

**Lås linjen med Enter**

```python
def confirm_name():
    global edit_row
    if len(highscores[edit_row]["name"]) < 3:
        return                                # alle tre bogstaver skal være skrevet
    edit_row = None                           # nu er linjen låst
    save_highscores()
```

Når ***edit_row*** er `None`, kan **add_letter()** ikke længere komme til
linjen. Den er låst. Først nu bliver listen gemt i filen.

**Nederst: hent listen, når filen importeres**

```python
load_highscores()
```

Det er samme idé som **reset()** nederst i `snake.py`: listen er klar, så
snart nogen skriver `import highscore`.

### `highscore.py` (hele filen)

```python
import json
from pathlib import Path
from datetime import date

HIGHSCORE_FILE = "highscore.json"
MAX_ENTRIES = 10                              # vi viser 10 pladser, ligesom på en arkademaskine
ALLOWED_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

highscores = []    # liste med én ordbog pr. plads: {"name": ..., "score": ..., "date": ...}
edit_row = None    # den række, der skrives navn i lige nu (None = ingen)

def load_highscores():
    global highscores
    if Path(HIGHSCORE_FILE).exists():
        with open(HIGHSCORE_FILE) as f:
            highscores = json.load(f)

def save_highscores():
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(highscores, f, indent=2)

def get_highscores():
    return highscores

def get_edit_row():
    return edit_row

def is_editing():
    return edit_row is not None

def is_highscore(score):
    if score == 0:
        return False                          # 0 point kommer aldrig på listen
    if len(highscores) < MAX_ENTRIES:
        return True                           # der er stadig ledige pladser
    return score > highscores[-1]["score"]    # bedre end den sidste på listen?

def insert_score(score):
    global edit_row
    pos = 0
    # Gå ned gennem listen, så længe dem på listen har mindst lige så mange point
    while pos < len(highscores) and highscores[pos]["score"] >= score:
        pos += 1

    today = date.today().strftime("%d-%m-%Y")  # fx "11-11-2026"
    entry = {"name": "", "score": score, "date": today}
    highscores.insert(pos, entry)
    del highscores[MAX_ENTRIES:]              # smid nummer 11 ud, hvis der er en
    edit_row = pos

def add_letter(text):
    letter = text.upper()                     # "b" bliver til "B"
    if len(letter) != 1 or letter not in ALLOWED_LETTERS:
        return                                # ikke et bogstav fra A til Z
    entry = highscores[edit_row]
    if len(entry["name"]) < 3:
        entry["name"] += letter

def confirm_name():
    global edit_row
    if len(highscores[edit_row]["name"]) < 3:
        return                                # alle tre bogstaver skal være skrevet
    edit_row = None                           # nu er linjen låst
    save_highscores()

load_highscores()
```

### Trin 3 — Tegn highscore-skærmen i `hud.py`

Alt, der skrives som tekst på skærmen, hører hjemme i `hud.py`. Først skal
`hud.py` kunne spørge `highscore.py` om listen. Tilføj en import lige under
`import globals as GL`:

```python
import globals as GL
from highscore import get_highscores, get_edit_row, is_editing
```

Tilføj så en ny funktion nederst i `hud.py`:

```python
# Uge 7 - Tegn highscore-listen
def draw_highscores(screen):
    draw_text_img(screen, "HIGHSCORES", GL.LARGE_SIZE, -200)

    if not get_highscores():
        draw_text_img(screen, "NO HIGHSCORES YET", GL.FIXED_SIZE, 0)

    # Stregerne er tændt i 400 ms og slukket i 400 ms - så blinker de
    blink_on = (pygame.time.get_ticks() // 400) % 2 == 0

    for idx, entry in enumerate(get_highscores()):
        name = entry["name"]
        if idx == get_edit_row():
            if blink_on:
                fill = "-"
            else:
                fill = " "
            name = name + fill * (3 - len(name))   # fyld op til 3 tegn
        text = f"{idx + 1:2}. {name} {entry['score']:03d} {entry['date']}"
        draw_text_img(screen, text, GL.FIXED_SIZE, -130 + idx * 34)

    if is_editing():
        draw_text_img(screen, "TYPE YOUR INITIALS", GL.FIXED_SIZE, 230)
    else:
        draw_text_img(screen, "PRESS <ESC> FOR MENU", GL.FIXED_SIZE, 230)
```

**Sådan blinker stregerne.** **pygame.time.get_ticks()** er antal
millisekunder, siden spillet startede. Deler vi med 400 (og smider resten
væk med `//`), tæller tallet én op hvert 400. millisekund. `% 2` giver så
skiftevis `0` og `1`:

| `get_ticks()` | `// 400` | `% 2` | ***blink_on*** |
|---|---|---|---|
| 0 - 399 | 0 | 0 | True |
| 400 - 799 | 1 | 1 | False |
| 800 - 1199 | 2 | 0 | True |

**Sådan bliver navnet fyldt op.** `"-" * 3` giver `"---"`. Har spilleren
skrevet `"B"`, er `3 - len(name)` lig med `2`, så der står `"B--"`. Når
stregerne er slukket, fylder vi op med mellemrum i stedet, og
**draw_text_img()** springer mellemrum over. Bogstaverne står stille, kun
stregerne blinker.

**Sådan bliver linjen skrevet.** `{idx + 1:2}` skriver pladsnummeret med 2
tegns bredde, så ` 1.` og `10.` står pænt under hinanden. `{entry['score']:03d}`
er samme trick som i HUD'en: altid 3 cifre. En linje ser fx sådan ud:

```
 1. BOS 120 11-11-2026
```

Fordi alle linjer er lige lange, står de pænt under hinanden, selvom
**draw_text_img()** centrerer hver linje for sig.

### Trin 4 — Highscore-skærmen i `snake_game.py`

Nu skal hovedprogrammet bruge alt det nye. Der er fire små ændringer.

**1. Imports.** Tilføj **draw_highscores** til hud-importen, og importer de
funktioner fra `highscore.py`, vi skal bruge:

```python
from hud import draw_hud_img, draw_text_img, draw_highscores
```

```python
import ai
from highscore import is_highscore, insert_score, is_editing, add_letter, confirm_name
```

**2. En fejl, der venter på at ske.** Sådan så det ud i bonusugen:

```python
        if event.type == SNAKE_MOVE and game_mode != "menu" and not is_game_over():
```

Nu får vi en ny "skærm", `"highscore"`. Hvad sker der med slangen, når vi
står på highscore-skærmen? `game_mode != "menu"` er sandt, så slangen kører
videre usynligt i baggrunden. I stedet for at skrive "alt undtagen menuen"
skriver vi præcis, hvornår slangen må flytte sig:

```python
        if event.type == SNAKE_MOVE and game_mode in ("player", "ai") and not is_game_over():
```

**Det er en god vane at sige, hvad der *skal* ske, i stedet for hvad der
*ikke* skal ske.** Så går det ikke galt, næste gang der kommer en ny skærm.

**3. Kom spilleren på listen?** Lige efter `score += 10`, stadig inde i
`SNAKE_MOVE`-blokken:

```python
            # Uge 7 - Kom spilleren på highscore-listen? (AI'en må ikke komme på listen)
            if is_game_over() and game_mode == "player" and is_highscore(score):
                insert_score(score)
                game_mode = "highscore"
```

Det sker kun i præcis det skridt, hvor slangen dør. Ved næste
`SNAKE_MOVE` er `is_game_over()` sand, og så kommer vi slet ikke ind i
blokken igen.

**4. Taster på highscore-skærmen.** Øverst i `KEYDOWN`-blokken, lige *før*
menu-delen:

```python
        if event.type == pygame.KEYDOWN:
            # Uge 7 - Highscore-skærmen: skriv initialer, eller gå tilbage til menuen
            if game_mode == "highscore":
                if is_editing():
                    if event.key == pygame.K_RETURN:
                        confirm_name()
                    else:
                        add_letter(event.unicode)
                elif event.key == pygame.K_ESCAPE:
                    game_mode = "menu"
                continue  # på highscore-skærmen styrer piletasterne ingenting

            if game_mode == "menu":
```

***event.key*** fortæller, *hvilken tast* der blev trykket på. Men
***event.unicode*** fortæller, *hvilket tegn* tasten skrev, fx `"b"`, `"B"`
eller `"7"`. Til navne er tegnet det, vi skal bruge. **add_letter()** sorterer
selv alt fra, som ikke er A til Z.

Læg mærke til, at ESC kun virker, når linjen er låst. Man skal skrive sine
initialer færdig, ligesom på en rigtig arkademaskine.

**5. Tegn skærmen.** I tegnedelen, mellem menuen og selve spillet:

```python
    if game_mode == "menu":
        draw_text_img(screen, "SNAKE", GL.LARGE_SIZE, -100)
        draw_text_img(screen, "1. PLAY SNAKE", GL.FIXED_SIZE, 0)
        draw_text_img(screen, "2. AI PLAYS SNAKE", GL.FIXED_SIZE, 50)
    elif game_mode == "highscore":
        draw_highscores(screen)
    else:
```

### `snake_game.py` (opdateret)

```python
import pygame
pygame.init()

import globals as GL
GL.init()

from hud import draw_hud_img, draw_text_img, draw_highscores
from snake import draw_snake, move_snake, change_direction, draw_apple, place_apple, is_game_over, reset
from board import draw_wall, is_wall, draw_obstacles, place_obstacles

import ai
from highscore import is_highscore, insert_score, is_editing, add_letter, confirm_name

WIDTH = GL.BOARD_COLUMNS * GL.CELL_SIZE
HEIGHT = GL.BOARD_ROWS * GL.CELL_SIZE

score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT + GL.CELL_SIZE))
pygame.display.set_caption("Snake")

def draw_grass():
    for x in range(GL.BOARD_COLUMNS):
        for y in range(1, GL.BOARD_ROWS + 1):
            # Vi tegner nu græsset. For at give det mere liv, skifter vi farve, for hver celle.
            if (x + y) % 2 == 0:
                rect_color = pygame.Color("green3")
            else:
                rect_color = pygame.Color("lawngreen")
            grass = pygame.Rect(x * GL.CELL_SIZE, y * GL.CELL_SIZE, GL.CELL_SIZE, GL.CELL_SIZE)
            pygame.draw.rect(screen, rect_color, grass)

# Lav en helt ny slags "begivenhed" (event), som kun vi selv bruger
SNAKE_MOVE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_MOVE, 150)  # send begivenheden hvert 150. millisekund

clock = pygame.time.Clock()
running = True

# Uge 6, Bonus - Hvilken "skærm" er vi på? "menu", "player", "ai" eller "highscore"
game_mode = "menu"

def start_game(mode):
    global game_mode, score
    game_mode = mode
    score = 0
    place_obstacles()
    reset()


while running:
    for event in pygame.event.get():
        # Luk spillet        
        if event.type == pygame.QUIT:
            running = False

        if event.type == SNAKE_MOVE and game_mode in ("player", "ai") and not is_game_over():
            if game_mode == "ai":
                # AI'en "trykker på tasterne" lige før slangen flytter sig
                action = ai.choose_action(ai.get_state())
                change_direction(ai.action_to_direction(action))
            ate_apple = move_snake(GL.BOARD_COLUMNS, GL.BOARD_ROWS)
            if ate_apple:
                score += 10

            # Uge 7 - Kom spilleren på highscore-listen? (AI'en må ikke komme på listen)
            if is_game_over() and game_mode == "player" and is_highscore(score):
                insert_score(score)
                game_mode = "highscore"

        if event.type == pygame.KEYDOWN:
            # Uge 7 - Highscore-skærmen: skriv initialer, eller gå tilbage til menuen
            if game_mode == "highscore":
                if is_editing():
                    if event.key == pygame.K_RETURN:
                        confirm_name()
                    else:
                        add_letter(event.unicode)
                elif event.key == pygame.K_ESCAPE:
                    game_mode = "menu"
                continue  # på highscore-skærmen styrer piletasterne ingenting

            if game_mode == "menu":
                if event.key == pygame.K_1:
                    start_game("player")
                elif event.key == pygame.K_2:
                    ai.load_brain()
                    start_game("ai")
                continue  # i menuen styrer piletasterne ingenting

            if event.key == pygame.K_ESCAPE:
                game_mode = "menu"
            elif event.key == pygame.K_SPACE and is_game_over():
                start_game(game_mode)

            match event.key:
                case pygame.K_UP | pygame.K_w:
                    change_direction((0, -1))
                case pygame.K_DOWN | pygame.K_s:
                    change_direction((0, 1))
                case pygame.K_LEFT | pygame.K_a:
                    change_direction((-1, 0))
                case pygame.K_RIGHT | pygame.K_d:
                    change_direction((1, 0))

    draw_hud_img(screen, score)
    draw_grass()
    draw_wall(screen)

    if game_mode == "menu":
        draw_text_img(screen, "SNAKE", GL.LARGE_SIZE, -100)
        draw_text_img(screen, "1. PLAY SNAKE", GL.FIXED_SIZE, 0)
        draw_text_img(screen, "2. AI PLAYS SNAKE", GL.FIXED_SIZE, 50)
    elif game_mode == "highscore":
        draw_highscores(screen)
    else:
        draw_obstacles(screen)
        draw_apple(screen)
        draw_snake(screen)

        if is_game_over():
            draw_text_img(screen, "GAME OVER", GL.LARGE_SIZE, 0)
            draw_text_img(screen, "PRESS <SPACE> TO START NEW GAME", GL.FIXED_SIZE, 0 + GL.LARGE_SIZE[1] + 10)
            draw_text_img(screen, "PRESS <ESC> FOR MENU", GL.FIXED_SIZE, 0 + GL.LARGE_SIZE[1] + 50)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

### Prøv selv

1. Spil et spil og skriv `bos`. Står der `BOS`? Prøv at trykke Enter efter
   kun to bogstaver. Hvad sker der?
2. Prøv at skrive `æ`, `7` eller trykke på mellemrum, mens I skriver
   initialer. Hvorfor sker der ingenting?
3. Ændr `400` i **draw_highscores()** til `100` og til `1000`. Hvordan blinker
   stregerne nu?
4. Ændr ***MAX_ENTRIES*** til `3`, og spil nogle spil. Hvad sker der med den
   dårligste score, når listen er fuld? Husk at sætte tallet tilbage til `10`.
5. Lad AI'en spille et spil. Kommer den på listen?
6. Åbn `highscore.json` i jeres editor, og kig på den. Ret nu jeres egen
   score til `999`, gem filen, og start spillet. Hvad står der på listen? Er
   det i orden? *(Det kigger vi på i næste uge.)*

---

## Opgaver

#### Opgave 1 — Bedste score i HUD'en

Øverst på skærmen står `SCORE 040`. Til højre på samme linje skal der nu
også stå den bedste score på listen, fx `HI 120`. Er listen tom, står der
`HI 000`.

*Tip 1:* Lav en ny funktion, **get_best_score()**, i `highscore.py`. Husk, at
den bedste altid står på plads `0`. Hvad skal funktionen svare, hvis listen
er tom?

*Tip 2:* **draw_hud_img()** i `hud.py` skal have den bedste score med som en
ekstra parameter, fx `draw_hud_img(screen, score, best)`. Kaldet står i
`snake_game.py` lige over **draw_grass()**.

*Tip 3:* I **draw_hud_img()** bliver tegnene sat ved `(idx + 1) * 20`. Den
nye tekst skal tegnes længere til højre. Hvor bred er skærmen? Hvor mange
pixels fylder `"HI 120"`, når hvert tegn er 20 pixels bredt?

*Tænk over:* Hvis I slår rekorden midt i et spil, skal `HI` så ændre sig med
det samme, eller først når I har skrevet jeres initialer? Der er ikke ét
rigtigt svar, men prøv at finde ud af, hvad jeres kode gør nu.

#### Opgave 2 — "3. HIGHSCORES" i menuen

Man skal kunne se listen uden at spille først. I menuen tilføjes en tredje
linje, `3. HIGHSCORES`. Trykker man `3`, vises highscore-skærmen, og ESC går
tilbage til menuen.

*Tip 1:* Menu-teksten tegnes i `snake_game.py` med **draw_text_img()**. Kig
på, hvordan linje 1 og 2 er lavet, og læg 50 til y-værdien.

*Tip 2:* Tasterne til menuen står i menu-delen af `KEYDOWN`-blokken, hvor
`K_1` og `K_2` allerede er. Tasten hedder `pygame.K_3`.

*Tip 3:* I behøver ikke at kalde **start_game()**. Det er nok at ændre
***game_mode***. Highscore-skærmen og ESC virker allerede fra Trin 4.

*Tænk over:* Prøv at trykke `3` i menuen. Kører slangen videre bag listen?
Hvad ville der være sket, hvis vi ikke havde rettet `game_mode != "menu"` i
Trin 4?

#### Opgave 3 (bonus) — Slet et bogstav

Har man tastet forkert, kan man ikke rette det. Backspace skal slette det
sidste bogstav, men kun mens linjen ikke er låst.

*Tip 1:* Kun `highscore.py` må ændre i listen. Lav derfor en ny funktion,
**remove_letter()**, ved siden af **add_letter()**.

*Tip 2:* `"BOS"[:-1]` giver `"BO"`. Det er samme trick som
`snake_body[:-1]`, som fjerner halen på slangen.

*Tip 3:* Tasten hedder `pygame.K_BACKSPACE`. Den skal fanges i
`snake_game.py`, samme sted som `K_RETURN`, så den ikke bliver sendt videre
til **add_letter()**.

*Tænk over:* Hvad sker der, hvis man trykker Backspace, når navnet allerede
er tomt? Går det godt, eller skal I tjekke for det?

---

## Kommende uger (planlagt)

- **Uge 8 — Anti-snyd.** I opdagede i *Prøv selv 6*, at man bare kan rette i
  `highscore.json`. Derfor laver vi en **checksum**: et tal, der regnes ud fra
  hele listen og et hemmeligt tal, og som gemmes sammen med listen. Passer
  tallet ikke, når filen læses, er der snydt. Så vises teksten `HIGHSCORE HAS
  BEEN TAMPERED WITH` på skrå hen over highscore-skærmen som et
  gennemsigtigt vandmærke, og der står ingen `HI` i HUD'en. En snydt liste
  bliver aldrig gemt igen, og ingen kan komme på den, så snyderiet ikke kan
  "vaskes" af en ny highscore. Vi laver også en reset-funktion, der tømmer
  listen og gør den gyldig igen.

*(Denne liste opdateres løbende, efterhånden som vi bliver enige om det
præcise indhold for hver uge.)*
