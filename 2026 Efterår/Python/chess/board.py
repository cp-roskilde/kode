import pygame
import globals as GL

def draw_board(screen):
    for x in range(GL.BOARD_COLUMNS):
        for y in range(1, GL.BOARD_ROWS + 1):
            # Vi tegner nu græsset. For at give det mere liv, skifter vi farve, for hver celle.
            if (x + y) % 2 == 0:
                rect_color = pygame.Color("green3")
            else:
                rect_color = pygame.Color("lawngreen")
            grass = pygame.Rect(x * GL.CELL_SIZE, y * GL.CELL_SIZE, GL.CELL_SIZE, GL.CELL_SIZE)
            pygame.draw.rect(screen, rect_color, grass)
