# Snake i Pygame — Bonus: En AI, der selv spiller Snake

Spillet er færdigt: slangen vokser, dør, kører gennem tunneller og undgår
forhindringer. Nu skal vi lave noget, der lyder meget sværere, end det er.
Vi bygger en **kunstig intelligens** (AI), som lærer sig selv at spille
Snake. Vi fortæller den ikke, *hvordan* man spiller. Den finder ud af det
selv ved at prøve, fejle og prøve igen, tusindvis af gange.

Og så laver vi en menu, når spillet starter:

```
1. PLAY SNAKE
2. AI PLAYS SNAKE
```

*Bemærk:* Vi bruger **ingen** ekstra programmer eller biblioteker: ingen
grafikkort, ingen CUDA, ingen PyTorch. Alt det, AI'en skal bruge, er
almindelig Python, som I allerede kender: lister, ordbøger (`dict`),
`random` og `json`. Træningen tager omkring 10 sekunder på en helt
almindelig computer.

## Hvordan kan en computer lære noget?

Tænk på, hvordan man lærer en hund at sidde. Man forklarer den ikke, hvad
"sidde" betyder. Man venter, til den gør det rigtige, og så får den en
godbid. Gør den det forkerte, får den ingenting. Efter mange forsøg har
hunden lært, at "sidde, når der bliver sagt sit" giver godbidder.

Det kaldes **forstærkningslæring** (på engelsk *reinforcement learning*),
og det er præcis sådan, vores AI lærer:

- Spiser slangen et æble, får den **+10** point i belønning.
- Dør den, får den **−10**.
- Alt andet giver **0**.

### AI'ens notesbog: Q-tabellen

AI'en har en notesbog. På hver side står en **situation**, og under den
står en **karakter** for hvert af de tre ting, slangen kan gøre:

| Situation | Ligeud | Drej til højre | Drej til venstre |
|---|---|---|---|
| "Mur lige foran, æblet er til højre" | −9.8 | 6.2 | −1.5 |

Når AI'en skal vælge, slår den situationen op og vælger det med **højest
karakter**. Hver gang den har prøvet noget, retter den karakteren lidt:
gik det godt, går karakteren op, gik det skidt, går den ned. Notesbogen
kaldes en **Q-tabel** (Q for *quality*, "hvor godt er det her valg?"), og
metoden hedder **Q-learning**.

### Hvad AI'en kan "se"

AI'en kan ikke se skærmen, som I kan. Den får i stedet svar på **11 ja/nej-
spørgsmål**, hver gang slangen skal flytte sig:

1. Dør jeg, hvis jeg kører **lige frem**?
2. Dør jeg, hvis jeg drejer til **højre**?
3. Dør jeg, hvis jeg drejer til **venstre**?
4. – 7. Kører jeg **op**, **ned**, **til venstre** eller **til højre**?
8. – 11. Er æblet **over** mig, **under** mig, **til venstre** eller
   **til højre** for mig?

Svarene skrives som en tekst med `0` (nej) og `1` (ja), fx
`"00000010001"`. Det er "situationen", AI'en slår op i notesbogen.

*Tænk over:* 11 ja/nej-spørgsmål giver 2¹¹ = 2048 mulige kombinationer.
Men mange af dem kan aldrig ske. Slangen kan fx ikke køre op **og** til
venstre på samme tid. Hvor mange situationer tror I, AI'en ender med at
kende? (Svaret står i træningen nedenfor.)

### Ligeud, højre, venstre — ikke op, ned, venstre, højre

Læg mærke til, at AI'en tænker i forhold til **sig selv**: ligeud, drej
til højre, drej til venstre. Ikke i op/ned/venstre/højre, som piletasterne.
Det gør den af to grunde:

- Den kan aldrig vælge at køre baglæns ind i sig selv. Det valg findes
  slet ikke.
- "Mur lige foran mig" er den samme situation, uanset om slangen kører op
  eller til venstre. Så kan erfaringen bruges begge steder.

---

## Nyt mønster: AI'en spiller *det rigtige spil*

