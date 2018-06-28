'''
Created on Mar 28, 2014
@author: BYSorynyos
'''

# Import a library of functions called 'pygame'
import pygame
import math
from math import pi

# Initialize the game engine
pygame.init()

# Define colors in RGB
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Open a 700/500 window 
size = (700, 500)
screen = pygame.display.set_mode(size)

# Put caption on widow
pygame.display.set_caption(" First Game ")

#Loop until the user clicks the close button.
done = False
  
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
  
# -------- Main Program Loop -----------
while not done:
    
    for event in pygame.event.get():                    # User did something
        if event.type == pygame.QUIT:                   # If user clicked close
            done = True                                 # Flag that we are done so we exit this loop
    
    # Clear the screen -> white
    screen.fill(WHITE)
    
    # Draw a line
    pygame.draw.rect(screen, GREEN, [50,50,100,100])
    pygame.draw.line(screen, GREEN, [0,0], [100,100], 5)
    
    # Draw on the screen several lines from (0,10) to (100,110) 
    # 5 pixels wide using a while loop
    y_offset = 0
    while y_offset < 100:
        pygame.draw.line(screen, RED, [0,10+y_offset], [100,110+y_offset], 5)
        y_offset = y_offset + 10
    
    # Random drawings - cool    
    for i in range(200):
        radians_x = i * 2
        radians_y = i * 3
        x = int(75 * math.sin(radians_x)) + 200
        y = int(75 * math.cos(radians_y)) + 200
        pygame.draw.line(screen, RED, [x,y], [x+5,y], 5)
    
    # Crosses
    for x_offset in range(30,300,30):
        pygame.draw.line(screen,BLACK,[x_offset,100],[x_offset-10,90], 2 )
        pygame.draw.line(screen,BLACK,[x_offset,90],[x_offset-10,100], 2 )
        
    # Draw a rectangle
    pygame.draw.rect(screen,BLACK,[20,20,250,100],2)
    
    # Draw an arc as part of an ellipse. Use radians to determine what
    # angle to draw.
    pygame.draw.arc(screen,GREEN,[100,100,250,200],  pi/2,     pi, 2)
    pygame.draw.arc(screen,BLACK,[100,100,250,200],     0,   pi/2, 2)
    pygame.draw.arc(screen,RED,  [100,100,250,200],3*pi/2,   2*pi, 2)
    pygame.draw.arc(screen,BLUE, [100,100,250,200],    pi, 3*pi/2, 2)
    
    # This draws a triangle using the polygon command
    pygame.draw.polygon(screen,BLACK,[[100,100],[0,200],[200,200]],5)
    
    # Select the font to use. Default font, 25 pt size.
    font = pygame.font.Font(None, 25)
 
    # Render the text. "True" means anti-aliased text. 
    # Black is the color. The variable BLACK was defined
    # above as a list of [0,0,0]
    # Note: This line creates an image of the letters, 
    # but does not put it on the screen yet.
    text = font.render("My text",True,BLACK)
 
    # Put the image of the text on the screen at 250x250
    screen.blit(text, [250,250])
    
    # Display everything
    pygame.display.flip()
    
    # Limit to 20 frames per second
    clock.tick(20)

# Quit the program
pygame.quit()