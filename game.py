import pygame
import os
import time
import random
# Initializes font
pygame.font.init()


# Sets width and height, and creates window variable 
WIDTH, HEIGHT = 850, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(os.path.join("assets", "spaceship.png"))
pygame.display.set_icon(icon)

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background, scaled to width and height
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "spacebackground.jpg")), (WIDTH, HEIGHT))

# Game function 
def main():
  run = True
  FPS = 60 
  level = 1
  lives = 3
  main_font = pygame.font.SysFont("ariel", 50)
  # Clock object
  clock = pygame.time.Clock()

  def redraw_window():
    # Refreshes the display with updated images at location defined (x-axis: 0, y-axis: 0)
    WIN.blit(BACKGROUND, (0,0))
    # Draws text
    lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
    level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

    # Puts text onto screen with blit
    WIN.blit(lives_label, (10, 10))
    WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
    

    pygame.display.update()

  while run:
    # Ensure game runs at clock speed of set FPS
    clock.tick(FPS)
    redraw_window()

    for event in pygame.event.get():
      # Game will stop running when window is closed 
      if event.type == pygame.QUIT:
        run = False

main()

