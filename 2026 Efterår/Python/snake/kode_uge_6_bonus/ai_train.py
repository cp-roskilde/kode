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