Husk tommelfingerreglen fra uge 5: al viden om muren bor ét sted, i
`is_wall()`, så tegningen og kollisionen aldrig kan blive uenige.

Det samme gælder AI'en. Man kunne fristes til at skrive en lille "øve-udgave"
af Snake til AI'en. Men så findes reglerne pludselig **to** steder igen, og
glemmer man at rette det ene sted, øver AI'en sig på et spil, der ikke er
det samme som det rigtige. Den har så lært at køre gennem tunneller, der
ikke virker, eller at undgå forhindringer, der ikke findes.

I stedet bruger AI'en **præcis de samme funktioner** som spilleren:

- Den læser spillet med `get_snake_body()`, `get_direction()` og
  `get_apple_pos()`.
- Den "trykker på tasterne" med `change_direction()`, lige som jer.
- Slangen flyttes af den samme `move_snake()`.

AI'en er med andre ord bare en **ekstra spiller**, der sidder ved tastaturet.

### Trin 1 — Getters i `snake.py`

AI'en skal kunne se, hvor slangen og æblet er. I uge 4 lærte I, hvorfor
`snake_game.py` ikke må skrive `from snake import game_over`: man får en
gammel kopi og opdager aldrig, at værdien ændrer sig. Derfor lavede vi
`is_game_over()`.

Det samme gælder `snake_body`, `direction` og `apple_pos`. Tilføj tre nye
funktioner i `snake.py`, lige under `is_game_over()`:

```python
# Bonus - "Getters", så AI'en kan se, hvordan spillet ser ud lige nu
def get_snake_body():
    return snake_body

def get_direction():
    return direction

def get_apple_pos():
    return apple_pos
```

En funktion, der bare "henter" en værdi, kaldes en **getter** (af engelsk
*get*, at hente).

### Trin 2 — `next_position()` og `is_deadly()`

AI'ens tre første spørgsmål er: "dør jeg, hvis jeg kører ligeud / til højre
/ til venstre?". For at svare skal den vide, hvilket felt hovedet ender på,
**også når slangen kører gennem en tunnel**, og om det felt er farligt.

Det spørgsmål stiller `move_snake()` allerede selv, hver gang slangen
flytter sig. Så i stedet for at AI'en skal regne det ud på sin egen måde
(og måske regne forkert), flytter vi svaret ud i to funktioner, som både
`move_snake()` og AI'en kan spørge. Læg dem i `snake.py`, lige over
`step()`:

```python
# Bonus - Hvor ender hovedet, hvis det tager ét skridt i retning 'd'?
def next_position(pos, d):
    x = (pos[0] + d[0]) % GL.BOARD_COLUMNS          # 24 -> 0, -1 -> 23
    y = (pos[1] + d[1] - 1) % GL.BOARD_ROWS + 1     # 17 -> 1,  0 -> 16
    return (x, y)

# Bonus - Dør slangen, hvis hovedet havner på feltet 'pos'?
def is_deadly(pos):
    x, y = pos
    return pos in snake_body[:-1] or is_wall(x, y)
```

Kan I genkende `%`? Det er modulo-tricket fra "Tænk over" i uge 5, opgave 1.
Vandret virker det direkte. Lodret skal vi huske, at banen starter i række
1 og ikke i række 0. Derfor trækker vi 1 fra **før** `%` og lægger 1 til
igen **bagefter**. Regn efter med `y = 0` (slangen kører ud foroven) og
`y = 17` (slangen kører ud forneden).

Nu kan `move_snake()` blive meget kortere. Alt mellem `head_x, head_y =
snake_body[0]` og `ate_apple = new_head == apple_pos`, altså udregningen af
det nye hoved, tunnel-`if`'erne og de to tjek for kollision, bliver erstattet
af:

```python
    new_head = next_position(snake_body[0], direction)

    if is_deadly(new_head):
        game_over = True
        return False

```

Hele `move_snake()` ser nu sådan ud:

