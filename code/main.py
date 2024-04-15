import pygame, sys
from settings import *
from level import Level
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define your screens
class StartScreen:
    def __init__(self):
        self.options = ["Start", "Settings"]
        self.selected_option = 0

    def render(self, screen):
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)

        for i, option in enumerate(self.options):
            text = font.render(option, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 200 + i * 50))
            screen.blit(text, text_rect)

        selected_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 50)
        selected_rect.center = (SCREEN_WIDTH / 2, 200 + self.selected_option * 50)
        pygame.draw.rect(screen, WHITE, selected_rect, 3)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:
                    return "start"
                elif self.selected_option == 1:
                    return "settings"
        return None

class IntroScreen:
    def __init__(self, text, image_path, char_delay=20):
        self.full_text = text
        self.image = pygame.image.load(image_path)  # Load your image here
        self.image_rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.rendered_text = ""
        self.rendered_text_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 100, 50)  # Adjust position and size as needed
        self.rendered_chars = 0
        self.char_delay = char_delay
        self.last_char_render_time = 0

    def render(self, screen):
        screen.fill(BLACK)
        font = pygame.font.Font(None, 24)  # Decrease font size to 24 (or adjust as needed)

        # Render text at the bottom, gradually typing out
        if pygame.time.get_ticks() - self.last_char_render_time > self.char_delay:
            if self.rendered_chars < len(self.full_text):
                self.rendered_text += self.full_text[self.rendered_chars]
                self.rendered_chars += 1
                self.last_char_render_time = pygame.time.get_ticks()

        rendered_surface = font.render(self.rendered_text, True, WHITE)
        screen.blit(rendered_surface, self.rendered_text_rect)

        # Render image at the center
        screen.blit(self.image, self.image_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                return True
        return False

   
class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.DOUBLEBUF)
		pygame.display.set_caption('Dempression')
		self.clock = pygame.time.Clock()

		self.level = Level()
	
	def run(self):
		while True:
			self.level.events = pygame.event.get()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self.screen.fill('black')
			self.level.run()
			pygame.display.flip()
			self.clock.tick(FPS)

def main():
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)  # Set fullscreen mode
    pygame.display.set_caption("Intro")

    clock = pygame.time.Clock()

    # Create instances of each screen
    start_screen = StartScreen()
    intro_screen1 = IntroScreen("Susan had always been a bright and cheerful young woman, filled with a zest for life.", "../graphics/intro/girl.png")
    intro_screen2 = IntroScreen("Growing up, she was the light of her family, bringing joy and laughter wherever she went.", "../graphics/intro/family.png")
    intro_screen3 = IntroScreen("However,her world came crashing down when her brother, Ethan, passed away in a car accident.", "../graphics/intro/crash.png")
    intro_screen4 = IntroScreen("Ethan had been Susan's closest confidant, her partner in crime, and her rock.", "../graphics/intro/brother.png")
    intro_screen5 = IntroScreen("...", "../graphics/intro/flowers.png")
    intro_screen6 = IntroScreen("Susan has struggled to find her footing. The grief has consumed her, leaving her hopeless.", "../graphics/intro/sad.png")  
    intro_screen7 = IntroScreen("She has isolated herself from everyone, unable to find the strength to engage with the world around her.", "../graphics/intro/sad2.png") 
    intro_screen8 = IntroScreen("The darkness and despair had become unbearable for Susan. She attempted to take her own life, ", "../graphics/intro/rope.png")
    intro_screen9 = IntroScreen("But fate had other plans for Susan. The rope she had fashioned was not properly secured, and Susan found herself struggling for breath but still alive. As she lay on the floor, gasping for air, her eyes landed on a framed photograph of her beloved brother Ethan. Seeing his warm smile and kind eyes seemed to cut through the fog of her depression, igniting a glimmer of hope within her.", "../graphics/intro/hope.png")
    screens = [start_screen, intro_screen1, intro_screen2, intro_screen3, intro_screen4,intro_screen5,intro_screen6,intro_screen7,intro_screen8,intro_screen9]

    current_screen_index = 0

    running = True
    while running:
        screen.fill((0, 0, 0))

        current_screen = screens[current_screen_index]
        current_screen.render(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif current_screen_index == 0:
                result = current_screen.handle_event(event)
                if result == "start":
                    current_screen_index += 1
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        current_screen_index += 1
                        if current_screen_index >= len(screens):
                            running = False

        pygame.display.flip()
        clock.tick(60)

    game = Game()
    game.run()
    sys.exit()
if __name__ == "__main__":
    main()    