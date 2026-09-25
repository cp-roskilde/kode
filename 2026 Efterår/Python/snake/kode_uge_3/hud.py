import pygame
pygame.init()
from pathlib import Path

font = pygame.font.SysFont("couriernew", 28) 

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

sprite_sheet = 'Resources/font/sheet.png'
FIXED_SIZE = (20, 32)  # (width, height) in pixels

def draw_hud_text(screen, score):
    score = max(0, min(score, 999))  # clamp to 0-999
    text = f" SCORE {score:03d}"            # zero-pad to 3 digits, e.g. 0 -> "000", 42 -> "042"
    rendered = font.render(text, True, (255, 255, 255))
    screen.blit(rendered, (0, 0))

def draw_hud_img(screen, score):
    score = max(0, min(score, 999))  # clamp to 0-999
    text = f"SCORE {score:03d}"            # zero-pad to 3 digits, e.g. 0 -> "000", 42 -> "042"

    hud_area = (0, 0, screen.get_width(), FIXED_SIZE[1])
    screen.fill((0, 0, 0), hud_area)  # ryd HUD-rækken, før vi tegner de nye cifre

    for idx, i in enumerate(text):
        if i == ' ':
            continue
        img = pygame.image.load(Path(font_img[i])).convert_alpha()
        img = pygame.transform.scale(img, FIXED_SIZE)
        screen.blit(img, ((idx + 1) * 20, 2))

def draw_hud_sheet(screen, score):
    sheet = pygame.image.load(Path(sprite_sheet))

    score = max(0, min(score, 999))  # clamp to 0-999
    text = f"SCORE {score:03d}"            # zero-pad to 3 digits, e.g. 0 -> "000", 42 -> "042"
    for i in text:
        if i == ' ':
            continue
        
        img = pygame.transform.scale(img, FIXED_SIZE)
        screen.blit(img, ((idx + 1) * 32, 2))