```python
def move_snake(cols, rows):
    global snake_body, direction, game_over
    direction = next_direction

    # Uge 3, Opgave 2 - Tjek timeout for æble. Hvis tiden er gået, placér nyt æble
    if pygame.time.get_ticks() - apple_ticks >= GL.APPLE_TIMEOUT:
        place_apple()

    new_head = next_position(snake_body[0], direction)

    if is_deadly(new_head):
        game_over = True
        return False

    ate_apple = new_head == apple_pos

    if ate_apple:
        # Uge 3, Opgave 1 - Slangen vokser, når den spiser æblerne
        snake_body = [new_head] + snake_body
        place_apple()
    else:
        snake_body = [new_head] + snake_body[:-1]

    return ate_apple
```

*Bemærk:* `cols` og `rows` bliver faktisk ikke brugt længere, fordi
`next_position()` henter størrelsen fra `GL`. Vi lader dem stå, så I ikke
også skal rette i `snake_game.py`. Hvis I har lyst, må I gerne fjerne dem
begge steder bagefter.

Start spillet og kør gennem alle fire tunneller, ind i muren, ind i en
forhindring og ind i jer selv. Det hele skal opføre sig som før. Vi har
kun flyttet koden rundt, ikke ændret, hvad den gør. Sådan en ombygning
kaldes **refaktorering**, ligesom `globals.py` i uge 3.

*Tænk over:* Kom slangen nogle gange ud et forkert sted, eller forsvandt
den et øjeblik uden for skærmen, da I kørte gennem tunnellerne i uge 5?
Prøv igen nu. Med `%` er der kun én udregning for alle fire sider, så der
er ikke fire `if`-sætninger, der hver især kan have en lille fejl.

### Trin 3 — `ai.py`: AI'ens hjerne

Opret en ny fil, `ai.py`. Den er lidt lang, så vi tager den i stykker
bagefter:

```python
# ai.py - AI'ens "hjerne": hvad ser den, hvad kan den gøre, og hvad har den lært?
import random
import json
from snake import get_snake_body, get_direction, get_apple_pos, next_position, is_deadly

BRAIN_FILE = "q_table.json"

# AI'en tænker ikke i op/ned/venstre/højre, men i forhold til sig selv:
STRAIGHT = 0
TURN_RIGHT = 1
TURN_LEFT = 2

def turn_right(d):
    dx, dy = d
    return (-dy, dx)

def turn_left(d):
    dx, dy = d
    return (dy, -dx)

def action_to_direction(action):
    d = get_direction()
    if action == TURN_RIGHT:
        return turn_right(d)
    if action == TURN_LEFT:
        return turn_left(d)
    return d

# --- Hvad AI'en "ser": 11 ja/nej-spørgsmål, skrevet som en tekst med 0 og 1 ---
def get_state():
    body = get_snake_body()
    head = body[0]
    d = get_direction()
    apple_x, apple_y = get_apple_pos()
    head_x, head_y = head

    answers = [
        is_deadly(next_position(head, d)),               # fare lige frem?
        is_deadly(next_position(head, turn_right(d))),   # fare til højre?
        is_deadly(next_position(head, turn_left(d))),    # fare til venstre?
        d == (0, -1),                                    # kører jeg op?
        d == (0, 1),                                     # kører jeg ned?
        d == (-1, 0),                                    # kører jeg til venstre?
        d == (1, 0),                                     # kører jeg til højre?
        apple_y < head_y,                                # er æblet over mig?
        apple_y > head_y,                                # er æblet under mig?
        apple_x < head_x,                                # er æblet til venstre?
        apple_x > head_x,                                # er æblet til højre?
    ]
    return "".join("1" if a else "0" for a in answers)

# --- Hvad AI'en har lært: en karakter til hvert af de 3 valg, i hver situation ---
q_table = {}

def scores_for(state):
    if state not in q_table:
        q_table[state] = [0.0, 0.0, 0.0]   # ny situation: ingen erfaring endnu
    return q_table[state]

def choose_action(state, explore=0.0):
    if random.random() < explore:
        return random.randint(0, 2)        # prøv noget tilfældigt
    scores = scores_for(state)
    return scores.index(max(scores))       # vælg det, der hidtil har virket bedst

def learn(state, action, reward, new_state, done):
    LEARNING_RATE = 0.1   # hvor meget én ny erfaring må flytte karakteren
    FUTURE = 0.9          # hvor meget "det, der sker bagefter" tæller med
    if done:
        target = reward
    else:
        target = reward + FUTURE * max(scores_for(new_state))
    scores = scores_for(state)
    scores[action] += LEARNING_RATE * (target - scores[action])

def save_brain():
    # Én linje pr. situation, med 2 decimaler, så filen er til at læse for et menneske
    lines = []
    for state in sorted(q_table):
        scores = [round(s, 2) for s in q_table[state]]
        lines.append(f'  "{state}": {json.dumps(scores)}')
    with open(BRAIN_FILE, "w") as f:
        f.write("{\n" + ",\n".join(lines) + "\n}\n")

def load_brain():
    global q_table
    with open(BRAIN_FILE) as f:
        q_table = json.load(f)
```

