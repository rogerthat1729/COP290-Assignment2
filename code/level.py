import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from tasks import *
import math
import sys
import time

index_to_name = {1419:'chair', 1389:'trashcan', 1357:'telephone', 1485:'bathtub', 1386:'sink', 1390:'books', 
				 1391:'notes', 1480:'washing_machine', 1742:'door', 1738:'bed'}

def create_radial_gradient(width, height, inner_color, outer_color):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    center = (width // 2, height // 2)
    max_radius = int(max(center[0], center[1]) * 1.414)  # Diagonal length
    num_circles = 50  # Number of concentric circles. Adjust for smoothness.

    for i in range(num_circles, 0, -1):
        radius = (i / num_circles) * max_radius
        color = [inner_color[j] + (outer_color[j] - inner_color[j]) * (i / num_circles) for j in range(4)]
        pygame.draw.circle(surface, color, center, int(radius))
    
    return surface

def happiness_to_alpha(happy, max_happy=100, min_alpha=0, max_alpha=255):
    """
    Convert happiness level to an alpha value for the overlay using an exponential function.
    
    :param happy: Current happiness level.
    :param max_happy: Maximum possible happiness level.
    :param min_alpha: Minimum alpha value (more transparent, more happy).
    :param max_alpha: Maximum alpha value (less transparent, less happy).
    :return: Alpha value based on the current happiness level.
    """
    # Map the happiness to a [0, 1] range
    normalized_happy = happy / max_happy
    # Use an exponential function for a non-linear mapping
    # Adjust the exponent as needed to achieve the desired perceptual uniformity
    non_linear_alpha = (1 - math.pow(normalized_happy, 2)) * (max_alpha - min_alpha) + min_alpha
    # Ensure alpha is within bounds
    alpha = max(min_alpha, min(max_alpha, non_linear_alpha))
    return int(alpha)


bad_tasks = {1:["You browsed through social media for 2 hours.",  "Your mental health is reduced by 10 points."],
			  2:["You ate a lot of junk food.", "Your mental health is reduced by 10 points."],
			    3:["You watched TV for 3 hours", "Your mental health is reduced by 15 points"],
				4:["You overthought about your bad grade", "Your mental health is reduced by 15 points"],
				5: ["You stayed in bed all day and didn't talk to anyone", "Your mental health is reduced by 20 points"]}
happiness_reduced = {1:10, 2:10, 3:15, 4:15, 5:20}
task_to_obj = {"Talk on phone":'telephone', "Go to balcony":'chair', "Clean out the trash":'trashcan', "Take a bath":'bathtub', "Do the dishes":'sink', 
			   "Read a book":'books', 'Do the laundry':'washing_machine', "Buy groceries":'door', 'Take a nap':'bed'}

difficulty_to_bad_task_wait = {'Easy':1500, 'Medium':1000, 'Hard':500}

class Level:
	def __init__(self, character, difficulty, music_volume, game_volume):
		# get the display surface 
		self.display_surface = pygame.display.get_surface()
		self.overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		self.go_to_menu = False

		#tasks
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
		
		self.events = []

		self.nearest_object = []
		self.interact_time = None
		self.interact_wait = 4
		self.playing_music = False
		self.playing_bg = True
		self.bg_track_path = '../audio/bg.mp3'

		self.phone_keypad_content = ""
		self.phone_keypad_active = False
		self.correct_code = '69420'

		self.notes_active = False

		self.pause_rect = pygame.Rect((1550/1600)*WIDTH, (50/880)*HEIGHT, 100, 100)
		self.paused = False
		
		self.music_volume = music_volume
		self.game_volume = game_volume

		self.booktask = BookTask(self)
		self.book_active = False
		# sprite setup
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

	def update_brightness(self):
		width, height = self.display_surface.get_size() 
		alpha = happiness_to_alpha(self.happy)
		inner_color = (0, 0, 0, 0)
		outer_color = (0, 0, 0, min(alpha*4, 255))
		
		gradient_overlay = create_radial_gradient(width, height, inner_color, outer_color)
		self.display_surface.blit(gradient_overlay, (0, 0))
		pygame.display.flip()
	
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
 
	def input(self):
		# print(self.paused)
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

		
		self.booktask.render()
		for event in self.events:
			self.booktask.handle_input(event)
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if self.pause_rect.collidepoint(event.pos):
					self.paused = not self.paused
			elif (not self.paused):
				if event.type == pygame.KEYDOWN and (not self.player.popup.active):
					if event.key == pygame.K_b:
						if self.task_list[0]=='Read a book' and check_for_object(self.nearest_object, 'books') and not self.book_active:
							self.booktask.active = True
					if event.key == pygame.K_p:
						if self.task_list[0]=='Talk on phone' and check_for_object(self.nearest_object, 'telephone') and not self.phone_keypad_active:
							self.phone_keypad_active = True
						elif check_for_object(self.nearest_object, 'notes') and not self.notes_active:
							self.notes_active = True
					if event.key == pygame.K_i:
						if check_for_object(self.nearest_object, task_to_obj[self.task_list[0]]) and not self.interact_time:
							self.interact_time = time.time()
							if not self.playing_music:
								self.playing_music = True
						else:
							self.interact_time = None
					else:
						self.interact_time = None
					if self.phone_keypad_active:
						if event.unicode.isnumeric() and len(self.phone_keypad_content) < 5:
							self.phone_keypad_content += str(event.unicode)
						elif event.key == pygame.K_BACKSPACE:
							self.phone_keypad_content = self.phone_keypad_content[:-1]
						elif event.key == pygame.K_RETURN:
							check_keypad_code(self)
				elif event.type == pygame.KEYUP and event.key == pygame.K_i and self.interact_time:
					self.interact_time = None
			else:
				self.interact_time = None
		
	def handle_tasks(self):
		if self.notes_active:
			display_task(self, 'Check the notes', None)

		if self.player.done_task == 0 and check_for_object(self.nearest_object, task_to_obj[self.task_list[0]]):
			if (self.interact_time or self.phone_keypad_active):
				display_task(self, self.task_list[0], self.interact_time, self.interact_wait, self.phone_keypad_content)
				if self.task_list[0]=='Buy groceries':
					self.player.show_player = False
				elif self.task_list[0]=='Take a nap':
					self.player.show_player = False
					fade_to_black(self)
					change_to_task_image(self, 'bed')
				if self.playing_music:
					play_music(task_to_seq[self.task_list[0]], self)
					self.playing_music = False
			else:
				self.interact_time = None
				self.player.show_player = True
		
		if self.player.done_task == 1 or self.task_list[0] != 'Read a book' or not check_for_object(self.nearest_object, 'books'):
			self.booktask.active = False

		if self.interact_time:
			if self.task_list[0] == 'Talk on phone':
				pass
			else:
				if time.time() - self.interact_time >= self.interact_wait and check_for_object(self.nearest_object, task_to_obj[self.task_list[0]]):
					self.player.done_task = 1
					self.interact_time = None
		else:
			pygame.mixer.music.stop()
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
		self.input()
		self.check_menu(game)
		if(not self.paused):
			self.update_recovery()
			self.check_win_or_lose(game)
			self.handle_tasks()
			self.activate_objects() 
			self.handle_popup()
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
		self.floor_surf = pygame.image.load('../map/basic_map.png').convert()
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