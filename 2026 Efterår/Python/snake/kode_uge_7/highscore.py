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

def remove_letter():
    entry = highscores[edit_row]
    entry['name'][:-1] = '-'

def confirm_name():
    global edit_row
    if len(highscores[edit_row]["name"]) < 3:
        return                                # alle tre bogstaver skal være skrevet
    edit_row = None                           # nu er linjen låst
    save_highscores()

def get_best_score():
    if not get_highscores():
        return None
    else:
        return highscores[0]['score']
    
load_highscores()