Lad os tage den bid for bid.

**`turn_right()` og `turn_left()`** drejer en retning en kvart omgang.
Prøv at regne efter: kører slangen til højre, `(1, 0)`, giver
`turn_right()` `(0, 1)`, altså ned. Det passer: drejer man til højre, mens
man kører mod højre på skærmen, ender man med at køre nedad. (Husk, at `y`
bliver **større** nedad på skærmen.)

**`action_to_direction()`** oversætter AI'ens valg (0, 1 eller 2) til en
rigtig retning, som `change_direction()` forstår.

**`get_state()`** stiller de 11 spørgsmål. Hvert svar er `True` eller
`False`, og den sidste linje laver dem om til en tekst som `"00000010001"`.
Læg mærke til de tre første spørgsmål: de bruger `next_position()` og
`is_deadly()` fra trin 2. AI'en spørger altså **spillet** om, hvad der er
farligt, i stedet for at gætte selv.

**`q_table`** er notesbogen: en ordbog, hvor nøglen er situationen, og
værdien er en liste med tre karakterer, én for hvert valg.

**`scores_for()`** slår en situation op. Har AI'en aldrig set situationen
før, skriver den en ny side med `[0.0, 0.0, 0.0]`, altså "ved ikke endnu".

**`choose_action()`** vælger, hvad AI'en skal gøre. Med tallet `explore`
kan man bede den om at prøve noget **tilfældigt** en gang imellem. Er
`explore` fx `0.3`, slår den plat og krone i 30 % af tilfældene. Hvorfor
skulle man nogensinde vælge tilfældigt, når man ved, hvad der virker bedst?
Fordi AI'en i starten **ikke** ved det. Prøver den aldrig noget nyt, finder
den aldrig ud af, at der var noget, der var endnu bedre. Det er ligesom at
bestille det samme hver gang på en restaurant: man bliver aldrig skuffet,
men man finder heller aldrig sin nye livret.

**`learn()`** er hjertet i det hele, og det er kun tre linjer. Den regner
ud, hvad karakteren **burde** have været (`target`):

- Var spillet slut (`done`), er svaret bare belønningen: −10.
- Ellers er det belønningen **plus** hvor godt det ser ud fra den nye
  situation. `max(scores_for(new_state))` er "den bedste karakter, jeg kan
  få derfra". Det er det, der gør, at AI'en lærer at tænke fremad. Drejer
  den hen mod æblet, får den ingen belønning med det samme. Men den nye
  situation ("æblet er lige foran mig") har en høj karakter, så drejet får
  også en god karakter.

`FUTURE = 0.9` betyder, at det, der sker bagefter, tæller lidt mindre end
det, der sker nu. Et æble om lidt er godt, men et æble lige nu er bedre.

Til sidst flyttes den gamle karakter et lille stykke (10 %, `LEARNING_RATE`)
hen mod `target`. Kun et lille stykke ad gangen. Ellers ville ét enkelt
uheld få AI'en til at "glemme" alt, hvad den har lært før.

