import pygame
import random
import globals as GL
from board import is_wall

GFX = "Resources/gfx/"

game_over = False

def is_game_over():
    return game_over

# Uge 6, bonus - Getters for AI
def get_snake_body():
    return snake_body

def get_direction():
    return direction

def get_apple_pos():
    return apple_pos

def load(filnavn):
    billede = pygame.image.load(GFX + filnavn)
    return pygame.transform.scale(billede, (GL.CELL_SIZE, GL.CELL_SIZE))

head_images = {
    (1, 0):  load("head_right.png"),
    (-1, 0): load("head_left.png"),
    (0, 1):  load("head_down.png"),
    (0, -1): load("head_up.png"),
}

tail_images = {
    (1, 0):  load("tail_right.png"),
    (-1, 0): load("tail_left.png"),
    (0, 1):  load("tail_down.png"),
    (0, -1): load("tail_up.png"),
}

body_images = {
    "horizontal":   load("body_horizontal.png"),
    "vertical":     load("body_vertical.png"),
}

def change_direction(new_direction):
    global next_direction
    opposite = (-direction[0], -direction[1])
    if new_direction != opposite:
        next_direction = new_direction

def move_snake(cols, rows):
    global snake_body, direction, game_over
    direction = next_direction

    # Uge 3, Opgave 2 - Tjek timeout for æble. Hvis tiden er gået, placér nyt æble
    if pygame.time.get_ticks() - apple_ticks >= GL.APPLE_TIMEOUT:
        place_apple()

    # Uge 6, bonus - Refactoring for AI
    new_head = next_position(snake_body[0], direction)

    if is_deadly(new_head):
        game_over = True
        return False
    
    ate_apple = new_head == apple_pos

    if ate_apple:
        # Uge 3, Opgave 1 - Slangen vokser, når den spiser æblerne
        snake_body = [new_head] + snake_body
        place_apple()
    else:
        snake_body = [new_head] + snake_body[:-1]

    return ate_apple

# Uge 6, Bonus - Hvor ender hovedet, hvis det tager ét skridt i retning 'd'?
def next_position(pos, d):
    x = (pos[0] + d[0]) % GL.BOARD_COLUMNS          # 24 -> 0, -1 -> 23
    y = (pos[1] + d[1] - 1) % GL.BOARD_ROWS + 1     # 17 -> 1,  0 -> 16
    return (x, y)

# Uge 6, Bonus - Dør slangen, hvis hovedet havner på feltet 'pos'?
def is_deadly(pos):
    x, y = pos
    return pos in snake_body[:-1] or is_wall(x, y)

# Uge 5, Opgave 2 - Sikre at slanges felter behandles rigtigt.
def step(d):
    if d > 1:
        return -1
    if d < -1:
        return 1
    return d

# Uge 2, Opgave 1 - Runde hjørner
def edge_towards(from_pos, to_pos):
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]
    if step(dx) == 1:  return "right" # Uge 5, Opgave 2 - Brug hjælpefunktion til at bestemme slangens placering.
    if step(dx) == -1: return "left"
    if step(dy) == 1:  return "bottom"
    if step(dy) == -1: return "top"

corner_images = {
    frozenset({"top", "left"}):     load("body_topleft.png"),
    frozenset({"top", "right"}):    load("body_topright.png"),
    frozenset({"bottom", "left"}):  load("body_bottomleft.png"),
    frozenset({"bottom", "right"}): load("body_bottomright.png"),
}

def draw_snake(screen):
    for index, segment in enumerate(snake_body):
        x, y = segment
        pixel_pos = (x * GL.CELL_SIZE, y * GL.CELL_SIZE)

        if index == 0:
            screen.blit(head_images[direction], pixel_pos)

        elif index == len(snake_body) - 1:
            prev_x, prev_y = snake_body[index - 1]
            tail_direction = (step(x - prev_x), step(y - prev_y)) # Uge 5, Opgave 2 - Placering af halen.
            screen.blit(tail_images[tail_direction], pixel_pos)

        else:
            prev_pos = snake_body[index - 1]
            next_pos = snake_body[index + 1]
            edge_to_prev = edge_towards(segment, prev_pos)
            edge_to_next = edge_towards(segment, next_pos)
            edges = {edge_to_prev, edge_to_next}

            if edges == {"left", "right"}:
                screen.blit(body_images["horizontal"], pixel_pos)
            elif edges == {"top", "bottom"}:
                screen.blit(body_images["vertical"], pixel_pos)
            else:
                screen.blit(corner_images[frozenset(edges)], pixel_pos)

# Uge 2, Opgave 2 - Tegn æblet
apple_image = pygame.transform.scale(
    pygame.image.load("Resources/gfx/apple.png"),
    (GL.CELL_SIZE, GL.CELL_SIZE)
)

def draw_apple(screen):
    x, y = apple_pos
    screen.blit(apple_image, (x * GL.CELL_SIZE, y * GL.CELL_SIZE))

apple_pos = (0, 0)  # midlertidig værdi - erstattes med det samme af place_apple()
apple_ticks = 0  # Uge 3, Opgave 2 - variabel til tid

def place_apple():
    global apple_pos, apple_ticks
    apple_ticks = pygame.time.get_ticks()  # Uge 3, Opgave 2 - Gem tid for æble placering

    while True:
        x = random.randint(1, GL.BOARD_COLUMNS - 2)
        y = random.randint(2, GL.BOARD_ROWS - 1)
        if (x, y) not in snake_body and not is_wall(x, y):
            apple_pos = (x, y)
            return

def reset():
    global snake_body, direction, next_direction, game_over
    snake_body = [(12, 8), (11, 8), (10, 8)]
    direction = (1, 0)
    next_direction = (1, 0)
    game_over = False
    place_apple()

# place_apple()  # kald funktionen med det samme, så der er et æble fra start
reset()