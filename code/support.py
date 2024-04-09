from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		img_files.sort()
		for image in img_files:
			# print(image)
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path)
			surface_list.append(image_surf)

	return surface_list

def import_folder_for_objects(path):
	surface_list = []

	for _,__,img_files in walk(path):
		img_files.sort(key=lambda x: int(x[:-4]))
		# print(img_files)
		for image in img_files:
			# print(image)
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path)
			surface_list.append(image_surf)

	return surface_list
