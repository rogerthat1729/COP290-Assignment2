import pygame
import sys
from settings import *

class EndScreen:
    def __init__(self, win):
        self.win = win
        self.font = pygame.font.Font(None, 36)
        self.replay_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 100, 100, 50)
        self.exit_button = pygame.Rect(WIDTH // 2 + 150, HEIGHT // 2 + 100, 100, 50)

    def draw(self, screen):
        if self.win:
            message = self.font.render("Congratulations for winning the game", True, (255, 255, 255))
        else:
            message = self.font.render("Please try again", True, (255, 255, 255))
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - 100))

        pygame.draw.rect(screen, (0, 255, 0), self.replay_button)
        replay_text = self.font.render("Replay", True, (0, 0, 0))
        screen.blit(replay_text, (self.replay_button.x + 25 - replay_text.get_width() // 2, self.replay_button.y + 15 - replay_text.get_height() // 2))

        pygame.draw.rect(screen, (255, 0, 0), self.exit_button)
        exit_text = self.font.render("Exit", True, (0, 0, 0))
        screen.blit(exit_text, (self.exit_button.x + 25 - exit_text.get_width() // 2, self.exit_button.y + 15 - exit_text.get_height() // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.replay_button.collidepoint(event.pos):
                return 'menu'
            elif self.exit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
        return 'end'