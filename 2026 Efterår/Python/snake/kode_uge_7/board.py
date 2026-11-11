import pygame
import random
import globals as GL

wall_image = pygame.transform.scale(
    pygame.image.load("Resources/gfx/wall.png"),
    (GL.CELL_SIZE, GL.CELL_SIZE)
)

# Åbningerne i muren - centreret, og ens i hver side
gap_start_x = (GL.BOARD_COLUMNS - GL.GAP_SIZE) // 2           # 10
gap_columns = range(gap_start_x, gap_start_x + GL.GAP_SIZE)   # 10, 11, 12, 13

gap_start_y = 1 + (GL.BOARD_ROWS - GL.GAP_SIZE) // 2          # 7 (muren starter i række 1)
gap_rows = range(gap_start_y, gap_start_y + GL.GAP_SIZE)      # 7, 8, 9, 10

# Uge 5, Opgave 3 - Forhindringer!
# obstacles = [(4, 4), (19, 4), (4, 13), (19, 13), (16, 5)]

# Uge 5, Opgave 4 (bonus) - Placér forhindring tilfældigt, hver gang spillet startes.
obstacles = [] # Vi laver en tom liste
def place_obstacles():
    global obstacles
    obstacles.clear() # Vi tømmer den tidligere liste, ved gameover
    for f in range(5): # Vi skal have 5 forhindringer
        # Vi tilføjer tilfældige (x, y) placeringer i vores 'obstacles' liste
        obstacles.append(((random.randint(1, GL.BOARD_COLUMNS - 2)),
                   random.randint(2, GL.BOARD_ROWS - 1)))
    
def is_wall(x, y):
    left_or_right = x == 0 or x == GL.BOARD_COLUMNS - 1
    top_or_bottom = y == 1 or y == GL.BOARD_ROWS

    # Uge 5, Opgave 3 - Tjek om vi rammer en forhindring.
    if (x, y) in obstacles:
        return True
    if left_or_right and y not in gap_rows:
        return True
    if top_or_bottom and x not in gap_columns:
        return True
    return False

def draw_wall(screen):
    for x in range(GL.BOARD_COLUMNS):
        for y in range(1, GL.BOARD_ROWS + 1):
            if is_wall(x, y):
                screen.blit(wall_image, (x * GL.CELL_SIZE, y * GL.CELL_SIZE))

def draw_obstacles(screen):
    if not obstacles:
        place_obstacles()
    for o in obstacles:
        screen.blit(wall_image, (o[0] * GL.CELL_SIZE, o[1] * GL.CELL_SIZE))