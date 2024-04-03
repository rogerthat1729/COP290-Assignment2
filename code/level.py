import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from tasks import *

bad_tasks = {1:["You browsed through social media for 2 hours.",  "Your happiness is reduced by 10 points."],
			  2:["You ate a lot of junk food.", "Your happiness is reduced by 10 points."],
			    3:["You watched TV for 3 hours", "Your happiness is reduced by 15 points"]}
happiness_reduced = {1:10, 2:10, 3:15}

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()
		self.overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		#tasks
		self.happy = 50
		self.task_list = ["Talk on phone", "Go to balcony", "Clean your room"]
		self.bad_task = ""

		self.brightness_wait = 0
		self.pop_up_wait = 0

		# sprite setup
		self.create_map()

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('../map/goodmap_FloorBlocks.csv'),
			'grass': import_csv_layout('../map/map1_Grass.csv'),
			'object': import_csv_layout('../map/map1_Objects.csv'),
		}
		graphics = {
			'grass': import_folder('../graphics/grass'),
			'objects': import_folder('../graphics/objects')
		}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'grass',random_grass_image)
						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)

		self.player = Player((1980,1500),[self.visible_sprites],self.obstacle_sprites)
	
	def update_brightness(self):
		alpha = max(0, min(255, 255 - (self.happy * 2.55)))
		self.overlay.fill((0, 0, 0, alpha)) 
		self.display_surface.blit(self.overlay, (0, 0))
		pygame.display.flip()
	
	def handle_popup(self):
		if self.pop_up_wait >= 200 and (not self.player.is_textbox_active):
			bad_task_index = choice(list(bad_tasks.keys()))
			self.bad_task = bad_tasks[bad_task_index]
			self.pop_up_wait = 0
			self.player.popup.active = True
			self.happy = max(0, self.happy-happiness_reduced[bad_task_index])
		elif (not self.player.popup.active) and (not self.player.is_textbox_active):
			self.pop_up_wait += 1

		if self.player.popup.active:
			show_popup(self, self.bad_task)
		

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		render_tasks(self)
		render_textbox(self.task_list[0], self.player.textbox_content, self)
		self.handle_popup()
		self.update_brightness()


class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# creating the floor
		self.floor_surf = pygame.image.load('../graphics/tilemap/basic_map.png').convert()
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
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