**`save_brain()` og `load_brain()`** gemmer notesbogen i en fil,
`q_table.json`, og henter den igen. Så skal AI'en kun trænes én gang.

### Trin 4 — `ai_train.py`: AI'en går i skole

Opret en ny fil, `ai_train.py`:

```python
# ai_train.py - Træn AI'en. Kør denne fil FØR I starter "AI plays Snake".
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"   # intet vindue - vi skal bare regne, ikke tegne

import pygame
pygame.init()

import globals as GL
GL.init()

from snake import move_snake, change_direction, reset, is_game_over
from board import place_obstacles
import ai

GAMES = 5000           # hvor mange spil AI'en skal øve sig på
MAX_HUNGRY_MOVES = 300 # så mange skridt uden æble, så stopper vi spillet

scores = []

for game in range(GAMES):
    place_obstacles()
    reset()

    # I starten prøver AI'en en masse tilfældigt - til sidst slet ikke
    explore = max(0.0, 0.5 - game / (GAMES * 0.7) * 0.5)

    apples = 0
    hungry = 0

    while not is_game_over():
        state = ai.get_state()
        action = ai.choose_action(state, explore)
        change_direction(ai.action_to_direction(action))

        ate_apple = move_snake(GL.BOARD_COLUMNS, GL.BOARD_ROWS)
        hungry += 1

        if is_game_over():
            reward = -10
        elif ate_apple:
            reward = 10
            apples += 1
            hungry = 0
        else:
            reward = 0

        done = is_game_over() or hungry > MAX_HUNGRY_MOVES
        ai.learn(state, action, reward, ai.get_state(), done)
        if done:
            break

    scores.append(apples)
    if (game + 1) % 500 == 0:
        last = scores[-500:]
        print(f"Spil {game + 1:5}: gennemsnit {sum(last) / len(last):5.1f} æbler, "
              f"bedste {max(last):3}, situationer kendt: {len(ai.q_table)}")

ai.save_brain()
print("Færdig! Hjernen er gemt i", ai.BRAIN_FILE)
```

Det nye her:

- **`SDL_VIDEODRIVER = "dummy"`** beder pygame om **ikke** at åbne et
  vindue. AI'en skal ikke se på spillet, den skal spille det, så hurtigt
  computeren kan. Linjen skal stå **før** `import pygame`.
- **Ingen `SNAKE_MOVE`-timer og ingen `clock.tick(60)`.** I det rigtige spil
  venter vi 150 millisekunder mellem hvert skridt, så et menneske kan nå
  at reagere. Her kalder vi bare `move_snake()` igen med det samme. Derfor
  kan AI'en spille 5000 spil på få sekunder.
- **Hver omgang i `while`-løkken** er ét skridt: se situationen, vælg,
  "tryk på tasten", flyt slangen, giv belønning, lær. Det er hele
  forstærkningslæringen.
- **`explore`** starter på `0.5` (halvdelen af valgene er tilfældige) og
  falder langsomt til `0`. Efter 70 % af spillene vælger AI'en kun det, den
  tror er bedst.
- **`MAX_HUNGRY_MOVES`** stopper et spil, hvor AI'en har lært at køre i
  ring for evigt. Det dør den ikke af, så uden en grænse ville spillet aldrig
  slutte.

Kør `ai_train.py`. Det tager omkring 10 sekunder, og I skal se noget i stil
med:

```
Spil   500: gennemsnit   1.1 æbler, bedste   6, situationer kendt: 187
Spil  1000: gennemsnit   1.8 æbler, bedste  10, situationer kendt: 212
Spil  1500: gennemsnit   2.4 æbler, bedste  12, situationer kendt: 229
Spil  2000: gennemsnit   3.2 æbler, bedste  16, situationer kendt: 236
Spil  2500: gennemsnit   4.5 æbler, bedste  22, situationer kendt: 247
Spil  3000: gennemsnit   7.2 æbler, bedste  46, situationer kendt: 252
Spil  3500: gennemsnit  15.1 æbler, bedste  50, situationer kendt: 255
Spil  4000: gennemsnit  22.1 æbler, bedste  57, situationer kendt: 256
Spil  4500: gennemsnit  22.6 æbler, bedste  48, situationer kendt: 256
Spil  5000: gennemsnit  20.7 æbler, bedste  53, situationer kendt: 256
Færdig! Hjernen er gemt i q_table.json
```

