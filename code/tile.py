import pygame 
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups,sprite_type,surface = [pygame.Surface((TILESIZE,TILESIZE))],sprite_name = None):
		super().__init__(groups)
		self.sprite_type = sprite_type
		self.active = 0
		self.name = sprite_name
		self.imglist = surface
		self.image = surface[self.active]
		if(self.sprite_type == 'object'):
			self.rect = self.image.get_rect(topleft = [pos[0],pos[1]-TILESIZE])
		else:
			self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-10)
	
	def update_image(self):
		self.image = self.imglist[self.active]