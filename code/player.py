import pygame 
from settings import *
from tasks import *
import sys

all_tasks = ["Talk on phone", "Go to balcony", "Clean your room"]
task_to_seq = {"Talk on phone": [pygame.K_p, pygame.K_h, pygame.K_o, pygame.K_n, pygame.K_e], "Go to balcony": [pygame.K_b, pygame.K_a, pygame.K_l, pygame.K_c, pygame.K_o, pygame.K_n, pygame.K_y], "Clean your room": [pygame.K_c, pygame.K_l, pygame.K_e, pygame.K_a, pygame.K_n]}

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)
		self.events = []
		
		self.done_task = 0
		self.wait = 0
		self.is_textbox_active = False
		self.textbox_content = ""

		self.direction = pygame.math.Vector2()
		self.speed = 5

		self.obstacle_sprites = obstacle_sprites

	def input(self):
		keys = pygame.key.get_pressed()
		if not self.is_textbox_active:
			if keys[pygame.K_w]:
				self.direction.y = -1
			elif keys[pygame.K_s]:
				self.direction.y = 1
			else:
				self.direction.y = 0

			if keys[pygame.K_d]:
				self.direction.x = 1
			elif keys[pygame.K_a]:
				self.direction.x = -1
			else:
				self.direction.x = 0
		
		if keys[pygame.K_1] and self.wait==0:
			self.is_textbox_active = not self.is_textbox_active
			self.textbox_content = ""
			self.wait = 100

		for event in self.events:
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if self.is_textbox_active:
					if event.key == pygame.K_BACKSPACE:
						self.textbox_content = self.textbox_content[:-1]
					else:
						char = event.unicode.upper()
						if char.isalpha():
							self.textbox_content += char

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center
		

	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

	def update(self):
		self.input()
		self.move(self.speed)
		self.wait = max(0,self.wait-1)