Jeres tal bliver ikke præcis de samme. Både æblerne, forhindringerne og de
tilfældige valg er jo tilfældige. Men I skal kunne se, at AI'en bliver
**meget** bedre undervejs. I starten dør den næsten med det samme. Til
sidst spiser den 20 æbler eller mere i gennemsnit.

(Og svaret på "Tænk over" fra før: AI'en kender kun **256** af de 2048
mulige situationer. De andre kan ikke opstå.)

### Kig i AI'ens hjerne

Åbn `q_table.json` i jeres editor. Den ser nogenlunde sådan ud:

```
{
  "00000010001": [9.36, 3.02, 3.11],
  "00000010010": [1.76, 1.62, 2.77],
  ...
```

Tag den første linje og læs de 11 tegn ét ad gangen ud fra listen med
spørgsmål:

- `000` — ingen fare ligeud, til højre eller til venstre
- `0001` — slangen kører **til højre**
- `0001` — æblet er **til højre** for slangen

Og karaktererne: ligeud `9.36`, drej til højre `3.02`, drej til venstre
`3.11`. AI'en har selv fundet ud af, at når æblet er lige foran, skal man
køre ligeud. Ingen har fortalt den det.

*Tænk over:* Prøv selv at læse den anden linje, `"00000010010"`. Hvor er
æblet? Giver AI'ens bedste valg mening?

---

## Bonus — Menu og AI-tilstand

**Mål:**
- Spillet starter med en menu: `1. PLAY SNAKE` og `2. AI PLAYS SNAKE`
- Vælger man 2, styrer AI'en slangen
- Med ESC kommer man tilbage til menuen

### Opgave 1 — Bogstaverne mangler

Prøv at skrive `draw_text_img(screen, "PLAY", GL.FIXED_SIZE, 0)` et sted i
hovedløkken og start spillet. Det crasher med `KeyError: 'Y'`. `font_img`
i `globals.py` stopper nemlig ved `W` — vi har bare ikke haft brug for de
sidste bogstaver før nu.

Tilføj `X`, `Y`, `Z` og punktum (`.`) til `font_img`. Billedet til punktum
hedder `_Period.png`, og det ligger i samme mappe som de andre.

*Bemærk:* Husk **tabulator**, ikke mellemrum, i `globals.py`.

### Opgave 2 — Menuen

Lige nu starter spillet direkte. Det skal i stedet starte i en menu.

*Tip 1:* Lav en ny variabel i `snake_game.py`, lige før hovedløkken:

```python
game_mode = "menu"
```

Den kan have tre værdier: `"menu"`, `"player"` og `"ai"`. Det er samme
tankegang som `game_over` i uge 4: en navngivet **tilstand**, som resten af
koden kan spørge til.

*Tip 2:* Når man starter et spil, skal der ske tre ting: scoren nulstilles,
der kommer nye forhindringer, og slangen nulstilles. Det gør I allerede,
når man trykker mellemrum efter Game Over. Saml det i en funktion,
`start_game(mode)`, så I kan bruge den både fra menuen og efter Game Over.
Husk `global` for de variabler, funktionen ændrer.

*Tip 3:* Tasterne til tallene hedder `pygame.K_1` og `pygame.K_2`.

*Tip 4:* I menuen skal slangen hverken flytte sig eller tegnes. Kig på
`if event.type == SNAKE_MOVE and not is_game_over():` — hvad skal der
tilføjes, så slangen står stille, mens man er i menuen? Og hvilke
`draw_...`-kald skal kun ske, når man **ikke** er i menuen?

*Tip 5:* Teksten tegnes med `draw_text_img()`. Det sidste tal er,
hvor langt fra midten af skærmen teksten skal stå. Et negativt tal flytter
teksten **op**.

