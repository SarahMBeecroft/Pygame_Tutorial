import pygame
import os
import time
import random
# Initializes font
pygame.font.init()

# Sets width and height, and creates window variable 
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and Icon
pygame.display.set_caption("Space Shooter")
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
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# Laser class
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel # Moves lasers up

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

# Ship class, enemy and player ships will care this abstract class
class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        # Stores ships x and y coordinates
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    # Draws ship onto window   
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        # Draws lasers
        for laser in self.lasers:
            laser.draw(window)
    # Method to move lasers (enemy)
    def move_lasers(self, vel, obj):
        self.cooldown() # Checks for cooldown to see if player can shoot
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser) # Removes laser if off screen
            elif laser.collision(obj):
                obj.health -= 10 # Takes 10 off of player health
                self.lasers.remove(laser) # Removes laser

    # Cooldown counter, if cooldown counter is 0, don't do anything, otherwise increment by 1
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
 
    # Method to shoot lasers, cool down counter starts at zero
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

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

    # Method to move lasers
    def move_lasers(self, vel, objs):
        self.cooldown() # Checks for cooldown to see if player can shoot
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser) # Removes laser if off screen
            else:
                for obj in objs:
                    if laser.collision(obj): # If laser collides with object, remove it
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

# Enemy class initialization with super constructor
class Enemy(Ship):
    # Color dictionary to map colors to ships
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    # Method to move ship
    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

# Collide method, given two masks (obj1 and ob2), if they're overlapping based on offset, return true
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# Main game function
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("ariel", 50)
    lost_font = pygame.font.SysFont("ariel", 60)

    # Stores enemies and initializes starting wave length and velocity 
    enemies = []
    wave_length = 5
    enemy_vel = 1

    # Player moves 5 pixels every key press
    player_vel = 5
    laser_vel = 5

    player = Player(300, 630)

    # Clock object
    clock = pygame.time.Clock()

    # Sets lost to false at beginning of game
    lost = False
    lost_count = 0

    def redraw_window():
        # Refreshes the display with updated images at location defined (x-axis: 0, y-axis: 0)
        WIN.blit(BG, (0,0))
        # Draws text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
          
        # Puts text onto screen with blit
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        
        # Inherits from ship's draw method and draws enemy onto screen
        for enemy in enemies:
            enemy.draw(WIN)

        # Draws ship onto window
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("GIT GUD SCRUB", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        # Ensure game runs at clock speed of set FPS
        clock.tick(FPS)
        redraw_window()

        # If statement to determine if player loses and prevents negative lives 
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3: # Display losing message
                run = False # Quits game
            else:
                continue # Redraw window and keep running
        # Once wave of enemies is defeated, increment level
        if len(enemies) == 0:
            level += 1
            wave_length += 5 # Adds 5 more enemies each wave
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy) # Appends to enemy list

        for event in pygame.event.get():
            # Game will stop running when window is closed
            if event.type == pygame.QUIT:
                quit()
    
        # Returns a dictionary of all keys and tells you what keys are being pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Movies enemies from enemies list
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont("ariel", 70)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()