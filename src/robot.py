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

class Robot(pygame.sprite.Sprite):
	def __init__(self, x,y, rot, sqr_pix, color):
		super(Robot, self).__init__()
		self.px = sqr_pix
		self.color = color

		self.x = x
		self.y = y
		self.rot = 0
		
		self.surf = pygame.Surface((4*sqr_pix, 4*sqr_pix))		#take up 4x4 pixel space
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

	def move(self,direction):
		if direction == "up":
			self.y-=1
		elif direction == "down":
			self.y+=1
		if direction == "left":
			self.x-=1
		elif direction == "right":
			self.x+=1


