import pygame 
from settings import *
from tasks import *
from support import import_folder
from settings import *

all_tasks = ["Talk on phone", "Go to balcony", "Clean your room"]
task_to_seq = {"Talk on phone": [pygame.K_p, pygame.K_h, pygame.K_o, pygame.K_n, pygame.K_e], 
			   "Go to balcony": [pygame.K_b, pygame.K_a, pygame.K_l, pygame.K_c, pygame.K_o, pygame.K_n, pygame.K_y], 
			   "Clean your room": [pygame.K_c, pygame.K_l, pygame.K_e, pygame.K_a, pygame.K_n]}

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites, character):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/player1/down_idle/idle_down.png').convert_alpha()
		if character == 'character2':
			self.image = pygame.image.load('../graphics/player2/down_idle/idle_down.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)
		self.speed = 10

		self.import_player_assets(character)
		self.sprite_type = 'player'
		self.show_player = True
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.15
		
		self.done_task = 0
		self.wait = 0

		self.popup = Popup("", 500, 60)

		self.direction = pygame.math.Vector2()

		self.obstacle_sprites = obstacle_sprites

	def import_player_assets(self, character):
		character_path = '../graphics/player1/'
		if character == 'character2':
			character_path = '../graphics/player2/'
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)
	
	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status:
				self.status = self.status + '_idle'

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
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
	
	def animate(self):
		animation = self.animations[self.status]

		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)


	def update(self):
		self.get_status()
		self.animate()
		self.move(self.speed)
		self.wait = max(0,self.wait-1)