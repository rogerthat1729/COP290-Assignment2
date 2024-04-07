import pygame, sys
from settings import *
from level import Level

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.DOUBLEBUF)
		pygame.display.set_caption('Dempression')
		self.clock = pygame.time.Clock()

		self.level = Level()
	
	def run(self):
		while True:
			self.level.player.events = pygame.event.get()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self.screen.fill('black')
			self.level.run()
			pygame.display.flip()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()