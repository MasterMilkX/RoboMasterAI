import csv
from robot import Robot, pt

import random
import numpy as np

# Import and initialize the pygame library
import pygame
pygame.init()

scale = 1
px = 10
pixels = px*scale     #size of pixels relative to the game arena
COLORS = [(93,96,106),(44,44,44),(139,137,142),(192,43,33),(181,147,72),(23,36,158)]       #med grey, dark grey, light grey, red, yellow, blue 

#import game map
m = list(csv.reader(open('arena1.csv')))

# Set up the drawing window
GAME_W = (len(m[0])*px)*scale+50
GAME_H = (len(m)*px)*scale+30
STATS_H = 200
screen = pygame.display.set_mode([GAME_W, GAME_H+STATS_H])
clock = pygame.time.Clock()

#print(GAME_W)
#print(GAME_H)


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

b_robot1 = Robot(3,23, 0, m, pixels+1, (0,0,255),"player")
b_robot2 = Robot(3,3, 0, m, pixels+1, (0,0,255),"ai")
r_robot1 = Robot(43,3, 0, m, pixels+1, (255,0,0),"ai")
r_robot2 = Robot(43,23, 0, m, pixels+1, (255,0,0),"ai")

#all_robots = [b_robot1, b_robot2, r_robot1, r_robot2]
all_robots = [b_robot1,r_robot1]
red_robots = [r_robot1,r_robot2]
blue_robots = [b_robot1,b_robot2]

#draw everything
def render():
    drawGame()
    drawStats()

    # Flip the display
    pygame.display.flip()


#drawing screen for the game
def drawGame():
    # Fill the background with dark gray
    screen.fill((50, 50, 50))

    #fill grid for the arena map
    for y in range(len(m)):
        for x in range(len(m[0])):
            color = COLORS[int(m[y][x])]
            rect = pygame.Rect(x*(pixels+1), y*(pixels+1), pixels, pixels)
            pygame.draw.rect(screen, color, rect)


    #draw the robots on screen
    for r in all_robots:
        screen.blit(r.surf, (r.x*(pixels+1),r.y*(pixels+1)))


# draw the stats at the bottom of the screen
def drawStats():
    # Fill the bottom part of the screen with black
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0,GAME_H,GAME_W,STATS_H))

    font = pygame.font.SysFont(None, 24)        #set font

    h = 1
    for b in blue_robots:
        bluetxt = font.render('Blue Robot ' + str(h) + ': ' + str((b.x,b.y)) + " @ " + str(b.rot), True, (0,0,255))
        screen.blit(bluetxt, (20, GAME_H+(h*20)))
        h+=1

    h = 1
    for r in red_robots:
        redtext = font.render('Red Robot ' + str(h) + ': ' + str((r.x,r.y)) + " @ " + str(r.rot), True, (255,0,0))
        screen.blit(redtext, (320, GAME_H+(h*20)))
        h+=1

#pick random empty spot on the map
def randArenaPos():
    s = []
    for r in range(len(m)):
        for c in range(len(m[0])):
            if m[r][c] not in [1,2]:
                s.append([c,r])
    return random.choice(s)

#choose random starting position location
def randBasePos():
    return random.choice([[3,3],[43,3],[43,23],[3,23]])


###############        MAIN GAME LOOP        ####################


# Run until the user asks to quit
running = True
tick = 0
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update ticks
    tick += 1

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    #perform every tick
    if tick % (5) == 0:

        #move player controlled robots
        for r in all_robots:
            if r.control == "player":
                r.keypress(pressed_keys)
            elif r.control == "ai":
                if r.target == None:
                    #t = randPos()
                    t = randArenaPos();
                    r.target = pt(t[0],t[1])

                r.gotoTarget()
                

    #draw the screen
    render()

    clock.tick(30)
    

# Done! Time to quit.
pygame.quit()