import pygame
pygame.init()

import globals as GL
GL.init()

from hud import draw_hud_img, draw_text_img, draw_highscores
from snake import draw_snake, move_snake, change_direction, draw_apple, place_apple, is_game_over, reset
from board import draw_wall, is_wall, draw_obstacles, place_obstacles
from highscore import get_best_score, remove_letter

import ai
from highscore import is_highscore, insert_score, is_editing, add_letter, confirm_name

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

clock = pygame.time.Clock()
running = True

# Uge 6, Bonus - Hvilken "skærm" er vi på? "menu", "player" eller "ai"
game_mode = "menu"

def start_game(mode):
    global game_mode, score
    game_mode = mode
    score = 0
    place_obstacles()
    reset()


while running:
    for event in pygame.event.get():
        # Luk spillet        
        if event.type == pygame.QUIT:
            running = False

        if event.type == SNAKE_MOVE and game_mode in ("player", "ai") and not is_game_over():
            if game_mode == "ai":
                # AI'en "trykker på tasterne" lige før slangen flytter sig
                action = ai.choose_action(ai.get_state())
                change_direction(ai.action_to_direction(action))
            ate_apple = move_snake(GL.BOARD_COLUMNS, GL.BOARD_ROWS)
            if ate_apple:
                score += 10

            # Uge 7 - Kom spilleren på highscore-listen? (AI'en må ikke komme på listen)
            if is_game_over() and game_mode == "player" and is_highscore(score):
                insert_score(score)
                game_mode = "highscore"

        if event.type == pygame.KEYDOWN:
            # Uge 7 - Highscore-skærmen: skriv initialer, eller gå tilbage til menuen
            if game_mode == "highscore":
                if is_editing():
                    if event.key == pygame.K_RETURN:
                        confirm_name()
                    else:
                        add_letter(event.unicode)
                elif event.key == pygame.K_ESCAPE:
                    game_mode = "menu"
                continue  # på highscore-skærmen styrer piletasterne ingenting

            if game_mode == "menu":
                if event.key == pygame.K_1:
                    start_game("player")
                elif event.key == pygame.K_2:
                    ai.load_brain()
                    start_game("ai")
                elif event.key == pygame.K_3:
                    game_mode = "highscore"
                continue  # i menuen styrer piletasterne ingenting

            if game_mode == "highscore":
                if event.key == pygame.K_BACKSPACE:
                    remove_letter()
                    
            if event.key == pygame.K_ESCAPE:
                game_mode = "menu"
            elif event.key == pygame.K_SPACE and is_game_over():
                start_game(game_mode)

            match event.key:
                case pygame.K_UP | pygame.K_w:
                    change_direction((0, -1))
                case pygame.K_DOWN | pygame.K_s:
                    change_direction((0, 1))
                case pygame.K_LEFT | pygame.K_a:
                    change_direction((-1, 0))
                case pygame.K_RIGHT | pygame.K_d:
                    change_direction((1, 0))

    draw_hud_img(screen, score, get_best_score())
    draw_grass()
    draw_wall(screen)

    if game_mode == "menu":
        draw_text_img(screen, "SNAKE", GL.LARGE_SIZE, -100)
        draw_text_img(screen, "1. PLAY SNAKE", GL.FIXED_SIZE, 0)
        draw_text_img(screen, "2. AI PLAYS SNAKE", GL.FIXED_SIZE, 50)
        draw_text_img(screen, "3. HIGHSCORE", GL.FIXED_SIZE, 100)
    elif game_mode == "highscore":
        draw_highscores(screen)
    else:
        draw_obstacles(screen)
        draw_apple(screen)
        draw_snake(screen)

        if is_game_over():
            draw_text_img(screen, "GAME OVER", GL.LARGE_SIZE, 0)
            draw_text_img(screen, "PRESS <SPACE> TO START NEW GAME", GL.FIXED_SIZE, 0 + GL.LARGE_SIZE[1] + 10)
            draw_text_img(screen, "PRESS <ESC> FOR MENU", GL.FIXED_SIZE, 0 + GL.LARGE_SIZE[1] + 50)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()