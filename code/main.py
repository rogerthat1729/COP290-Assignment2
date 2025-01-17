import pygame, sys
from settings import *
from level import Level
from start import *
from intro import *
from end import *
pygame.init()
pygame.mixer.init()
    
class Game:
    def __init__(self, character, difficulty, music_volume, game_volume):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF) 
        self.clock = pygame.time.Clock()
        self.level = Level(character, difficulty, music_volume, game_volume)
        self.go_to = None

    def run(self):
        self.screen.fill('black')
        while True:
            self.level.events = pygame.event.get()
            # print(self.level.events)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            self.level.run(self)
            if self.go_to:
                break
            pygame.display.flip()
            self.clock.tick(FPS)

def main():
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    # Create instances of each screen
    intro_screen1 = IntroScreen("Rosa had always been a bright and cheerful young woman, filled with a zest for life.", "../graphics/intro/girl2.png")
    intro_screen2 = IntroScreen("Growing up, she was the light of her family, bringing joy and laughter wherever she went.", "../graphics/intro/family.png")
    intro_screen3 = IntroScreen("However, her world came crashing down when her brother, Ethan, passed away in a car accident.", "../graphics/intro/crash.png")
    intro_screen4 = IntroScreen("Ethan had been Rosa's closest confidant, her partner in crime, and her ultimate support.", "../graphics/intro/brother.png")
    intro_screen5 = IntroScreen("...", "../graphics/intro/flowers.png")
    intro_screen6 = IntroScreen("Rosa struggled to find her footing. The grief consumed her, leaving her hopeless.", "../graphics/intro/sad.png")  
    intro_screen7 = IntroScreen("She isolated herself from everyone, unable to find the strength to engage with the world around her.", "../graphics/intro/sad2.png") 
    intro_screen8 = IntroScreen("The darkness and despair had become unbearable for Rosa. She attempted to take her own life, ", "../graphics/intro/rope.png")
    intro_screen9 = IntroScreen("But fate had other plans for Rosa...", "../graphics/intro/rope.png")
    intro_screen10 = IntroScreen("The rope she had fashioned was not properly secured, and Rosa found herself struggling for breath but still alive.", "../graphics/intro/introrope.png")
    intro_screen11 = IntroScreen("As she lay on the floor, gasping for air, her eyes landed on a framed photograph of her beloved brother Ethan.", "../graphics/intro/hope.png")
    intro_screen12 = IntroScreen("His warm smile and kind eyes seemed to cut through the fog of her depression, igniting a glimmer of hope within her.", "../graphics/intro/introlast.png")

    intro_screen_timer = 0
    fade_timer = 0
    menu = Menu()
    start_menu = StartMenu()
    settings_menu = SettingsMenu()
    end_screen = EndScreen(True)
    current_menu = 'menu'
    screens = [intro_screen1, intro_screen2, intro_screen3, intro_screen4, intro_screen5, intro_screen6, intro_screen7, intro_screen8, intro_screen9, intro_screen10, intro_screen11, intro_screen12]
    current_screen_index = 0
    menu_music_running = True
    intro_music_running = False
    outro_music_running = False
    game_music_running = False
    pygame.mixer.music.load('../audio/mixed_intro2.mp3')
    pygame.mixer.music.play(-1)

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if current_menu == 'menu':
                if outro_music_running:
                    pygame.mixer.music.stop()
                    outro_music_running = False
                if game_music_running:
                    pygame.mixer.music.stop()
                    game_music_running = False
                if not menu_music_running:
                    menu_music_running = True
                    pygame.mixer.music.load('../audio/bg.mp3')
                    pygame.mixer.music.play(-1)     
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
                        intro_screen_timer = 0
                        fade_timer = 0
                        current_screen_index += 1
            elif current_menu == 'end':
                current_menu = end_screen.handle_event(event)

        if current_menu == 'menu':
            menu.draw(screen)
        elif current_menu == 'start':
            start_menu.draw(screen)
        elif current_menu == 'settings':
            settings_menu.draw(screen)
        elif current_menu == 'end':
            end_screen.draw(screen, fade_timer)
            fade_timer = min(255, fade_timer + 2)
            if game_music_running:
                pygame.mixer.music.stop()
                game_music_running = False
            if not outro_music_running:
                pygame.mixer.music.load('../audio/outro_good.mp3')
                pygame.mixer.music.play(-1)
                outro_music_running = True
        elif current_menu == 'intro' and current_screen_index < len(screens):
            screens[current_screen_index].render(screen, fade_timer)
            if menu_music_running:
                pygame.mixer.music.stop()
                menu_music_running = False
            if not intro_music_running:
                pygame.mixer.music.load('../audio/intro.mp3')
                pygame.mixer.music.play(-1)
                intro_music_running = True
            if intro_screen_timer >= 300:
                if fade_timer > 0:
                    fade_timer = max(0, fade_timer-20)
                else:
                    current_screen_index += 1
                    intro_screen_timer = 0
            else:
                intro_screen_timer += 1
                fade_timer = min(255, fade_timer+2)
        elif current_menu == 'intro' and current_screen_index >= len(screens):
            if intro_music_running:
                pygame.mixer.music.stop()
                intro_music_running = False
            game = Game(start_menu.characters[start_menu.selected_character], start_menu.difficulties[start_menu.selected_difficulty], settings_menu.music_volume, settings_menu.game_volume)
            game_music_running = True
            game.run()
            fade_timer = 0
            print("Ended")
            current_menu = game.go_to
            current_screen_index = 0

        pygame.display.flip()
        clock.tick(60)
    sys.exit()

if __name__ == "__main__":
    main()    