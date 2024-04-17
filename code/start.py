import pygame
import sys
from settings import *

pygame.init()
FONT = pygame.font.Font("../graphics/font/joystix.ttf", 24)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)

mid_width = 910
mid_height = 490

def draw_text(text, font, color, surface, x, y, offset=4):
    textobj = font.render(text, True, color)
    textobj1 = font.render(text, True, 'black')
    textrect = textobj.get_rect()
    textrect1 = textobj1.get_rect()
    textrect.topleft = (x, y)
    textrect1.topleft = (x-offset, y-offset)
    surface.blit(textobj1, textrect1)
    surface.blit(textobj, textrect)


def draw_button(text, rect, color, surface):
    # pygame.draw.rect(surface, color, rect)
    draw_text(text, FONT, color, surface, rect.x + 20, rect.y + 10, 2)

def draw_title(text, surface):
    draw_text(text, pygame.font.Font("../graphics/font/joystix.ttf", 75), (255, 255, 0), surface, mid_width-230, 100)


class Menu:
    def __init__(self):
        self.current_menu = 'main'
        self.menus = {
            'main': ['Start', 'Settings', 'Exit'],
            'start': ['Choose Character', 'Difficulty', 'Start Game'],
            'settings': ['Music Volume', 'In-game Volume']
        }
        self.buttons = {key: [] for key in self.menus}
        self.create_buttons()

    def create_buttons(self):
        for menu_name, options in self.menus.items():
            y = 400
            for option in options:
                rect = pygame.Rect(mid_width-50, y, 200, 50)
                self.buttons[menu_name].append((option, rect))
                y += 60

    def draw(self, surface):
        pygame.display.set_caption("Petrichor")
        bg = pygame.image.load('../graphics/ui/bg.png')
        surface.blit(bg, (0, 0))
        draw_title("Petrichor", surface)
        draw_text("Main Menu", pygame.font.Font("../graphics/font/joystix.ttf", 48), 'white', surface, mid_width-130, 250)
        for text, rect in self.buttons[self.current_menu]:
            draw_button(text, rect, 'yellow', surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for text, rect in self.buttons[self.current_menu]:
                if rect.collidepoint(pos):
                    if text == 'Exit':
                        pygame.quit()
                        sys.exit()
                    return text.lower()

class StartMenu(Menu):
    def __init__(self):
        self.character_images = [pygame.image.load('../graphics/player1/down_idle/idle_down.png'), pygame.image.load('../graphics/player2/down_idle/idle_down.png')]
        self.characters = ['character1', 'character2']
        self.difficulties = ['Easy', 'Medium', 'Hard']
        self.selected_character = 0
        self.selected_difficulty = 0
        self.start_game_rect = pygame.Rect(mid_width-60, 670, 230, 50)
        self.back_rect = pygame.Rect(mid_width, 750, 120, 50)

        # Load images and set positions
        self.character_positions = [(mid_width-170, 400), (mid_width+230, 400)]
        self.difficulty_positions = [(mid_width-200, 580), (mid_width, 580), (mid_width+200, 580)]

    def draw(self, surface):
        # pygame.display.set_caption("Petrichor")
        bg = pygame.image.load('../graphics/ui/bg.png')
        surface.blit(bg, (0, 0))
        draw_title("Petrichor", surface)
        draw_text("Start Menu", pygame.font.Font("../graphics/font/joystix.ttf", 48), 'white', surface, mid_width-130, 250)
        self.draw_characters(surface)
        self.draw_difficulties(surface)
        self.draw_buttons(surface)

    def draw_characters(self, surface):
        # char_text = FONT.render("Select Character", True, (255, 255, 255))
        # surface.blit(char_text, (mid_width-90, 350))
        draw_text("Select Character", FONT, 'white', surface, mid_width-90, 350, 2)
        for i, image in enumerate(self.character_images):
            rect = pygame.Rect(*self.character_positions[i], image.get_width(), image.get_height())
            if i == self.selected_character:
                pygame.draw.rect(surface, 'yellow', rect)  # Draw a red rectangle around the selected character
            surface.blit(image, rect.topleft)

    def draw_difficulties(self, surface):
        # diff_text = FONT.render("Select Difficulty", True, (255, 255, 255))
        # surface.blit(diff_text, (mid_width-100, 530))
        draw_text("Select Difficulty", FONT, 'white', surface, mid_width-100, 530, 2)
        for i, difficulty in enumerate(self.difficulties):
            text = FONT.render(difficulty, True, (255, 255, 255))
            text_rect = text.get_rect()
            rect = pygame.Rect(*self.difficulty_positions[i], text_rect.width, text_rect.height)
            if i == self.selected_difficulty:
                pygame.draw.rect(surface, 'brown', rect)
            # surface.blit(text, rect.topleft)
            draw_text(difficulty, FONT, 'white', surface, rect.x, rect.y, 2)
    
    def draw_buttons(self, surface):
        draw_button('Start Game', self.start_game_rect, 'yellow', surface)
        draw_button('Back', self.back_rect, 'yellow', surface)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check character selection
            for i, pos in enumerate(self.character_positions):
                rect = pygame.Rect(*pos, self.character_images[i].get_width(), self.character_images[i].get_height())
                if rect.collidepoint(event.pos):
                    self.selected_character = i

            # Check difficulty selection
            for i, pos in enumerate(self.difficulty_positions):
                rect = pygame.Rect(*pos, 100, 30)
                if rect.collidepoint(event.pos):
                    self.selected_difficulty = i

            if self.start_game_rect.collidepoint(event.pos):
                return "intro"
            
            if self.back_rect.collidepoint(event.pos):
                return "menu"
            
        return "start"

class SettingsMenu(Menu):
    def __init__(self):
        self.music_volume = 50  # Default volume
        self.game_volume = 50  # Default volume
        # self.slider_positions = {'music': (mid_width, 350), 'game': (mid_width, 450)}
        self.sliders = {'music': pygame.Rect(mid_width-20, 450, 200, 20), 'game': pygame.Rect(mid_width-20, 550, 200, 20)}
        self.back_rect = pygame.Rect(mid_width, 650, 120, 50) 

    def draw(self, surface):
        bg = pygame.image.load('../graphics/ui/bg.png')
        surface.blit(bg, (0, 0))
        draw_title("Petrichor", surface)
        draw_text("Settings Menu", pygame.font.Font("../graphics/font/joystix.ttf", 48), 'white', surface, mid_width-180, 250)
        # Draw each slider
        # music_text = FONT.render("Music Volume", True, (255, 255, 255))
        # game_text = FONT.render("In-game Volume", True, (255, 255, 255))
        # surface.blit(music_text, (mid_width-50, 400))
        # surface.blit(game_text, (mid_width-70, 500))
        draw_text("Music Volume", FONT, 'white', surface, mid_width-50, 400, 2)
        draw_text("In-game Volume", FONT, 'white', surface, mid_width-70, 500, 2)
        for key, rect in self.sliders.items():
            pygame.draw.rect(surface, GRAY, rect)  # The slider background
            pygame.draw.rect(surface, WHITE, (rect.x, rect.y, self.music_volume if key == 'music' else self.game_volume, rect.height))  # The volume level

        # Draw back button
        draw_button("Back", self.back_rect, 'yellow', surface)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # Check if a slider is clicked and adjust volume
            for key, rect in self.sliders.items():
                if rect.collidepoint(pos):
                    if key == 'music':
                        self.music_volume = pos[0] - rect.x
                        pygame.mixer.music.set_volume(self.music_volume/100)
                    elif key == 'game':
                        self.game_volume = pos[0] - rect.x

            if self.back_rect.collidepoint(pos):
                return "menu"
        return "settings"

