import pygame

# Initializes the pygame
pygame.init()

# Creates the game screen (width, height) or (x-axis, y-axis)
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('images/spaceship.png')
pygame.display.set_icon(icon)

# Player icon
playerImg = pygame.image.load('images/player.png')

# Where we are positioning player on x-axis 
playerX = 370

# Where we are positioning player on y-axis 
playerY = 480

# Player function
def player():
  # blit method draws image of player onto screen, along with x and y coordinates 
  screen.blit(playerImg, (playerX, playerY))


# Game loop, infinite loop that makes sure game is always running
running = True
while running:

  # Sets color of game background with RGB
  screen.fill((55,4,185))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Calls player function 
  player()

  # Updates game display 
  pygame.display.update()