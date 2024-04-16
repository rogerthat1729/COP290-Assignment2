import pygame, sys
from settings import *
from level import Level
from start import *
from intro import *
pygame.init()
    
class Game:
    def __init__(self, character, difficulty):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)  # Set fullscreen mode
        pygame.display.set_caption('Dempression')
        self.clock = pygame.time.Clock()

        self.level = Level(character, difficulty)

    def run(self):
        self.screen.fill('black')
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
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Intro")

    clock = pygame.time.Clock()

    # Create instances of each screen
    intro_screen1 = IntroScreen("Susan had always been a bright and cheerful young woman, filled with a zest for life.", "../graphics/intro/girl.png")
    intro_screen2 = IntroScreen("Growing up, she was the light of her family, bringing joy and laughter wherever she went.", "../graphics/intro/family.png")
    intro_screen3 = IntroScreen("However,her world came crashing down when her brother, Ethan, passed away in a car accident.", "../graphics/intro/crash.png")
    intro_screen4 = IntroScreen("Ethan had been Susan's closest confidant, her partner in crime, and her rock.", "../graphics/intro/brother.png")
    intro_screen5 = IntroScreen("...", "../graphics/intro/flowers.png")
    intro_screen6 = IntroScreen("Susan has struggled to find her footing. The grief has consumed her, leaving her hopeless.", "../graphics/intro/sad.png")  
    intro_screen7 = IntroScreen("She has isolated herself from everyone, unable to find the strength to engage with the world around her.", "../graphics/intro/sad2.png") 
    intro_screen8 = IntroScreen("The darkness and despair had become unbearable for Susan. She attempted to take her own life, ", "../graphics/intro/rope.png")
    intro_screen9 = IntroScreen("But fate had other plans for Susan. The rope she had fashioned was not properly secured, and Susan found herself struggling for breath but still alive. As she lay on the floor, gasping for air, her eyes landed on a framed photograph of her beloved brother Ethan. Seeing his warm smile and kind eyes seemed to cut through the fog of her depression, igniting a glimmer of hope within her.", "../graphics/intro/hope.png")

    menu = Menu()
    start_menu = StartMenu()
    settings_menu = SettingsMenu()
    current_menu = 'menu'
    screens = [intro_screen1, intro_screen2, intro_screen3, intro_screen4, intro_screen5, intro_screen6, intro_screen7, intro_screen8, intro_screen9]
    current_screen_index = 0

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if current_menu == 'menu':
                if menu.handle_event(event) == 'start':
                    current_menu = 'start'
                elif menu.handle_event(event) == 'settings':
                    current_menu = 'settings'
                elif menu.handle_event(event) == 'exit':
                    running = False
            elif current_menu == 'start':
                current_menu = start_menu.handle_event(event)
            elif current_menu == 'settings':
                current_menu = settings_menu.handle_event(event)
            elif current_menu == 'intro':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if current_screen_index >= len(screens):
                            game = Game(start_menu.characters[start_menu.selected_character], start_menu.difficulties[start_menu.selected_difficulty])
                            game.run()
                        current_screen_index += 1
        if current_menu == 'menu':
            menu.draw(screen)
        elif current_menu == 'start':
            start_menu.draw(screen)
        elif current_menu == 'settings':
            settings_menu.draw(screen)
        elif current_menu == 'intro' and current_screen_index < len(screens):
            screens[current_screen_index].render(screen)
        pygame.display.flip()
        clock.tick(60)
    sys.exit()

if __name__ == "__main__":
    main()    