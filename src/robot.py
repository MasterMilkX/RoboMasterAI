import numpy as np
import pygame

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

#x, y coordinate points
class pt():
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Robot(pygame.sprite.Sprite):
	def __init__(self, x,y, rot, arena, sqr_pix, color):
		super(Robot, self).__init__()
		self.px = sqr_pix
		self.color = color
		self.robotDim = pt(4,4)

		self.arena = arena
		self.collisions = [1,2]

		self.x = x
		self.y = y
		self.rot = 0
		
		self.surf = pygame.Surface((self.robotDim.x*sqr_pix, self.robotDim.y*sqr_pix))		#take up 4x4 pixel space
		self.surf.fill(color)
		self.rect = self.surf.get_rect()

	# Move the sprite based on user keypresses
	def keypress(self, pressed_keys):
		if pressed_keys[K_UP]:
			self.move("up")
		if pressed_keys[K_DOWN]:
			self.move("down")
		if pressed_keys[K_LEFT]:
			self.move("left")
		if pressed_keys[K_RIGHT]:
			self.move("right")

	#move 1 tile in a specific direction
	def move(self,direction):
		if not self.canMove(direction):
			return

		if direction == "up":
			self.y-=1
		elif direction == "down":
			self.y+=1
		if direction == "left":
			self.x-=1
		elif direction == "right":
			self.x+=1

	#returns the bounding box location for the robot
	def getRobotBox(self,pos=None):
		#default
		if(pos == None):
			pos = pt(self.x, self.y)

		box = []
		for h in range(self.robotDim.y):
			b = []
			for w in range(self.robotDim.x):
				nx = pos.x+w
				ny = pos.y+h
				#out of bounds
				if((ny < 0) or (ny >= len(self.arena)) or (nx < 0) or (nx >= len(self.arena[0]))):
					return None

				#add tile at placement
				b.append(self.arena[ny][nx])
			box.append(b)

		return box



	#check if can move in direction
	def canMove(self, direction):
		#get bounding area with offset
		pos = pt(self.x,self.y)
		if direction == "up":
			pos.y-=1
		elif direction == "down":
			pos.y+=1
		if direction == "left":
			pos.x-=1
		elif direction == "right":
			pos.x+=1

		box = self.getRobotBox(pos)

		#out of bounds
		if box == None:
			return False

		#just get the values and check if any colliable parts
		box = np.array(box).flatten()
		for c in self.collisions:
			if str(c) in box:
				return False
		return True




		
	


