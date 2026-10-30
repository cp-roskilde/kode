import pygame
pygame.init()
from pathlib import Path

import globals as GL

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

def draw_hud_text(screen, score):
    score = max(0, min(score, 999))  # clamp to 0-999
    text = f" SCORE {score:03d}"            # zero-pad to 3 digits, e.g. 0 -> "000", 42 -> "042"
    rendered = font.render(text, True, (255, 255, 255))
    screen.blit(rendered, (0, 0))

def draw_hud_img(screen, score):
    score = max(0, min(score, 999))  # clamp to 0-999
    text = f"SCORE {score:03d}"            # zero-pad to 3 digits, e.g. 0 -> "000", 42 -> "042"

    hud_area = (0, 0, screen.get_width(), GL.FIXED_SIZE[1])
    screen.fill((0, 0, 0), hud_area)  # ryd HUD-rækken, før vi tegner de nye cifre

    for idx, i in enumerate(text):
        if i == ' ':
            continue
        img = pygame.image.load(Path(GL.font_img[i])).convert_alpha()
        img = pygame.transform.scale(img, GL.FIXED_SIZE)
        screen.blit(img, ((idx + 1) * 20, 2))

