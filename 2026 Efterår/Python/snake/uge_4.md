# Snake i Pygame — Uge 4

Sidste uge lærte slangen at vokse og at spise æbler med en tidsfrist. Men
prøv at spille et par runder nu: kør slangen lige ind i muren, eller ind i
sin egen krop. Der sker... ingenting. Slangen glider bare videre, som om
intet var hændt. Det er dét, vi retter denne uge: **kollision** og
**Game Over**. Når slangen rammer noget, den ikke må ramme, skal spillet
opdage det, stoppe, og vise spilleren, at det er slut.

## Nyt mønster: en `init()`-funktion i `snake.py`

Kig på toppen af `snake.py`, som den ser ud nu:

```python
snake_body = [(12, 8), (11, 8), (10, 8)]
direction = (1, 0)        # den retning, slangen faktisk bevæger sig i lige nu
next_direction = (1, 0)   # den retning, spilleren senest har bedt om
```

Disse tre linjer bliver kun kørt **én gang** — første gang `snake.py`
importeres. Det har ikke været et problem indtil nu, fordi spillet aldrig
skulle starte forfra. Men det skal det nu: når man er død, skal man kunne
prøve igen, og så skal slangen jo tilbage til sin start-position, med sin
oprindelige længde og retning.

Det er præcis det samme problem, I løste med `globals.py` i uge 3 —
kommentaren dengang nævnte faktisk, at I ville få brug for det igen:

> "Der er også en praktisk gevinst: hvis I i uge 4 skal kunne starte
> spillet forfra efter 'Game Over', kan I genbruge `GL.init()` til at
> nulstille de delte værdier."

Løsningen er den samme opskrift: saml opsætningen i en funktion, i stedet
for at lade den stå som løse linjer øverst i filen:

```python
def reset():
    global snake_body, direction, next_direction, game_over
    snake_body = [(12, 8), (11, 8), (10, 8)]
    direction = (1, 0)
    next_direction = (1, 0)
    game_over = False
    place_apple()
```

