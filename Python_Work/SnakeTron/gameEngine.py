'''
Created on Mar 29, 2014
@author: BYSorynyos
'''

import pygame
import operator
import random
from math import fabs

# Initialize the game engine
pygame.init()

# Points variable
points = 0

# Bonus position
bonus = (100, 100)

# Game speed = 20
SPEED = 20

# Game resolution
MAX_X = 800
MAX_Y = 600

# Starting position + current_pos
start_pos = (MAX_X/2, MAX_Y/2)
current_pos = start_pos

# Snake movement vector
snake_move = []

# key bindings
move_map = [(-3, 0), (3, 0), (0, -3), (0, 3)]
move_map_k =[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN] 

# Define last key pressed initial value
last_key = 2

# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Open a max resolution window
size = (MAX_X, MAX_Y)
screen = pygame.display.set_mode(size)

# Put caption on window
pygame.display.set_caption(" SnakeTron game ")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Main loop
done = False

# Add the starting postion to the movement vector
snake_move.append(start_pos)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    # Determine the movement vector of the keyboard
    pressed = pygame.key.get_pressed()
    
    # Check in sw if keys were pressed
    # Update the position depending on the keys pressed, memorize last_movement
    # Add the new movements to the movement vector
    sw = 0
    i = 0    
    for key in move_map_k:
        if pressed[key] == 1:
            current_pos = tuple(map(operator.add, current_pos, move_map[i])) 
            snake_move.append(current_pos)
            last_key = i
            sw = 1
        i += 1
    
    # No keys pressed -> continue movement        
    if sw == 0:
        current_pos = tuple(map(operator.add, current_pos, move_map[last_key])) 
        snake_move.append(current_pos)
    
    # If out of bounds [0] - x / [1] - y    
    if current_pos[0] > MAX_X or current_pos[0] < 0:
        done = True
    if current_pos[1] > MAX_Y or current_pos[1] < 0:
        done = True
        
    # Contact with the snake body
    for elements in range(len(snake_move)-1):
        if current_pos == snake_move[elements]:
            done = True
            
    # If bonus exists check if tuched else create new
    if fabs(bonus[0] - current_pos[0]) <= 8 and fabs(bonus[1] - current_pos[1]) <= 8:
        del snake_move[0:(len(snake_move)/2)]
        points += 1000
        SPEED += 2
        aux = (random.randrange(MAX_X - 100) + 50, random.randrange(MAX_Y - 100) + 50)
        bonus = aux
    else:
        points += 1
            
    # Clear screen
    screen.fill(BLACK)
    
    # Draw the snake
    for elements in snake_move:
        pygame.draw.circle(screen, RED, elements, 2, 2)     
    
    # Draw the bonus 
        pygame.draw.circle(screen, BLUE, bonus, 7, 7)
    
    # Draw the score + speed
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Points = " + str(points) + " Speed = " + str(SPEED), 1, WHITE)
    screen.blit(label, (0, 0))        
        
    # Show everything on screen
    pygame.display.flip()
    
    # Limit to the speed frames per second
    clock.tick(SPEED)

# Put the score on the screen
screen.fill(WHITE)
myfont = pygame.font.SysFont("monospace", 30)
label = myfont.render("Points = " + str(points) + " Speed = " + str(SPEED), 1, BLACK)
screen.blit(label, (50, 100))

scores = []
f = open('highscores.txt', 'r')
for i in range(5):
    scores.append(f.readline())
f.close()

# Print scores
for i in range(5):
    myfont = pygame.font.SysFont("monospace", 20)
    label = myfont.render(scores[i], 1, BLACK)
    screen.blit(label, (50, i*50 + 150))
pygame.display.flip()

for i in range(5):
    aux = int(scores[i])
    if aux < points:
        j = 4
        while j > i:
            scores[j] = scores[j-1]
            j -= 1
        scores[i] = str(points) + '\n'
        points = -1
    
f = open('highscores.txt', 'w')
for i in range(5):
    f.write(scores[i])
f.close()

done = False
while not done:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

# Quit the program
pygame.quit()
    