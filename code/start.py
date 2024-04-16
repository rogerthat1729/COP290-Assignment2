import pygame
import sys
from settings import *

FONT = pygame.font.Font("../graphics/font/joystix.ttf", 18)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_button(text, rect, color, surface):
    pygame.draw.rect(surface, color, rect)
    draw_text(text, FONT, 'white', surface, rect.x + 20, rect.y + 10)


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
            y = 100
            for option in options:
                rect = pygame.Rect(750, y, 200, 50)
                self.buttons[menu_name].append((option, rect))
                y += 60

    def draw(self, surface):
        for text, rect in self.buttons[self.current_menu]:
            draw_button(text, rect, 'grey', surface)

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
        self.start_game_rect = pygame.Rect(700, 400, 200, 50)
        self.back_rect = pygame.Rect(700, 500, 100, 50)

        # Load images and set positions
        self.character_positions = [(550, 150), (950, 150)]
        self.difficulty_positions = [(550, 300), (750, 300), (950, 300)]

    def draw(self, surface):
        self.draw_characters(surface)
        self.draw_difficulties(surface)
        self.draw_buttons(surface)

    def draw_characters(self, surface):
        char_text = FONT.render("Select Character", True, (255, 255, 255))
        surface.blit(char_text, (700, 100))
        for i, image in enumerate(self.character_images):
            rect = pygame.Rect(*self.character_positions[i], image.get_width(), image.get_height())
            surface.blit(image, rect.topleft)
            if i == self.selected_character:
                pygame.draw.rect(surface, (255, 0, 0), rect, 3)  # Draw a red rectangle around the selected character

    def draw_difficulties(self, surface):
        diff_text = FONT.render("Select Difficulty", True, (255, 255, 255))
        surface.blit(diff_text, (700, 250))
        for i, difficulty in enumerate(self.difficulties):
            text = FONT.render(difficulty, True, (255, 255, 255))
            rect = pygame.Rect(*self.difficulty_positions[i], 100, 30)
            surface.blit(text, rect.topleft)
            if i == self.selected_difficulty:
                pygame.draw.rect(surface, (255, 0, 0), rect, 3)
    
    def draw_buttons(self, surface):
        draw_button('Start Game', self.start_game_rect, 'grey', surface)
        draw_button('Back', self.back_rect, 'grey', surface)
    
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
        self.slider_positions = {'music': (750, 150), 'game': (750, 250)}
        self.sliders = {'music': pygame.Rect(750, 150, 200, 20), 'game': pygame.Rect(750, 250, 200, 20)}
        self.back_rect = pygame.Rect(700, 350, 100, 50) 

    def draw(self, surface):
        # Draw each slider
        music_text = FONT.render("Music Volume", True, (255, 255, 255))
        game_text = FONT.render("In-game Volume", True, (255, 255, 255))
        surface.blit(music_text, (700, 100))
        surface.blit(game_text, (700, 200))
        for key, rect in self.sliders.items():
            pygame.draw.rect(surface, GRAY, rect)  # The slider background
            pygame.draw.rect(surface, WHITE, (rect.x, rect.y, self.music_volume if key == 'music' else self.game_volume, rect.height))  # The volume level

        # Draw back button
        draw_button("Back", self.back_rect, GRAY, surface)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # Check if a slider is clicked and adjust volume
            for key, rect in self.sliders.items():
                if rect.collidepoint(pos):
                    if key == 'music':
                        self.music_volume = pos[0] - rect.x
                    elif key == 'game':
                        self.game_volume = pos[0] - rect.x

            # Check if the back button is clicked
            if self.back_rect.collidepoint(pos):
                return "menu"
        return "settings"  # Assuming the game class can manage which menu is active


