import pygame
from settings import *

font = pygame.font.Font("../graphics/font/merchant.ttf", 40)

class IntroScreen:
    def __init__(self, text, image_path, char_delay=18):
        self.full_text = text
        self.image = pygame.image.load(image_path)
        # self.image = pygame.transform.scale(self.image, (WIDTH // 2, HEIGHT // 2))
        self.image_rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.rendered_text = ""
        self.rendered_text_rect = pygame.Rect(50, HEIGHT - 100, WIDTH - 100, 50)
        self.rendered_chars = 0
        self.char_delay = char_delay
        self.last_char_render_time = 0

    def render(self, screen, fade_timer):
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

        overlay = pygame.Surface((self.image_rect.width, self.image_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 255-fade_timer))
        screen.blit(overlay, self.image_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                return True
        return False

def fade_screen(surface, duration, fade_out=True):
    """
    Fades the screen in or out over the specified duration.
    
    :param surface: The Pygame surface to fade.
    :param duration: The duration of the fade in milliseconds.
    :param fade_out: If True, fades out. If False, fades in.
    """
    start_alpha = 255 if fade_out else 0
    end_alpha = 0 if fade_out else 255
    step = (start_alpha - end_alpha) / (duration // 16) # 16 is the number of steps in the fade

    for alpha in range(start_alpha, end_alpha, int(step)):
        # Create a new surface with the same size as the screen
        fade_surface = pygame.Surface(surface.get_size())
        fade_surface.set_alpha(alpha)
        # Draw the original surface onto the fade surface
        fade_surface.blit(surface, (0, 0))
        # Update the display with the fade surface
        pygame.display.flip()
        # Wait for the next frame
        pygame.time.wait(16)