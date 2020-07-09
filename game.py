import pygame

# Initializes the pygame
pygame.init()

# Creates the game screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Game loop, infinite loop that makes sure game is always running
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
