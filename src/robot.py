import numpy as np
import pygame
import math
import random

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

	def __eq__(self, other):
		if isinstance(other, pt):
			return self.x == other.x and self.y == other.y
		return False

	def __str__(self):
		return f"({self.x},{self.y})"

	#get distance between this point and another
	def dist(self,other):
		return math.sqrt(math.pow(other.x-self.x,2)+math.pow(other.y-self.y,2))


#x,y coordinate points with parents (for BFS)
class node():
	def __init__(self,pos,parent):
		self.pos = pos
		self.parent = parent

	def __str__(self):
		return pos + " > " + parent


class Robot(pygame.sprite.Sprite):
	def __init__(self, idno, x,y, rot, arena, bases, sqr_pix, color, control):
		super(Robot, self).__init__()
		self.px = sqr_pix
		self.color = color
		self.robotDim = pt(2,2)		#w,h of robot
		#self.robotDim = pt(1,1)		#w,h of robot

		self.control = control
		self.path = []
		self.target = None
		self.mode = "random"

		self.arena = arena
		self.collisions = [1,2]
		self.bases = bases			#just use starting position

		self.id = idno
		self.x = x
		self.y = y
		self.rot = 0
		self.hp = 2000
		self.maxhp = 2000
		
		self.surf = pygame.Surface((self.robotDim.x*sqr_pix, self.robotDim.y*sqr_pix))		#take up 4x4 pixel space
		self.surf.fill(color)
		self.rect = self.surf.get_rect()


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
	def canMove(self, directions, p=None):
		#create position
		if p == None:
			p = pt(self.x,self.y)
		pos = pt(p.x,p.y)

		#calculate relative position
		for direction in directions:
			if direction == "up":
				pos.y-=1
			elif direction == "down":
				pos.y+=1
			if direction == "left":
				pos.x-=1
			elif direction == "right":
				pos.x+=1

		#get bounding area with offset
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


	#converts a point location to a direction based on current location
	def pt2Dir(self,p,pos=None):
		#create position
		if pos == None:
			pos = pt(self.x,self.y)

		goto = []
		if(p.x > pos.x):
			goto.append("right")
		elif(p.x < pos.x):
			goto.append("left")

		if(p.y > pos.y):
			goto.append("down")
		elif(p.y < pos.y):
			goto.append("up")

		return goto

	#converts a set of directions to a point (relative)
	def dir2Pt(self,dirs,pos=None):
		#create position
		if pos == None:
			pos = pt(self.x,self.y)
		pos2 = pt(pos.x,pos.y)

		#calculate new position from the direction(s) given
		for d in dirs:
			if d == "up":
				pos2.y-=1
			elif d == "down":
				pos2.y+=1
			if d == "left":
				pos2.x-=1
			elif d == "right":
				pos2.x+=1

		return pos2


	#check if bounding box is at the position
	def atPos(self, target, pos=None):
		#create position
		if pos == None:
			pos = pt(self.x,self.y)

		for h in range(self.robotDim.y):
			for w in range(self.robotDim.x):
				nx = pos.x+w
				ny = pos.y+h

				p2 = pt(nx,ny)

				if p2 == target:
					return True
				

		return False





	#######  PLAYER CONTROL METHODS   #######


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
		if not self.canMove([direction]):
			return

		if direction == "up":
			self.y-=1
		elif direction == "down":
			self.y+=1
		if direction == "left":
			self.x-=1
		elif direction == "right":
			self.x+=1





	######      AI METHODS      #######


	#generates best first search path to a target point from the current location
	def bfsPath(self,t):
		startpos = node(pt(self.x,self.y),None)
		queue = []
		visited = []

		path = []
		dest = None

		queue.append(startpos)

		#breadth first search
		while len(queue) > 0 and dest == None:
			#print(len(queue))
			origin = queue.pop(0)
			pqueue = list(map(lambda x: x.pos, queue))

			if origin.pos in visited:
				continue

			visited.append(origin.pos)
			n = self.getNeighbors(origin.pos)

			#add all valid points to queue if not already in it
			for p in n:
				#found destination
				if p == t or self.atPos(t,p):
					path = []
					path.insert(0,p)
					dest = origin
					break

				#new point to add to queue of search
				if p not in visited and p not in pqueue:
					newpt = node(p,origin)
					queue.append(newpt)
					

		if dest == None:
			print(f"No path found to {self.target} = ({self.arena[self.target.y][self.target.x]})")
			return 0

		#find path back to current position
		while dest.parent != None:
			path.insert(0,dest.pos)
			dest = dest.parent

		self.path = path
		#self.printPath()

		return 1



	#returns valid neighbors of a given point
	def getNeighbors(self,p):
		dirs = [["up"],["down"],["left"],["right"],["up", "left"],["down", "left"],["up", "right"],["down", "right"]]

		validPts = []
		for d in dirs:
			if self.canMove(d,p):
				a = self.dir2Pt(d,p)
				validPts.append(a)

		return validPts


	#ai moves to the point based on the path calculated
	def gotoTarget(self):
		#if no target, stay create new one based on current mode
		if self.target == None:
			self.cancelTarget()
			self.modeSelect()
			return

		#if no path set, calculate it, otherwise cancel it
		if len(self.path) == 0 and not self.bfsPath(self.target):
			self.cancelTarget()
			return
			


		#determine next direction from the point in the path
		nextPt = self.path.pop(0)
		nextDir = self.pt2Dir(nextPt)
		for d in nextDir:
			self.move(d)

		#reach destination
		if len(self.path) == 0:
			self.cancelTarget()


	#cancel the path and target saved from the bfs calculation
	def cancelTarget(self):
		self.path = []
		self.target = None


	#debug to print the current path
	def printPath(self):
		s = ""
		for p in self.path:
			s += f"{p} "
		s += f" --> {self.target}"
		print(s)

		
	######   ROBOT MOVEMENT STRATEGIES  ######

	#reset the target based on the mode
	def modeChange(self, mode):
		self.mode = mode
		self.cancelTarget()
		self.modeSelect()

	#create target position based on robot mode
	def modeSelect(self):
		if(self.hp < self.maxhp/4):				#retreat @ quarter hp
			self.retreat()
		elif(self.mode == "random"):
			self.randArenaPos()
		elif(self.mode == "defensive"):
			self.defensive()
		elif(self.mode == "offensive"):
			self.offensive()


	#pick random empty spot on the map
	def randArenaPos(self):
		s = []
		for r in range(len(self.arena)):
			for c in range(len(self.arena[0])):
				if int(self.arena[r][c]) not in self.collisions:
					s.append([c,r])

		#set new target  
		p = random.choice(s)
		self.target = pt(p[0],p[1])

	#defensive control - hide from robots
	def defensive(self):
		return

	#offensive control - seek out robots
	def offensive(self):
		return

	#return to nearest base
	def retreat(self):
		#get closest base
		dists = []
		for b in self.bases:
			dists.append(pt(self.x,self.y).dist(b))
		dists = np.array(dists)
		self.target = self.bases[np.where(dists == min(dists))[0]]



