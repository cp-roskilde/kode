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
