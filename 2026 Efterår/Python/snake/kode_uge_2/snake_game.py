import pygame
pygame.init()

from hud import draw_hud_img
from snake import draw_snake, move_snake, change_direction, draw_apple

GAME_BOARD = []
CELL_SIZE = 32
BOARD_ROWS = 16
BOARD_COLUMNS = 24

WIDTH = BOARD_COLUMNS * CELL_SIZE
HEIGHT = BOARD_ROWS * CELL_SIZE

score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT + CELL_SIZE))
pygame.display.set_caption("Snake")

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

wall_image = pygame.transform.scale(
    pygame.image.load("Resources/gfx/wall.png"),
    (CELL_SIZE, CELL_SIZE)
)

def draw_wall():
    # Venstre og højre mur
    for y in range(1, BOARD_ROWS + 1):
        screen.blit(wall_image, (0, y * CELL_SIZE))
        screen.blit(wall_image, ((BOARD_COLUMNS - 1) * CELL_SIZE, y * CELL_SIZE))

    # Top og bund
    for x in range(BOARD_COLUMNS):
        screen.blit(wall_image, (x * CELL_SIZE, 1 * CELL_SIZE))
        screen.blit(wall_image, (x * CELL_SIZE, BOARD_ROWS * CELL_SIZE))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        # Luk spillet        
        if event.type == pygame.QUIT:
            running = False

        if event.type == SNAKE_MOVE:
            move_snake(BOARD_COLUMNS, BOARD_ROWS)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                change_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                change_direction((1, 0))

    draw_hud_img(screen, score)
    draw_grass()
    draw_wall()
    draw_apple(screen)
    draw_snake(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()