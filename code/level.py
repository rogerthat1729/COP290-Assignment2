import pygame 
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice
from tasks import *
from dictionaries import *
from walkbook import *
import sys
import time

pygame.mixer.init()

class Level:
	def __init__(self, character, difficulty, music_volume, game_volume):
		self.display_surface = pygame.display.get_surface()
		self.overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)

		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		self.go_to_menu = False

		self.happy = 90
		self.recovery = 95
		self.task_list = good_tasks.copy()
		self.bad_task = ""
		self.player = Player((1980,1500),[self.visible_sprites],self.obstacle_sprites, character)
		self.show_player = True
		self.player.speed = 5 + (self.happy/100)*5

		self.brightness_wait = 0
		self.pop_up_wait = 0
		self.bad_task_wait = difficulty_to_bad_task_wait[difficulty]

		self.control_text = []
		
		self.events = []

		self.nearest_object = []
		self.interact_time = None
		self.interact_wait = 4

		self.gamebg_track_path = '../audio/gamebg.mp3'
		self.menubg_track_path = '../audio/bg.mp3'

		self.phone_keypad_content = ""
		self.phone_keypad_active = False
		self.correct_code = '69420'

		self.notes_active = False

		self.pause_rect = pygame.Rect((1550/1600)*WIDTH, (50/880)*HEIGHT, 100, 100)
		self.paused = False
		
		self.music_volume = music_volume
		self.game_volume = game_volume

		self.task_music_running = 0
		self.game_music_running = 1
		self.menu_music_running = 0

		self.booktask = BookTask(self)
		self.walktask = WalkTask(self)
		self.book_active = False

		self.create_map()

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('../map/map1_FloorBlocks.csv'),
			'grass': import_csv_layout('../map/map1_Grass.csv'),
			'object': import_csv_layout('../map/map1_Objects.csv'),
			'details': import_csv_layout('../map/map1_Details.csv'),
			'entities': import_csv_layout('../map/map1_Entities.csv')
		}
		graphics = {
			'objects': import_folder_for_objects('../graphics1')
		}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						idx = int(col)
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')
						elif style == 'object':
							if idx in index_to_name.keys():
								imgs = import_folder('../graphics/objects/'+index_to_name[idx])
								Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',imgs, index_to_name[idx])
							else:
								surf = graphics['objects'][idx]
								Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',[surf])

	def handle_popup(self):
		if self.pop_up_wait >= self.bad_task_wait and not self.interact_time:
			bad_task_index = choice(list(bad_tasks.keys()))
			self.bad_task = bad_tasks[bad_task_index]
			self.pop_up_wait = 0
			self.player.popup.active = True
			self.happy = max(0, self.happy-happiness_reduced[bad_task_index])
		elif (not self.player.popup.active) and (not self.interact_time) and (not self.paused):
			self.pop_up_wait += 1
		if self.player.popup.active:
			show_popup(self, self.bad_task)
	
	def handle_music(self, arg=None):	
		if not arg:
			if self.menu_music_running == 0 and self.game_music_running == 1 and self.task_music_running == 0:
				pygame.mixer.music.stop()
				pygame.mixer.music.load(self.gamebg_track_path)
				pygame.mixer.music.set_volume(self.game_volume/100)
				pygame.mixer.music.play(-1)
				self.game_music_running = 2
			if self.menu_music_running == 0 and self.game_music_running == 0 and self.task_music_running == 1:
				pygame.mixer.music.stop()
				play_music(task_to_seq[self.task_list[0]], self)
				self.task_music_running = 2
			if self.menu_music_running == 1 and self.game_music_running == 0 and (self.task_music_running == 0 or self.task_music_running == 2):
				pygame.mixer.music.stop()
				pygame.mixer.music.load(self.menubg_track_path)
				pygame.mixer.music.set_volume(self.music_volume/100)
				pygame.mixer.music.play(-1)
				self.menu_music_running = 2
		else:
			if arg == 1:
				if self.menu_music_running==0 and self.game_music_running==2 and self.task_music_running==0:
					self.menu_music_running = 1
					self.game_music_running = 0
					self.task_music_running = 0
				elif self.menu_music_running==0 and self.game_music_running==0 and self.task_music_running==2:
					self.menu_music_running = 1
					self.game_music_running = 0
					self.task_music_running = 2
			elif arg==2:
				if self.menu_music_running==0 and self.game_music_running==0 and self.task_music_running==2:
					self.menu_music_running = 0
					self.game_music_running = 1
					self.task_music_running = 0
			elif arg==3:
				if self.menu_music_running==2 and self.game_music_running==0 and self.task_music_running==2:
					self.menu_music_running = 0
					self.game_music_running = 0
					self.task_music_running = 1
				elif self.menu_music_running==2 and self.game_music_running==0 and self.task_music_running==0:
					self.menu_music_running = 0
					self.game_music_running = 1
					self.task_music_running = 0
			elif arg==4:
				if self.menu_music_running==0 and self.game_music_running==2 and self.task_music_running==0:
					self.menu_music_running = 0
					self.game_music_running = 0
					self.task_music_running = 1
		
	def input(self):
		draw_pause_button(self)
		keys = pygame.key.get_pressed()
		bothchecker=0
		if(not self.paused):
			if keys[pygame.K_w]:
				self.player.direction.y = -1
				self.player.status = 'up'
				bothchecker+=1
			elif keys[pygame.K_s]:
				self.player.direction.y = 1
				self.player.status = 'down'
				bothchecker+=1
			else:
				self.player.direction.y = 0

			if keys[pygame.K_d]:
				self.player.direction.x = 1
				self.player.status = 'right'
				bothchecker+=1
			elif keys[pygame.K_a]:
				self.player.direction.x = -1
				self.player.status = 'left'
				bothchecker+=1
			else:
				self.player.direction.x = 0
			if bothchecker==2:
				self.player.direction.x/=2
				self.player.direction.y/=2
			if keys[pygame.K_ESCAPE]:
				if self.player.popup.active:
					self.player.popup.active = False
				elif self.phone_keypad_active:
					self.phone_keypad_active = False
					self.phone_keypad_content = ""
				elif self.notes_active:
					self.notes_active = False
		else:
			self.player.direction.x = 0
			self.player.direction.y = 0
		
		if not self.paused and self.menu_music_running==2:
			self.handle_music(3)
		elif self.paused:
			self.handle_music(1)

		if self.task_list[0]=='Take a walk':
			# print("walk task going on")
			# print(self.interact_time)
			self.walktask.update()
			self.walktask.render()

		self.booktask.render()
		for event in self.events:
			self.booktask.handle_input(event)
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if self.pause_rect.collidepoint(event.pos):
					if self.paused:
						self.handle_music(1)
					self.paused = not self.paused
			elif (not self.paused):
				if event.type == pygame.KEYDOWN and (not self.player.popup.active):
					if event.key == pygame.K_b:
						if self.task_list[0]=='Read a book' and check_for_object(self.nearest_object, 'books') and not self.book_active:
							self.booktask.active = True
					elif event.key == pygame.K_p:
						if self.task_list[0]=='Talk on phone' and check_for_object(self.nearest_object, 'telephone') and not self.phone_keypad_active:
							self.phone_keypad_active = True
						elif check_for_object(self.nearest_object, 'notes') and not self.notes_active:
							self.notes_active = True
					elif event.key == pygame.K_i:
						if self.task_list[0]=='Take a walk':
							for obj in task_to_obj[self.task_list[0]]:
								if check_for_object(self.nearest_object, obj) == True and not self.interact_time:
									self.interact_time = time.time()
									# print("hello")
									# self.handle_music(4)
									break
								# if check_for_object(self.nearest_object, obj) and not self.interact_time():
								# 	self.interact_time = time.time()
								# 	self.handle_music(4)
								# 	break
						elif check_for_object(self.nearest_object, task_to_obj[self.task_list[0]]) and not self.interact_time:
							self.interact_time = time.time()
							self.handle_music(4)
					else:
						self.interact_time = None
						self.handle_music(2)
					if self.phone_keypad_active:
						if event.unicode.isnumeric() and len(self.phone_keypad_content) < 5:
							self.phone_keypad_content += str(event.unicode)
						elif event.key == pygame.K_BACKSPACE:
							self.phone_keypad_content = self.phone_keypad_content[:-1]
						elif event.key == pygame.K_RETURN:
							check_keypad_code(self)
				elif event.type == pygame.KEYUP and event.key == pygame.K_i and self.interact_time:
					self.show_player = True
					self.interact_time = None
					self.handle_music(2)
			else:
				self.show_player = True
				self.interact_time = None
				self.handle_music(2)
		
	def handle_tasks(self):

		if self.notes_active:
			display_task(self, 'Check the notes', None)

		if self.player.done_task == 0 and check_for_object(self.nearest_object, task_to_obj[self.task_list[0]]) and self.task_list[0]!='Take a walk':
			if (self.interact_time or self.phone_keypad_active):
				# print(self.interact_time==None)
				display_task(self, self.task_list[0], self.interact_time, self.interact_wait, self.phone_keypad_content)
				if self.task_list[0]=='Buy groceries':
					self.player.show_player = False
					change_to_task_image(self, 'door')
				elif self.task_list[0]=='Take a nap':
					self.player.show_player = False
					fade_to_black(self)
					change_to_task_image(self, 'bed')
			else:
				self.handle_music(2)
				self.interact_time = None
				self.player.show_player = True
		elif self.task_list[0]!='Take a walk':
			self.handle_music(2)
			self.interact_time = None
			self.player.show_player = True
		
		if self.player.done_task == 1 or self.task_list[0] != 'Read a book' or not check_for_object(self.nearest_object, 'books'):
			self.booktask.active = False

		if self.interact_time:
			if self.task_list[0] == 'Talk on phone' or self.task_list[0]=='Take a walk':
				pass
			else:
				if time.time() - self.interact_time >= self.interact_wait and check_for_object(self.nearest_object, task_to_obj[self.task_list[0]]):
					self.player.done_task = 1
					self.interact_time = None
		# pygame.mixer.music.play('../audio/bg.mp3')
			
	
	def activate_objects(self):
		player = self.player
		for obj in self.nearest_object:
			if abs(player.rect.centerx - obj.rect.centerx) >= 100 or abs(player.rect.centery - obj.rect.centery) >= 100:
				self.nearest_object.pop(self.nearest_object.index(obj))
		for spr in self.visible_sprites.sprites():
			if spr.sprite_type == 'object' and spr.name and (not self.interact_time) :
				if abs(player.rect.centerx - spr.rect.centerx) < 100 and abs(player.rect.centery - spr.rect.centery) < 100:
					spr.active = 1
					self.nearest_object.append(spr)
				else:
					spr.active = 0
				spr.update_image()
	
	def update_recovery(self):
		if(self.happy >= 80):
			self.recovery = min(100, self.recovery+0.05)
	
	def check_near_object(self, objname):
		for sprite in self.visible_sprites.sprites():
			if sprite.sprite_type == 'object':
				if sprite.name == objname:
					return (sprite.active==1)
		return True
	
	def check_win_or_lose(self, game):
		if self.recovery==100:
			game.go_to = "end"
		
	def check_menu(self, game):
		if self.go_to_menu:
			game.go_to = "menu"
		
	def run(self, game):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		render_tasks(self)
		render_controls(self)
		self.input()
		self.check_menu(game)
		self.handle_music()
		if(not self.paused):
			self.update_recovery()
			self.check_win_or_lose(game)
			self.handle_tasks()
			self.activate_objects() 
			self.handle_popup()
		# print("here")
		# self.update_brightness()

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# creating the floor
		self.floor_surf = pygame.image.load('../map/new_map_files/basic_map.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# drawing the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			if(sprite.sprite_type=='player' and (not player.show_player)):
				pass
			else:
				offset_pos = sprite.rect.topleft - self.offset
				self.display_surface.blit(sprite.image,offset_pos)