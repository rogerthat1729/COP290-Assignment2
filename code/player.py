import pygame 
from settings import *
from tasks import *
# import sys
from support import import_folder
# import time

all_tasks = ["Talk on phone", "Go to balcony", "Clean your room"]
task_to_seq = {"Talk on phone": [pygame.K_p, pygame.K_h, pygame.K_o, pygame.K_n, pygame.K_e], 
			   "Go to balcony": [pygame.K_b, pygame.K_a, pygame.K_l, pygame.K_c, pygame.K_o, pygame.K_n, pygame.K_y], 
			   "Clean your room": [pygame.K_c, pygame.K_l, pygame.K_e, pygame.K_a, pygame.K_n]}

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)

		self.import_player_assets()
		self.sprite_type = 'player'
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.15
		
		self.done_task = 0
		self.wait = 0
		# self.is_textbox_active = False
		# self.textbox_content = ""

		self.popup = Popup("", 500, 60)

		self.direction = pygame.math.Vector2()

		self.obstacle_sprites = obstacle_sprites

	def import_player_assets(self):
		character_path = '../graphics/player/'
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	# def input(self):
		# if(self.nearest_obj):
		# 	print("Object")
		# else:
		# 	print("No")

		# keys = pygame.key.get_pressed()
		# # if not self.is_textbox_active:
		# if keys[pygame.K_w]:
		# 	self.direction.y = -1
		# 	self.status = 'up'
		# elif keys[pygame.K_s]:
		# 	self.direction.y = 1
		# 	self.status = 'down'
		# else:
		# 	self.direction.y = 0

		# if keys[pygame.K_d]:
		# 	self.direction.x = 1
		# 	self.status = 'right'
		# elif keys[pygame.K_a]:
		# 	self.direction.x = -1
		# 	self.status = 'left'
		# else:
		# 	self.direction.x = 0
		
		# if keys[pygame.K_ESCAPE] and self.popup.active:
		# 	self.popup.active = False
			
		# if keys[pygame.K_ESCAPE] and self.is_textbox_active:
		# 	self.is_textbox_active = False

		# if keys[pygame.K_1] and self.wait==0 and not self.popup.active:
		# 	self.is_textbox_active = not self.is_textbox_active
		# 	self.textbox_content = ""
		# 	self.wait = 100

		# for event in self.events:
		# 	if event.type == pygame.QUIT:
		# 		pygame.quit()
		# 		sys.exit()
			# elif event.type == pygame.KEYDOWN:
				# if self.is_textbox_active:
				# 	if event.key == pygame.K_BACKSPACE:
				# 		self.textbox_content = self.textbox_content[:-1]
				# 	else:
				# 		char = event.unicode.upper()
				# 		if char.isalpha():
				# 			self.textbox_content += char
		# 		if event.key == pygame.K_i:
		# 			if not self.interact_time:
		# 				self.interact_time = time.time()
		# 	elif event.type == pygame.KEYUP:
		# 		if event.key == pygame.K_i and self.interact_time:
		# 			self.interact_time = None
		
		# if self.interact_time:
		# 	if time.time() - self.interact_time >= 3:
		# 		self.done_task = 1
		# 		print("Task done")
		# 		self.interact_time = None

	
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
	
	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)


	def update(self):
		# self.input()
		self.get_status()
		self.animate()
		self.move(self.speed)
		self.wait = max(0,self.wait-1)