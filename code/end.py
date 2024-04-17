import pygame
import sys
from settings import *
from start import draw_text
from tasks import Button

class EndScreen:
    def __init__(self, win):
        self.win = win
        self.bg = pygame.image.load("../graphics/endscene/goodend.png")
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        self.font = pygame.font.Font("../graphics/font/joystix.ttf", 48)
        self.replay_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, 'Replay', 'green')
        self.exit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 200, 200, 50, 'Exit', 'red')

    def draw(self, screen):
        if self.win:
            message = "Congratulations for winning the game"
        else:
            message = "Please try again"
        screen.blit(self.bg, (0, 0))
        draw_text(message, self.font, 'white', screen, 250, HEIGHT // 2 - 50)
        self.replay_button.draw(screen)
        self.exit_button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.replay_button.is_clicked(event.pos):
                return 'menu'
            elif self.exit_button.is_clicked(event.pos):
                pygame.quit()
                sys.exit()
        return 'end'