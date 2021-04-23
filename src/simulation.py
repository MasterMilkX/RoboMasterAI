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

b_robot1 = Robot(1,3,23, 0, m, [pt(3,3),pt(3,23)], pixels+1, (0,0,255),"player")
b_robot2 = Robot(2,3,3, 0, m, [pt(3,3),pt(3,23)], pixels+1, (0,0,255),"ai")
r_robot1 = Robot(1,43,3, 0, m, [pt(43,3),pt(43,23)], pixels+1, (255,0,0),"ai")
r_robot2 = Robot(2,43,23, 0, m, [pt(43,3),pt(43,23)], pixels+1, (255,0,0),"ai")

all_robots = [b_robot1, b_robot2, r_robot1, r_robot2]
#all_robots = [b_robot1,r_robot1]
red_robots = [r_robot1,r_robot2]
blue_robots = [b_robot1,b_robot2]



#################        UI        ###################



def create_button(x, y, text, color, callback, active=False):
    """A button is a dictionary that contains the relevant data.

    Consists of a rect, text surface and text rect, color and a
    callback function.
    """
    # The button is a dictionary consisting of the rect, text,
    # text rect, color and the callback function.
    FONT = pygame.font.Font(None, 15)
    text_surf = FONT.render(text, True, (255,255,255))
    button_rect = pygame.Rect(x, y, 60, 30)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'active' : active,
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': color,
        'callback': callback,
        }
    return button

#sets the mode of the robot from the button press
def setRobotMode(rid, color, mode):
    rb = None
    if rid == 8:
        print('hmm')
        return
    if color == "red":
        rb = red_robots[rid-1]
    elif color == "blue":
        rb = blue_robots[rid-1]

    if rb == None:
        return

    print("Changing mode to [" + mode + "] for " +  color + " robot " + str(rid))
    rb.modeChange(mode)

#reset the colors of all of the buttons
def resetBtns(b):
    for s in btn_sets:
        #button in this set
        if b in s:
            for a in s:
                a['active'] = False
            b['active'] = True
            return



# make the buttons for the UI
robot_btns = []
btn_sets = []
if blue_robots[0].control != "player":
    bs = []
    b_btn1 = create_button(20, GAME_H+(3*20), "Random", (32,32,181),(lambda: setRobotMode(1, "blue", "random")),True)
    robot_btns.append(b_btn1)
    b_btn2 = create_button(90, GAME_H+(3*20), "Offense", (32,32,181),(lambda: setRobotMode(1, "blue", "offense")))
    robot_btns.append(b_btn2)
    b_btn3 = create_button(160, GAME_H+(3*20), "Defense", (32,32,181),(lambda: setRobotMode(1, "blue", "defense")))
    robot_btns.append(b_btn3)

    bs.append(b_btn1)
    bs.append(b_btn2)
    bs.append(b_btn3)
    btn_sets.append(bs)

if blue_robots[1].control != "player":
    bs = []
    b_btn1 = create_button(20, GAME_H+(7*20), "Random", (32,32,181),(lambda: setRobotMode(2, "blue", "random")),True)
    robot_btns.append(b_btn1)
    b_btn2 = create_button(90, GAME_H+(7*20), "Offense", (32,32,181),(lambda: setRobotMode(2, "blue", "offense")))
    robot_btns.append(b_btn2)
    b_btn3 = create_button(160, GAME_H+(7*20), "Defense", (32,32,181),(lambda: setRobotMode(2, "blue", "defense")))
    robot_btns.append(b_btn3)

    bs.append(b_btn1)
    bs.append(b_btn2)
    bs.append(b_btn3)
    btn_sets.append(bs)

if red_robots[0].control != 'player':
    rs = []
    r_btn1 = create_button(320, GAME_H+(3*20), "Random", (181,32,32),(lambda: setRobotMode(1, "red", "random")),True)
    robot_btns.append(r_btn1)
    r_btn2 = create_button(390, GAME_H+(3*20), "Offense", (181,32,32),(lambda: setRobotMode(1, "red", "offense")))
    robot_btns.append(r_btn2)
    r_btn3 = create_button(460, GAME_H+(3*20), "Defense", (181,32,32),(lambda: setRobotMode(1, "red", "defense")))
    robot_btns.append(r_btn3)

    rs.append(r_btn1)
    rs.append(r_btn2)
    rs.append(r_btn3)
    btn_sets.append(rs)

if red_robots[1].control != 'player':
    rs = []
    r_btn1 = create_button(320, GAME_H+(7*20), "Random", (181,32,32),(lambda: setRobotMode(2, "red", "random")),True)
    robot_btns.append(r_btn1)
    r_btn2 = create_button(390, GAME_H+(7*20), "Offense", (181,32,32),(lambda: setRobotMode(2, "red", "offense")))
    robot_btns.append(r_btn2)
    r_btn3 = create_button(460, GAME_H+(7*20), "Defense", (181,32,32),(lambda: setRobotMode(2, "red", "defense")))
    robot_btns.append(r_btn3)

    rs.append(r_btn1)
    rs.append(r_btn2)
    rs.append(r_btn3)
    btn_sets.append(rs)



###################       RENDERS       ###################


#draw everything
def render():
    drawGame()
    drawStats()

    for btn in robot_btns:
        draw_button(btn,screen)

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

    font = pygame.font.SysFont(None, 20)        #set font

    h = 1
    for b in blue_robots:
        bluetxt = font.render('Blue ' + str(b.id) + ': ' + str((b.x,b.y)) + " @ " + str(b.rot) + " [" + str(b.hp) + " / " + str(b.maxhp) + "]", True, (0,0,255)) 
        screen.blit(bluetxt, (20, GAME_H+(h*20)))
        h+=4

    h = 1
    for r in red_robots:
        redtext = font.render('Red ' + str(r.id) + ': ' + str((r.x,r.y)) + " @ " + str(r.rot) + " [" + str(r.hp) + " / " + str(r.maxhp) + "]", True, (255,0,0))
        screen.blit(redtext, (320, GAME_H+(h*20)))
        h+=4

#make the robot mode buttons 
def draw_button(button, screen):
    c = (180,180,180)
    if button['active']:
        c = button['color']

    """Draw the button rect and the text surface."""
    pygame.draw.rect(screen, c, button['rect'])
    screen.blit(button['text'], button['text rect'])



###############        MAIN GAME LOOP        ####################


# Run until the user asks to quit
running = True
tick = 0
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # on click function for buttons
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in robot_btns:
                    if button['rect'].collidepoint(event.pos):
                        button['callback']()
                        resetBtns(button)

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
                r.gotoTarget()
                

    #draw the screen
    render()

    clock.tick(30)
    

# Done! Time to quit.
pygame.quit()