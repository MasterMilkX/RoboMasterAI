import csv


# Import and initialize the pygame library
import pygame
pygame.init()

scale = 1
pixels = 10*scale     #size of pixels relative to the game arena
COLORS = [(93,96,106),(44,44,44),(139,137,142),(192,43,33),(181,147,72),(23,36,158)]      

#import game map
m = list(csv.reader(open('arena1.csv')))

# Set up the drawing window
GAME_W = (len(m[0])*10)*scale+50
GAME_H = (len(m)*10)*scale+30
screen = pygame.display.set_mode([GAME_W, GAME_H])


# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Fill the background with black
    screen.fill((50, 50, 50))

    #fill grid
    for y in range(len(m)):
        for x in range(len(m[0])):
            color = COLORS[int(m[y][x])]
            rect = pygame.Rect(x*(pixels+1), y*(pixels+1), pixels, pixels)
            pygame.draw.rect(screen, color, rect)



    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()