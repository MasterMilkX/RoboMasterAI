import csv
from robot import Robot, pt
from arena_builder import make_arena_polygon

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

#set up boundaries for visilibity
arena_poly = make_arena_polygon()

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

NUM_ROBOTS = 4

b_robot1 = Robot(1,3,23, 0, m, [pt(3,3),pt(3,23)], pixels+1, (0,0,255),"player")
b_robot2 = Robot(2,3,3, 0, m, [pt(3,3),pt(3,23)], pixels+1, (0,0,255),"ai")
r_robot1 = Robot(1,43,3, 0, m, [pt(43,3),pt(43,23)], pixels+1, (255,0,0),"ai")
r_robot2 = Robot(2,43,23, 0, m, [pt(43,3),pt(43,23)], pixels+1, (255,0,0),"ai")


all_robots = []
red_robots = []
blue_robots = []


all_robots.append(b_robot1)
blue_robots.append(b_robot1)

if(NUM_ROBOTS >= 2):
    all_robots.append(r_robot1)
    red_robots.append(r_robot1)
if(NUM_ROBOTS >= 3):
    all_robots.append(b_robot2)
    blue_robots.append(b_robot2)
if(NUM_ROBOTS == 4):
    all_robots.append(r_robot2)
    red_robots.append(r_robot2)




all_robots = [b_robot1, b_robot2, r_robot1, r_robot2]
#all_robots = [b_robot1,r_robot1]
red_robots = [r_robot1,r_robot2]
blue_robots = [b_robot1,b_robot2]



#################        UI        ###################



def create_button(x, y, text, color, callback, active=False, w=60, h=30):
    """A button is a dictionary that contains the relevant data.

    Consists of a rect, text surface and text rect, color and a
    callback function.
    """
    # The button is a dictionary consisting of the rect, text,
    # text rect, color and the callback function.
    FONT = pygame.font.Font(None, 15)
    text_surf = FONT.render(text, True, (255,255,255))
    button_rect = pygame.Rect(x, y, w, h)
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
cam_btns = []
if blue_robots[0].control != "player":
    bs = []
    b_btn1 = create_button(20, GAME_H+(2*20), "Random", (32,32,181),(lambda: setRobotMode(1, "blue", "random")),True)
    robot_btns.append(b_btn1)
    b_btn2 = create_button(90, GAME_H+(2*20), "Offense", (32,32,181),(lambda: setRobotMode(1, "blue", "offense")))
    robot_btns.append(b_btn2)
    b_btn3 = create_button(160, GAME_H+(2*20), "Defense", (32,32,181),(lambda: setRobotMode(1, "blue", "defense")))
    robot_btns.append(b_btn3)

    bs.append(b_btn1)
    bs.append(b_btn2)
    bs.append(b_btn3)
    btn_sets.append(bs)

if b_robot1 in blue_robots:
    cam1 = create_button(100, GAME_H+(4*20), 'Camera', (180,122,191), (lambda: toggleRobotCam(1,"blue")),True, 45, 15)
    cam_btns.append(cam1)

if blue_robots[1].control != "player":
    bs = []
    b_btn1 = create_button(20, GAME_H+(6*20), "Random", (32,32,181),(lambda: setRobotMode(2, "blue", "random")),True)
    robot_btns.append(b_btn1)
    b_btn2 = create_button(90, GAME_H+(6*20), "Offense", (32,32,181),(lambda: setRobotMode(2, "blue", "offense")))
    robot_btns.append(b_btn2)
    b_btn3 = create_button(160, GAME_H+(6*20), "Defense", (32,32,181),(lambda: setRobotMode(2, "blue", "defense")))
    robot_btns.append(b_btn3)

    bs.append(b_btn1)
    bs.append(b_btn2)
    bs.append(b_btn3)
    btn_sets.append(bs)

if b_robot2 in blue_robots:
    cam2 = create_button(100, GAME_H+(8*20), 'Camera', (180,122,191), (lambda: toggleRobotCam(2,"blue")),True, 45, 15)
    cam_btns.append(cam2)