*Tænk over:* Hvorfor er det en god idé at tegne græsset og muren i
menuen, men ikke slangen og æblet?

<details>
<summary>Facit — prøv selv først!</summary>

```python
# Bonus - Hvilken "skærm" er vi på? "menu", "player" eller "ai"
game_mode = "menu"

def start_game(mode):
    global game_mode, score
    game_mode = mode
    score = 0
    place_obstacles()
    reset()
```

I hovedløkken, i stedet for den gamle `if event.type == pygame.KEYDOWN:`:

```python
        if event.type == pygame.KEYDOWN:
            if game_mode == "menu":
                if event.key == pygame.K_1:
                    start_game("player")
                elif event.key == pygame.K_2:
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
```

Og tegningen:

```python
    draw_hud_img(screen, score)
    draw_grass()
    draw_wall(screen)

    if game_mode == "menu":
        draw_text_img(screen, "SNAKE", GL.LARGE_SIZE, -100)
        draw_text_img(screen, "1. PLAY SNAKE", GL.FIXED_SIZE, 0)
        draw_text_img(screen, "2. AI PLAYS SNAKE", GL.FIXED_SIZE, 50)
    else:
        draw_obstacles(screen)
        draw_apple(screen)
        draw_snake(screen)

        if is_game_over():
            draw_text_img(screen, "GAME OVER", GL.LARGE_SIZE, 0)
            draw_text_img(screen, "PRESS <SPACE> TO START NEW GAME", GL.FIXED_SIZE, 0 + GL.LARGE_SIZE[1] + 10)
            draw_text_img(screen, "PRESS <ESC> FOR MENU", GL.FIXED_SIZE, 0 + GL.LARGE_SIZE[1] + 50)
```

`continue` springer resten af `for`-løkkens krop over og går videre til
næste begivenhed. Så når man er i menuen, når koden aldrig ned til
piletasterne.

</details>

### Opgave 3 — Lad AI'en spille

Nu kan man vælge `2`, men det er stadig jer, der styrer. Gør det sådan, at
AI'en styrer slangen, når `game_mode` er `"ai"`.

*Tip 1:* Øverst i `snake_game.py`: `import ai`.

*Tip 2:* AI'en skal hente sin hjerne fra `q_table.json` med
`ai.load_brain()`. Det sker også i **`snake_game.py`**, i menu-delen af
`KEYDOWN`-blokken, dér hvor der trykkes `2`. Hjernen skal hentes **før**
spillet startes:

```python
                elif event.key == pygame.K_2:
                    ai.load_brain()
                    start_game("ai")
```

*Tænk over:* Glemmer man `ai.load_brain()`, er `q_table` i `ai.py` stadig
den tomme ordbog `{}`. Så får hver eneste situation karaktererne
`[0.0, 0.0, 0.0]`, og `scores.index(max(scores))` vælger altid det
første valg, `0`, altså **ligeud**. Slangen starter i række 8, som er en
tunnel-bane, så den kører bare vandret rundt og rundt gennem tunnellen
for evigt. Prøv det: det er en god måde at *se*, hvad en AI, der intet har
lært, gør.

*Tip 3:* Arbejdet foregår i **`snake_game.py`**, i hovedløkken. Find den
blok, der flytter slangen, hver gang `SNAKE_MOVE`-timeren "tikker":

```python
        if event.type == SNAKE_MOVE and game_mode != "menu" and not is_game_over():
            ate_apple = move_snake(GL.BOARD_COLUMNS, GL.BOARD_ROWS)
            if ate_apple:
                score += 10
```

Her skal AI'en vælge en retning og "trykke på tasten" **lige før**
`move_snake()` kaldes. Men kun når det er AI'en, der spiller. Når I selv
spiller, skal blokken virke præcis som før. Derfor skal de nye linjer
ligge i en `if game_mode == "ai":`, mellem den første linje og
`ate_apple = ...`:

