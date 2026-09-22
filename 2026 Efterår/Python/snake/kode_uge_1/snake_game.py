import pygame
pygame.init()

from hud import draw_hud_img

GAME_BOARD = []
CELL_SIZE = 32 
BOARD_ROWS = 16
BOARD_COLUMNS = 24

WIDTH = BOARD_COLUMNS * CELL_SIZE
HEIGHT = BOARD_ROWS * CELL_SIZE

score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT + CELL_SIZE))
pygame.display.set_caption("Snake")

def draw_grass_v0():
    rect_color = pygame.Color("green3")
    for x in range(BOARD_COLUMNS):
        for y in range(1, BOARD_ROWS + 1):
            grass = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, rect_color, grass)

def draw_grass():
    for x in range(BOARD_COLUMNS):
        for y in range(1, BOARD_ROWS + 1):
            # Vi tegner nu græsset. For at give det mere liv, skifter vi farve, for hver celle.
            if (x + y) % 2 == 0:
                rect_color = pygame.Color("green3")
            else:
                rect_color = pygame.Color("lawngreen")
            grass = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, rect_color, grass)

# Lav en helt ny slags "begivenhed" (event), som kun vi selv bruger
SNAKE_MOVE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_MOVE, 150)  # send begivenheden hvert 150. millisekund

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        # Luk spillet        
        if event.type == pygame.QUIT:
            running = False

    draw_hud_img(screen, score)
    draw_grass()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()