if red_robots[0].control != 'player':
    rs = []
    r_btn1 = create_button(320, GAME_H+(2*20), "Random", (181,32,32),(lambda: setRobotMode(1, "red", "random")),True)
    robot_btns.append(r_btn1)
    r_btn2 = create_button(390, GAME_H+(2*20), "Offense", (181,32,32),(lambda: setRobotMode(1, "red", "offense")))
    robot_btns.append(r_btn2)
    r_btn3 = create_button(460, GAME_H+(2*20), "Defense", (181,32,32),(lambda: setRobotMode(1, "red", "defense")))
    robot_btns.append(r_btn3)

    rs.append(r_btn1)
    rs.append(r_btn2)
    rs.append(r_btn3)
    btn_sets.append(rs)

if r_robot1 in red_robots:
    cam3 = create_button(400, GAME_H+(4*20), 'Camera', (180,122,191), (lambda: toggleRobotCam(1,"red")),True, 45, 15)
    cam_btns.append(cam3)

if red_robots[1].control != 'player':
    rs = []
    r_btn1 = create_button(320, GAME_H+(6*20), "Random", (181,32,32),(lambda: setRobotMode(2, "red", "random")),True)
    robot_btns.append(r_btn1)
    r_btn2 = create_button(390, GAME_H+(6*20), "Offense", (181,32,32),(lambda: setRobotMode(2, "red", "offense")))
    robot_btns.append(r_btn2)
    r_btn3 = create_button(460, GAME_H+(6*20), "Defense", (181,32,32),(lambda: setRobotMode(2, "red", "defense")))
    robot_btns.append(r_btn3)

    rs.append(r_btn1)
    rs.append(r_btn2)
    rs.append(r_btn3)
    btn_sets.append(rs)

if r_robot2 in red_robots:
    cam4 = create_button(400, GAME_H+(8*20), 'Camera', (180,122,191), (lambda: toggleRobotCam(2,"red")),True, 45, 15)
    cam_btns.append(cam4)



#camera toggle button
def toggleAllCams():
    FONT = pygame.font.Font(None, 15)
    camTogg['active'] = not camTogg['active']
    if(camTogg['active']):
        camTogg['text'] = FONT.render("Hide Cams", True, (255,255,255))
    else:
        camTogg['text'] = FONT.render("Show Cams", True, (0,0,0))

    for r in all_robots:
        r.showCam = camTogg['active']

#toggle individual robot cams
def toggleRobotCam(rid, color):
    rb = None
    if color == "red":
        rb = red_robots[rid-1]
    elif color == "blue":
        rb = blue_robots[rid-1]

    if rb == None:
        return

    rb.showCam = not rb.showCam


camTogg = create_button(240,GAME_H+(75), "Show Cams", (135,37,147), toggleAllCams,True)

###################       RENDERS       ###################


#draw everything
def render():
    drawGame()
    drawStats()

    for btn in robot_btns:
        draw_button(btn,screen)

    for btn in cam_btns:
        draw_button(btn,screen)

    draw_button(camTogg,screen)


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

    #draw all the camera viewports of the robots
    for r in all_robots:
        if not r.showCam:
            continue

        pts = []
        cx = (r.x*(pixels+1) + (r.robotDim.x/2)*(pixels+1))
        cy = (r.y*(pixels+1) + (r.robotDim.y/2)*(pixels+1))

        for p in range(len(r.camPts)):
            s = (r.camPts[p][0]+cx,r.camPts[p][1]+cy)
            e = (r.camPts[0][0]+cx,r.camPts[0][1]+cy)
            if p < len(r.camPts)-1:
                e = (r.camPts[p+1][0]+cx,r.camPts[p+1][1]+cy)
            pygame.draw.line(screen, r.camColor, s,e,1)
            #pts.append((p[0]+cx,p[1]+cy))
            




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

                for button in cam_btns:
                    if button['rect'].collidepoint(event.pos):
                        button['callback']()

                if camTogg['rect'].collidepoint(event.pos):
                    camTogg['callback']()

    #update ticks
    tick += 1

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    #perform every 5 ticks
    if tick % (5) == 0:

        #move player controlled robots
        for r in all_robots:
            if r.control == "player":
                r.keypress(pressed_keys)
            elif r.control == "ai":
                r.gotoTarget()

            #update location
            if r.mode != "random":
                r.envUpdate(arena_poly)


    #check cameras for robot detection 
    if tick % 10 == 0:
        for r in all_robots:
            if r.color == "blue":
                r.findThreat(red_robots)
            else:
                r.findThreat(blue_robots)




    #draw the screen
    render()

    clock.tick(30)
    

# Done! Time to quit.
pygame.quit()