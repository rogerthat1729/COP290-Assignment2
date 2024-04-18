import pygame
from settings import *

font = pygame.font.Font("../graphics/font/merchant.ttf", 40)

class IntroScreen:
    def __init__(self, text, image_path, char_delay=13):
        self.full_text = text
        self.image = pygame.image.load(image_path)  # Load your image here
        self.image_rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.rendered_text = ""
        self.rendered_text_rect = pygame.Rect(50, HEIGHT - 100, WIDTH - 100, 50)
        self.rendered_chars = 0
        self.char_delay = char_delay
        self.last_char_render_time = 0

    def render(self, screen):
        screen.fill('black')

        # Render text at the bottom, gradually typing out
        if pygame.time.get_ticks() - self.last_char_render_time > self.char_delay:
            if self.rendered_chars < len(self.full_text):
                self.rendered_text += self.full_text[self.rendered_chars]
                self.rendered_chars += 1
                self.last_char_render_time = pygame.time.get_ticks()

        rendered_surface = font.render(self.rendered_text, True, 'white')
        screen.blit(rendered_surface, self.rendered_text_rect)

        # Render image at the center
        screen.blit(self.image, self.image_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                return True
        return False