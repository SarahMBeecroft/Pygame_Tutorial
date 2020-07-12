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
#
playerX_change = 0

# Player function
def player(x, y):
  # blit method draws image of player onto screen, along with x and y coordinates 
  screen.blit(playerImg, (x, y))


# Game loop, infinite loop that makes sure game is always running
running = True
while running:

  # Sets color of game background with RGB
  screen.fill((55,4,185))

  # Prevents game from hanging
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    # Keystroke event to move player, checks to see if right or left
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        print('Left arrow is pressed')
      if event.key == pygame.K_RIGHT:
        print('Right arrow is pressed')
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        print('Keystroke has been released')

  # Calls player function 
  player(playerX, playerY)

  # Updates game display 
  pygame.display.update()