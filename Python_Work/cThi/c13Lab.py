""" 
 Show how to use a sprite backed by a graphic.
  
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/vRB_983kUMc
"""
 
import pygame
import random
 
# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
 
class Rectangle():
    # Methods
    def __init__(self):
        self.h = -1
        self.w = -1
        self.x = -1
        self.y = -1
        self.change_x = -1
        self.change_y = -1
        self.color = (0, 0, 0)
        
    def drawer(self, screen):
        box = pygame.Rect(self.x, self.y, self.h, self.w)
        pygame.draw.rect(screen, self.color, box, 0)
        
    def move_object(self):
        self.x += self.change_x
        self.y += self.change_y

class Ellipse(Rectangle):
    def drawer(self, screen):
        box = pygame.Rect(self.x, self.y, self.h, self.w)
        pygame.draw.ellipse(screen, self.color, box, 0)
         
 
pygame.init()
  
# Set the width and height of the screen [width, height]
size = (800, 600)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
#Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

myList = []

# Create a new object / rectangle 

for i in range(500):
    myObject = Rectangle()
    myObject.x = random.randrange(0,801)
    myObject.y = random.randrange(0,601)
    myObject.w = random.randrange(20,71)
    myObject.h = random.randrange(20,71)
    myObject.change_x = random.randrange(-3,4)
    myObject.change_y = random.randrange(-3,4)
    r = random.randrange(0,255)
    g = random.randrange(0,255)
    b = random.randrange(0,255)
    tup = (r, g, b)
    myObject.color = tup
    myList.append(myObject)

for i in range(500):
    myObject = Ellipse()
    myObject.x = random.randrange(0,801)
    myObject.y = random.randrange(0,601)
    myObject.w = random.randrange(20,71)
    myObject.h = random.randrange(20,71)
    myObject.change_x = random.randrange(-3,4)
    myObject.change_y = random.randrange(-3,4)
    r = random.randrange(0,255)
    g = random.randrange(0,255)
    b = random.randrange(0,255)
    tup = (r, g, b)
    myObject.color = tup
    myList.append(myObject)
 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
  
    # --- Game logic should go here
    for i in range(1000):
        obj = myList[i]
        obj.move_object()
    
    # --- Drawing code should go here
     
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    
    for i in range(1000):
        myList[i].drawer(screen)
         
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
     
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()