import math
import random
import pygame

WIDTH = 500
HEIGHT = 500

def main():
  pygame.init()

  screen = pygame.display.set_mode((WIDTH, HEIGHT))

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    do_stuff()
    draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

  pygame.quit()

def do_stuff_none():
  print("Doing stuff")

def draw_house(screen):
  color_black = (0, 0, 0)
  color_yellow = (255, 255, 0)
  color_red = (255, 0, 0)
  color_blue = (0, 0, 255)
  color_green = (0, 255, 0)

  screen.fill((0,0,0))
  
  jord_y = 400
  hus_start_x = 100
  hus_slut_x = 400
  hus_top_y = 200
  hus_tag_top_y = 100
  hus_tag_extra = 20
  vindue_start_x = 150
  vindue_top_y = 250
  vindue_size = 75
  door_start_x = 275
  door_top_y = 250
  door_width = 75
  door_height = 150

  pygame.draw.rect(screen, color_green, (0, jord_y, WIDTH, HEIGHT - jord_y))
  pygame.draw.rect(screen, color_red, (hus_start_x, hus_top_y, hus_slut_x - hus_start_x, jord_y - hus_top_y))
  pygame.draw.rect(screen, color_blue, (vindue_start_x, vindue_top_y, vindue_size, vindue_size))
  pygame.draw.rect(screen, color_blue, (door_start_x, door_top_y, door_width, door_height))
  
  punkter = []
  punkter.append((hus_start_x-hus_tag_extra, hus_top_y))
  punkter.append(((hus_start_x+hus_slut_x)//2, hus_tag_top_y))
  punkter.append((hus_slut_x+hus_tag_extra, hus_top_y))
  pygame.draw.polygon(screen, (255, 255, 0), punkter)

class point:
  def __init__(self):
    self.x = random.randrange(0, WIDTH)
    self.y = random.randrange(0, HEIGHT)
    self.dx = random.randrange(-10, 10)
    self.dy = random.randrange(-10, 10)
    self.color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))

  def move(self):
    self.x += self.dx
    self.y += self.dy
    if self.x < 0 or self.x > WIDTH:
      self.dx = -self.dx
    if self.y < 0 or self.y > HEIGHT:
      self.dy = -self.dy

  def draw(self, screen):
    pygame.draw.circle(screen, self.color, (self.x, self.y), 5)

points = [point() for _ in range(10)]

def draw_animate(screen):
  screen.fill((0,0,0))
  for point in points: point.draw(screen)

def do_stuff_animate():
  for point in points: point.move()

# draw = draw_house
# do_stuff = do_stuff_none
draw = draw_animate
do_stuff = do_stuff_animate


if __name__ == "__main__":  main()