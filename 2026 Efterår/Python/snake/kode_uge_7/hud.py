import pygame
pygame.init()
from pathlib import Path

import globals as GL
from highscore import get_highscores, get_edit_row, is_editing, get_best_score

font = pygame.font.SysFont("couriernew", 28) 

sprite_sheet = 'Resources/font/sheet.png'

def draw_text_img(screen, text, size, y):
    center_x = (screen.get_width() - (len(text) * size[0])) // 2
    center_y = (screen.get_height() - size[1]) // 2

    for idx, i in enumerate(text):
        if i == ' ':
            continue
        img = pygame.image.load(Path(GL.font_img[i])).convert_alpha()
        img = pygame.transform.scale(img, size)
        screen.blit(img, (center_x + idx * size[0], center_y + y))

def draw_hud_text(screen, score, hi):
    score = max(0, min(score, 999))  # clamp to 0-999
    if hi != None:
        if score > hi:
            hi = score
    else:
        hi = 0
    
    text = f" SCORE {score:03d}   HI {hi:03d}"            # zero-pad to 3 digits, e.g. 0 -> "000", 42 -> "042"
    rendered = font.render(text, True, (255, 255, 255))
    screen.blit(rendered, (0, 0))

def draw_hud_img(screen, score, hi):
    score = max(0, min(score, 999))  # clamp to 0-999
    if hi != None:
        if score > hi:
            hi = score
    else:
        hi = 0
    
    text = f" SCORE {score:03d}   HI {hi:03d}"            # zero-pad to 3 digits, e.g. 0 -> "000", 42 -> "042"

    hud_area = (0, 0, screen.get_width(), GL.FIXED_SIZE[1])
    screen.fill((0, 0, 0), hud_area)  # ryd HUD-rækken, før vi tegner de nye cifre

    for idx, i in enumerate(text):
        if i == ' ':
            continue
        img = pygame.image.load(Path(GL.font_img[i])).convert_alpha()
        img = pygame.transform.scale(img, GL.FIXED_SIZE)
        screen.blit(img, ((idx + 1) * 20, 2))

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