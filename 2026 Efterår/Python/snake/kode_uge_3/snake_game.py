import pygame
pygame.init()

import globals as GL
GL.init()

from hud import draw_hud_img
from snake import draw_snake, move_snake, change_direction, draw_apple, place_apple

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

wall_image = pygame.transform.scale(
    pygame.image.load("Resources/gfx/wall.png"),
    (GL.CELL_SIZE, GL.CELL_SIZE)
)

def draw_wall():
    # Venstre og højre mur
    for y in range(1, GL.BOARD_ROWS + 1):
        screen.blit(wall_image, (0, y * GL.CELL_SIZE))
        screen.blit(wall_image, ((GL.BOARD_COLUMNS - 1) * GL.CELL_SIZE, y * GL.CELL_SIZE))

    # Top og bund
    for x in range(GL.BOARD_COLUMNS):
        screen.blit(wall_image, (x * GL.CELL_SIZE, 1 * GL.CELL_SIZE))
        screen.blit(wall_image, (x * GL.CELL_SIZE, GL.BOARD_ROWS * GL.CELL_SIZE))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        # Luk spillet        
        if event.type == pygame.QUIT:
            running = False

        if event.type == SNAKE_MOVE:
            ate_apple = move_snake(GL.BOARD_COLUMNS, GL.BOARD_ROWS)
            if ate_apple:
                score += 10

        if event.type == pygame.KEYDOWN:
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
    draw_wall()
    draw_apple(screen)
    draw_snake(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()