```python
        if event.type == SNAKE_MOVE and game_mode != "menu" and not is_game_over():
            if game_mode == "ai":
                # AI'en "trykker på tasterne" lige før slangen flytter sig
                action = ai.choose_action(ai.get_state())
                change_direction(ai.action_to_direction(action))
            ate_apple = move_snake(GL.BOARD_COLUMNS, GL.BOARD_ROWS)
            if ate_apple:
                score += 10
```

De to linjer i midten er de samme som i `while`-løkken i `ai_train.py`,
bare uden `explore`. Det er hele idéen fra "Nyt mønster": AI'en spiller
på præcis samme måde, uanset om den træner eller I kigger på.

Rækkefølgen betyder noget. `change_direction()` gemmer kun den nye retning
i `next_direction`, og først når `move_snake()` kører, bliver den brugt.
Kalder I AI'en **efter** `move_snake()`, kommer den altid ét skridt for
sent. Den ser på en situation, der allerede er forbi.

*Tip 4:* Piletasterne skal kun virke, når `game_mode` er `"player"`.
Ellers kan I snyde og hjælpe AI'en (prøv det gerne først, det er sjovt).

*Tænk over:* Hvorfor kalder vi `choose_action()` **uden** `explore` her?
Hvad ville der ske, hvis AI'en stadig valgte tilfældigt 30 % af gangene,
mens I kigger på?

*Tænk over:* Hvad sker der, hvis man vælger `2`, men har glemt at køre
`ai_train.py` først, så `q_table.json` ikke findes? Kan I få spillet til at
skrive en venlig besked i terminalen i stedet for at crashe? (Hint:
`try:` og `except FileNotFoundError:`.)

### Opgave 4 — I er forskerne

En rigtig AI-forsker bruger det meste af sin tid på at **ændre lidt og
måle igen**. Prøv én ting ad gangen i `ai_train.py` eller `ai.py`, kør
træningen og skriv det sidste gennemsnit ned. Sæt alt tilbage, før I
prøver den næste ting.

| Forsøg | Hvad ændrer I? | Gennemsnit |
|---|---|---|
| A | Ingenting (det normale) | |
| B | `GAMES = 500` | |
| C | `FUTURE = 0.0` | |
| D | Belønning for at dø: `-1` i stedet for `-10` | |
| E | Belønning for æble: `0` i stedet for `10` | |
| F | `explore` altid `0` (ret linjen til `explore = 0`) | |

*Tænk over:*
- Forsøg C: Med `FUTURE = 0.0` kan AI'en kun lære af det, der sker **lige
  nu**. Hvorfor bliver den så dårlig til at finde æbler?
- Forsøg E: Hvad lærer AI'en, når den aldrig bliver belønnet for æbler?
  Kig på, hvordan den kører.
- Forsøg F: Hvorfor er det dårligt aldrig at prøve noget nyt?

### Opgave 5 (svær bonus) — Hvorfor dør AI'en?

Se AI'en spille et par spil. Når slangen bliver lang, dør den næsten altid
på samme måde: den kører ind i en "lomme" i sin egen krop og kan ikke komme
ud igen.

*Tænk over:* Kig på de 11 spørgsmål igen. Hvor langt frem kan AI'en se?
Kan den overhovedet vide, at den er på vej ind i en lomme, før det er for
sent?

*Tænk over:* AI'en ved ikke, at der findes tunneller. Står æblet helt ude
til venstre, og slangen er helt ude til højre, kører den hele vejen hen
over banen, selvom tunnelen ville være kortere. Hvilket spørgsmål kunne man
stille den, så den lærte at bruge tunnellerne?

*Tænk over:* Forhindringerne står et nyt sted i hvert eneste spil. Alligevel
kan AI'en undgå dem, selvom den aldrig har set netop de pladser før.
Hvorfor? (Hint: kig på de tre første spørgsmål. Spørger AI'en "hvor er
forhindringerne?", eller spørger den om noget andet?)

Vil I prøve at gøre AI'en klogere, så husk: hvert nyt ja/nej-spørgsmål
**fordobler** antallet af mulige situationer. AI'en skal så have flere spil
for at lære dem alle at kende. Prøv fx at sætte `GAMES` op til `20000`.
