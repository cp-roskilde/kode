import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spil")

class Circle:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.size = 0
        self.speed = speed

new_circle_chance = 0.0150
circles = []

circle_color = (200, 100, 50)
background_color = (30, 30, 30)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        # Luk spillet        
        if event.type == pygame.QUIT:
            running = False

        # Mus
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            point = pygame.Vector2(event.pos)
            for circle in list(circles):
                circleCenter = pygame.Vector2(circle.x,circle.y)
                distance = circleCenter.distance_to(point)
                if distance<circle.size:
                    circles.remove(circle)

    # Handlinger
    for circle in circles:
        circle.size += circle.speed

    if random.random()<=new_circle_chance and len(circles)<10:
        new_circle_x = random.randrange(WIDTH)
        new_circle_y = random.randrange(HEIGHT)
        new_circle_speed = random.random()

        circles.append(Circle(new_circle_x,new_circle_y,new_circle_speed))
    
    # Tegn
    screen.fill(background_color)

    for circle in circles:
        if circle.size < 25:
            circle_color = pygame.Color("yellow")
        elif circle.size > 25 and circle.size < 50:
            circle_color = pygame.Color("orange")
        elif circle.size > 50:
            circle_color = pygame.Color("red")
        pygame.draw.circle(
            screen,
            circle_color,
            (circle.x, circle.y),
            circle.size
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()