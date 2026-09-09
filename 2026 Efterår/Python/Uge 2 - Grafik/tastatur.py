import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spil")

# Spiller
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed_x = 0
player_speed_y = 0
player_speed = 2

player_size = 10

player_color = (0,200,0)
background_color = (0, 0, 0)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        # Luk spillet        
        if event.type == pygame.QUIT:
            running = False

        # Tastatur
        if event.type==pygame.KEYDOWN and event.key == pygame.K_LEFT:
            player_speed_x -= player_speed
        if event.type==pygame.KEYUP and event.key == pygame.K_LEFT:
            player_speed_x += player_speed
            
        if event.type==pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            player_speed_x += player_speed
        if event.type==pygame.KEYUP and event.key == pygame.K_RIGHT:
            player_speed_x -= player_speed
            
        if event.type==pygame.KEYDOWN and event.key == pygame.K_UP:
            player_speed_y -= player_speed
        if event.type==pygame.KEYUP and event.key == pygame.K_UP:
            player_speed_y += player_speed

        if event.type==pygame.KEYDOWN and event.key == pygame.K_DOWN:
            player_speed_y += player_speed
        if event.type==pygame.KEYUP and event.key == pygame.K_DOWN:
            player_speed_y -= player_speed

    # Handlinger
    player_x = player_x + player_speed_x
    player_y = player_y + player_speed_y
    
    # Tegn
    screen.fill(background_color)

    pygame.draw.circle(
        screen,
        player_color,
        (player_x, player_y),
        player_size
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()