`reset()` skal ligge nederst i `snake.py`, dér hvor `place_apple()` er
defineret — den kalder jo `place_apple()` selv. Erstat den gamle linje
`place_apple()` (som kaldes helt til sidst i filen, "så der er et æble fra
start") med et kald til `reset()` i stedet:

```python
reset()  # sætter slangen, retningen og æblet til deres startværdier
```

Og slet de tre gamle linjer (`snake_body = ...`, `direction = ...`,
`next_direction = ...`) øverst i filen — de bor nu udelukkende inde i
`reset()`. Bemærk `game_over = False` på listen — det er en helt ny
variabel, som resten af dette dokument handler om.

*Bemærk:* Vi har valgt navnet `reset()` og ikke `init()`, selvom det er
nøjagtig samme mønster som `GL.init()`. Det er med vilje — `snake_game.py`
kalder allerede `pygame.init()` **og** `GL.init()`. Endnu en funktion, der
også hedder `init()`, ville hurtigt blive forvirrende at holde styr på, når
I læser koden. Navnet på en funktion må gerne fortælle, hvad den gør *i sin
egen sammenhæng* — her handler det om at nulstille slangen, altså
`reset()`.

## Trin — Fra et tvetydigt Boolean til en rigtig tilstand

Kig på `move_snake()`, som den ser ud nu:

```python
def move_snake(cols, rows):
    global snake_body, direction
    direction = next_direction

    if pygame.time.get_ticks() - apple_ticks >= GL.APPLE_TIMEOUT:
        place_apple()

    head_x, head_y = snake_body[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    new_x, new_y = new_head

    inside_board = 1 <= new_x <= cols - 2 and 2 <= new_y <= rows - 1
    if not inside_board:
        return False  # ramte muren - og den spiste heller ikke noget

    ate_apple = new_head == apple_pos
    ...
    return ate_apple
```

Kommentaren på `return False` afslører faktisk et problem, der allerede
har luret i koden siden uge 1: `move_snake()` returnerer `False` i to helt
forskellige situationer — når slangen **rammer muren**, og når den bare
**bevæger sig uden at spise**. `snake_game.py` kan ikke se forskel:

```python
ate_apple = move_snake(GL.BOARD_COLUMNS, GL.BOARD_ROWS)
if ate_apple:
    score += 10
```

`if ate_apple:` er `False` i begge tilfælde — hovedprogrammet har med
andre ord **ingen måde** at vide, om slangen lige er død. Et enkelt
Boolean var nok, dengang det kun skulle fortælle "blev der spist et æble
eller ej?" — men nu skal vi holde styr på **to** ting samtidig: blev der
spist noget, *og* er spillet slut? Det klarer vi ikke med kun én
returværdi. Løsningen er at gemme "er spillet slut?" som sin egen,
navngivne tilstand — akkurat som `snake_body` og `direction` allerede er
tilstand, `snake.py` selv ejer og holder styr på:

```python
game_over = False

def is_game_over():
    return game_over
```

*Tænk over:* Hvorfor er der en hel funktion, `is_game_over()`, og ikke
bare et `from snake import game_over` i `snake_game.py`, ligesom I kunne
finde på at gøre? Prøv at huske, hvordan Python fungerer: `from x import y`
kopierer værdien af `y`, **på det tidspunkt import-linjen køres** — én gang,
ved opstart. Ændrer `snake.py` bagefter sin egen `game_over`-variabel (fra
`False` til `True`, inde i `move_snake()`), opdager `snake_game.py`
**ikke** noget som helst — den sidder stadig med sin gamle kopi, `False`,
resten af spillet. Det er præcis samme faldgrube, som er grunden til, at
`snake_game.py` heller aldrig importerer `snake_body` eller `direction`
direkte — den henter dem altid gennem et **funktionskald**
(`draw_snake(screen)`), som slår den friskeste værdi op, hver gang den
kaldes. `is_game_over()` gør det samme: hvert kald slår `game_over` op
**lige nu**, inde i `snake.py`, i stedet for at læse en gammel kopi.

Nu kan vi koble mur-kollisionen til den nye tilstand:

```python
def move_snake(cols, rows):
    global snake_body, direction, game_over
    direction = next_direction

    if pygame.time.get_ticks() - apple_ticks >= GL.APPLE_TIMEOUT:
        place_apple()

    head_x, head_y = snake_body[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    new_x, new_y = new_head

    inside_board = 1 <= new_x <= cols - 2 and 2 <= new_y <= rows - 1
    if not inside_board:
        game_over = True
        return False

    ate_apple = new_head == apple_pos

    if ate_apple:
        snake_body = [new_head] + snake_body
        place_apple()
    else:
        snake_body = [new_head] + snake_body[:-1]

    return ate_apple
```

Og i `snake_game.py` skal I importere `is_game_over` og `reset` sammen med
de andre funktioner:

```python
from snake import draw_snake, move_snake, change_direction, draw_apple, place_apple, is_game_over, reset
```

og bruge `is_game_over()` til at holde slangen stille, så snart spillet er
slut — hvis `move_snake()` ikke bliver kaldt mere, kan slangen jo ikke
bevæge sig videre ind i muren eller sig selv:

```python
if event.type == SNAKE_MOVE and not is_game_over():
    ate_apple = move_snake(GL.BOARD_COLUMNS, GL.BOARD_ROWS)
    if ate_apple:
        score += 10
```

Prøv spillet nu: kør lige ind i muren. Slangen fryser på stedet, i stedet
for at fortsætte ud gennem kanten. Det er halvdelen af denne uges opgave —
resten er jeres.

---

## Uge 4 — Kollision og Game Over

**Mål for ugen:**
- Slangen dør også, hvis den rammer sin egen krop (ikke kun muren)
- Spilleren kan **se** tydeligt på skærmen, at spillet er slut
- (Bonus) Spilleren kan starte forfra, uden at genstarte selve programmet

### Opgave 1 — Slangen rammer sig selv

Lige nu opdager `move_snake()` kun kollision med muren. Byg videre på
samme funktion, så den **også** sætter `game_over = True`, hvis slangens
nye hoved rammer et felt, som resten af kroppen allerede optager.

*Tip 1:* I har allerede al den information, I skal bruge: `new_head` (det
felt, hovedet er på vej ind på) og `snake_body` (listen over alle
felter, kroppen optager lige nu, **før** den flytter sig). `in`-operatoren
kan bruges til at tjekke, om et felt findes i en liste — akkurat som
`place_apple()` allerede gør det, med `(x, y) not in snake_body`.

*Tip 2:* Sæt tjekket ind samme sted som mur-tjekket, altså **før** I
regner `ate_apple` ud og flytter slangen — ellers tjekker I mod
`snake_body`, efter den allerede er ændret, og det giver et forkert svar.

*Tænk over:* Prøv først den simpleste udgave, `new_head in snake_body`, og
kør spillet. Sving slangen i en tæt cirkel, uden at spise nogen æbler.
Oplever I, at spillet erklærer Game Over, selvom slangens hoved reelt
**ikke** rammer noget? Hvorfor sker det — hvilket felt i `snake_body`
er det, hovedet "rammer"? (Tænk på, hvad der sker med halen, `[:-1]`, i
samme øjeblik hovedet flytter sig derhen.) Ret jeres tjek, så det tager
højde for det — I skal kun sammenligne med de felter, kroppen **stadig**
vil optage, efter slangen er flyttet.

### Opgave 2 — Vis "GAME OVER" på skærmen, med samme bogstaver som scoren

Når `is_game_over()` er sand, skal spilleren kunne se det, ikke bare
gætte det ud fra, at slangen står stille. "GAME OVER" skal se ud, som om
det hører til samme HUD som scoren — altså tegnet med de samme
PNG-billeder pr. bogstav, som `draw_hud_img()` allerede bruger, ikke
pygames indbyggede skrifttype.

*Tip 1:* Kig på `font_img` i `hud.py`. Den kender i forvejen `S`, `C`,
`O`, `R`, `E`, `:` og cifrene — nok til "SCORE 000", men ikke nok til
"GAME OVER". Tjek `Resources/font/Individual/`: de bogstaver, I mangler
(`G`, `A`, `M`, `V`) findes allerede der, som `Upper_G.png`, `Upper_A.png`
osv. — helt samme navngivning som de bogstaver, der allerede er i
`font_img`. Udvid opslagsbogen med dem.

*Tip 2:* Skriv en ny funktion, fx `draw_game_over_img(screen)`, efter
nøjagtig samme opskrift som `draw_hud_img()`:

```python
def draw_hud_img(screen, score):
    ...
    for idx, i in enumerate(text):
        if i == ' ':
            continue
        img = pygame.image.load(Path(font_img[i])).convert_alpha()
        img = pygame.transform.scale(img, FIXED_SIZE)
        screen.blit(img, ((idx + 1) * 20, 2))
```

Løkken, der slår hvert bogstav op i `font_img` og tegner det, kan
genbruges nærmest uændret — det, der skal ændre sig, er **hvor** på
skærmen den begynder at tegne. `draw_hud_img()` starter altid ved
`x = 20` (`(idx + 1) * 20`) og `y = 2`, fast i øverste venstre hjørne.
"GAME OVER" skal derimod stå **centreret**, midt på spillepladen.

*Tip 3:* Hvert bogstav fylder `FIXED_SIZE[0]` (20) pixels i bredden. Kender
I teksten på forhånd (`"GAME OVER"`, 9 tegn inkl. mellemrummet), kender I
også dens samlede bredde: `len(text) * FIXED_SIZE[0]`. For at centrere et
stykke, der er så bredt, i et vindue, der er `screen.get_width()` bredt,
skal det starte ved `(screen.get_width() - samlet_bredde) // 2` i stedet
for et fast tal som `20`. Samme tankegang gælder lodret, med
`screen.get_height()` og `FIXED_SIZE[1]`.

*Tip 4:* Husk at kalde jeres nye funktion fra `snake_game.py`s hovedløkke
— men kun når spillet faktisk er slut, ellers vil "GAME OVER" stå og
blinke midt på brættet under hele spillet.

### Opgave 3 (bonus) — Start forfra

Lige nu er spillet permanent slut, når man dør — eneste udvej er at lukke
og starte programmet igen. Gør det muligt at prøve igen med et tastetryk,
uden at genstarte selve programmet.

*Tip 1:* I har allerede byttet på ærmet: `reset()` i `snake.py` nulstiller
netop slangen, retningen og æblet. Den er skrevet, netop så I kan kalde
den igen, når som helst — ikke kun ved opstart.

*Tip 2:* I hovedløkken, dér hvor I allerede tjekker `pygame.KEYDOWN`, kan
I tilføje endnu et tjek: hvis spillet er slut (`is_game_over()`), og en
bestemt tast trykkes (fx mellemrum), skal I kalde `reset()` **og** selv
huske at nulstille `score` tilbage til `0` — `reset()` bor jo i
`snake.py` og ved intet om `score`, som er `snake_game.py`s eget ansvar
(husk tommelfingerreglen fra uge 3: hver fil nulstiller kun den tilstand,
den selv ejer).

---

## Kommende uger (planlagt)

- **Uge 5** — Vi sætter nu et antal forhindringer op, når spillet
  starter. Disse forhindringer kan placeres på samme sted, hver gang.
  Eller de kan placeres tilfældigt (random).

*(Denne liste opdateres løbende, efterhånden som vi bliver enige om det
præcise indhold for hver uge.)*
