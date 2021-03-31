import csv
from robot import Robot


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
screen = pygame.display.set_mode([GAME_W, GAME_H])
clock = pygame.time.Clock()


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

t_robot = Robot(2,20, 0, pixels+1, (0,255,0))


#drawing screen functionality
def draw():
    # Fill the background with black
    screen.fill((50, 50, 50))

    #fill grid
    for y in range(len(m)):
        for x in range(len(m[0])):
            color = COLORS[int(m[y][x])]
            rect = pygame.Rect(x*(pixels+1), y*(pixels+1), pixels, pixels)
            pygame.draw.rect(screen, color, rect)


    #draw the robot on screen
    screen.blit(t_robot.surf, (t_robot.x*(pixels+1),t_robot.y*(pixels+1)))


    # Flip the display
    pygame.display.flip()




tick = 0


# Run until the user asks to quit
running = True
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
    if tick % (pixels) == 0:
        t_robot.keypress(pressed_keys)

    #draw the screen
    draw()

    clock.tick(30)
    

# Done! Time to quit.
pygame.quit()