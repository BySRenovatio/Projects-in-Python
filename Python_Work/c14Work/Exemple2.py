""" 
 Move a sprite in a circle.
  
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
"""
 
import pygame
import random
import math
 
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
 
 
class Block(pygame.sprite.Sprite):
    """ This class represents the ball that moves in a circle. """
 
    # The "center" the sprite will orbit
    center_x = 0
    center_y = 0
 
    # Current angle in radians
    angle = 0
     
    # How far away from the center to orbit, in pixels
    radius = 0
     
    # How fast to orbit, in radians per frame
    speed = 0.05
     
    def __init__(self, color, width, height):
        """ Constructor that create's the ball's image. """
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
         
    def update(self):
        """ Update the ball's position. """
        # Calculate a new x, y
        self.rect.x = self.radius * math.sin(self.angle) + self.center_x
        self.rect.y = self.radius * math.cos(self.angle) + self.center_y
         
        # Increase the angle in prep for the next round.
        self.angle += self.speed
 
class Player(pygame.sprite.Sprite):
    """ Class to represent the player. """
    def __init__(self, color, width, height):
        """ Create the player image. """
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
         
    def update(self):
        """Set the user to be where the mouse is. """
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
         
# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])
 
# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()
 
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
 
for i in range(50):
    # This represents a block
    block = Block(black, 20, 15)
 
    # Set a random center location for the block to orbit
    block.center_x = random.randrange(screen_width)
    block.center_y = random.randrange(screen_height)
    # Random radius from 10 to 200
    block.radius = random.randrange(10, 200)
    # Random start angle from 0 to 2pi
    block.angle = random.random() * 2 * math.pi
    # radians per frame
    block.speed = 0.008
    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)
 
# Create a red player block
player = Player(red, 20, 15)
all_sprites_list.add(player)
 
#Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
score = 0
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
 
    all_sprites_list.update()
            
    # Clear the screen
    screen.fill(white)
     
    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)  
     
    # Check the list of collisions.
    for block in blocks_hit_list:
        score += 1
        print( score )
     
    # Draw all the spites
    all_sprites_list.draw(screen)
     
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)
 
pygame.quit()