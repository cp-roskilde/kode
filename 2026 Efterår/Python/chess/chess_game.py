import pygame
pygame.init()

import globals as GL
GL.init()

from board import draw_board
import pieces

GAME_BOARD = []
WIDTH = GL.BOARD_COLUMNS * GL.CELL_SIZE
HEIGHT = GL.BOARD_ROWS * GL.CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT + GL.CELL_SIZE))
pygame.display.set_caption("Coding Pirates CHESS")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        # Luk spillet        
        if event.type == pygame.QUIT:
            running = False

    draw_board(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()