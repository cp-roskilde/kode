import pygame

BOARD_COLUMNS = 24
BOARD_ROWS = 16
CELL_SIZE = 32
GFX = "Resources/gfx/"

def load(filnavn):
    billede = pygame.image.load(GFX + filnavn)
    return pygame.transform.scale(billede, (CELL_SIZE, CELL_SIZE))

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
    "topleft":      load("body_topleft.png"),
    "topright":     load("body_topright.png"),
    "bottomleft":   load("body_bottomleft.png"),
    "bottomright":  load("body_bottomright.png"),
}

snake_body = [(12, 8), (11, 8), (10, 8)]
direction = (1, 0)   # slangen starter med at bevæge sig mod højre

def change_direction(new_direction):
    global direction
    opposite = (-direction[0], -direction[1])
    if new_direction != opposite:
        direction = new_direction

def move_snake(cols, rows):
    global snake_body
    head_x, head_y = snake_body[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    new_x, new_y = new_head

    inside_board = 1 <= new_x <= cols - 2 and 2 <= new_y <= rows - 1
    if not inside_board:
        return  # ramte muren - lad slangen stå stille i stedet

    snake_body = [new_head] + snake_body[:-1]

# Uge 2, Opgave 1 - Runde hjørner
def edge_towards(from_pos, to_pos):
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]
    if dx == 1:  return "right"
    if dx == -1: return "left"
    if dy == 1:  return "bottom"
    if dy == -1: return "top"

corner_images = {
    frozenset({"top", "left"}):     load("body_topleft.png"),
    frozenset({"top", "right"}):    load("body_topright.png"),
    frozenset({"bottom", "left"}):  load("body_bottomleft.png"),
    frozenset({"bottom", "right"}): load("body_bottomright.png"),
}

def draw_snake(screen):
    for index, segment in enumerate(snake_body):
        x, y = segment
        pixel_pos = (x * CELL_SIZE, y * CELL_SIZE)

        if index == 0:
            screen.blit(head_images[direction], pixel_pos)

        elif index == len(snake_body) - 1:
            prev_x, prev_y = snake_body[index - 1]
            tail_direction = (x - prev_x, y - prev_y)
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
    (CELL_SIZE, CELL_SIZE)
)

def draw_apple(screen):
    screen.blit(apple_image, (18 * CELL_SIZE, 4 * CELL_SIZE))
