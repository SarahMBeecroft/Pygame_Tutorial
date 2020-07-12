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

# Ship class, enemy and player ships will care this abstract class
class Ship: 
  def __init__(self, x, y, health=100):
      # Stores ships x and y coordinates
      self.x = x
      self.y = y
      self.health =  health
      self.ship_img = None
      self.laser_img = None
      self.lasers = []
      self.cool_down_counter = 0
  # Draws ship onto window
  def draw(self, window):
    window.blit(self.ship_img, (self.x, self.y))

  # Gets player ship width
  def get_width(self):
    return self.ship_img.get_width()

  # Gets player ship height 
  def get_height(self):
    return self.ship_img.get_height()

# Player class initialization with super constructor
class Player(Ship):
  def __init__(self, x, y, health=100):
    super().__init__(x, y, health)
    self.ship_img = YELLOW_SPACE_SHIP
    self.laser_img = YELLOW_LASER
    # Mask tells you where pixels are (lets you do pixel perfect collision)
    self.mask = pygame.mask.from_surface(self.ship_img)
    self.max_health = health # Health bar

# Enemy class initialization with super constructor
class Enemy(Ship):
  # Color dictionary to map colors to ships
  COLOR_MAP = {
              "red": (RED_SPACE_SHIP, RED_LASER)
              "green": (GREEN_SPACE_SHIP, GREEN_LASER)
              "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
              }

  def __init__(self, x, y, color, health=100):
    super().__init__(x, y, health)
    self.ship_img, self.laser_img = self.COLOR_MAP[color]
    self.mask = pygame.mask.from_surface(self.ship_img) 

  # Method to move ship
  def move(self, vel):
    self.y += vel # Moves down only


# Game function 
def main():
  run = True
  FPS = 60 
  level = 1
  lives = 3
  main_font = pygame.font.SysFont("ariel", 50)
  # Player moves 5 pixels every key press
  player_vel = 5

  player = Player(300, 650)

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

    # Draws ship onto window 
    player.draw(WIN)
    

    pygame.display.update()

  while run:
    # Ensure game runs at clock speed of set FPS
    clock.tick(FPS)
    redraw_window()

    for event in pygame.event.get():
      # Game will stop running when window is closed 
      if event.type == pygame.QUIT:
        run = False

    # Returns a dictionary of all keys and tells you what keys are being pressed
    keys = pygame.key.get_pressed() 
    
    if keys[pygame.K_a] and player.x - player_vel > 0: #left
      player.x -= player_vel
    if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: #right
      player.x += player_vel
      print('key was pressed')
    if keys[pygame.K_w] and player.y - player_vel > 0: #upw
      player.y -= player_vel
    if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 10 < HEIGHT: #down
      player.y += player_vel

main()

