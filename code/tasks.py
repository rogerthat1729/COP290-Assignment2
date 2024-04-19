import pygame
from random import choice
import time
import sys
from support import *
from settings import *
from start import *
from intro import *
from dictionaries import *

FONT = pygame.font.Font("../graphics/font/joystix.ttf", 24)
GRAY = (200, 200, 200)

pygame.init()
font = pygame.font.Font('../graphics/font/joystix.ttf',18)
keypad_font2 = pygame.font.Font(None,20)
notes_font = pygame.font.Font(None, 40)

def fade_to_black(level):
    if level.interact_time:
        overlay = pygame.Surface(level.display_surface.get_size(), pygame.SRCALPHA)
        color = min(255, int(((time.time() - level.interact_time)/level.interact_wait)*255))
        
        overlay.fill((0, 0, 0, color))
        level.display_surface.blit(overlay, (0, 0))

def draw_pause_screen(level):
    screen = level.display_surface
    surface = screen.copy()
    amt = 10
    scale = 1.0 / float(amt)
    surf_size = (WIDTH, HEIGHT)
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    screen.blit(surf, (0, 0))

    resume_button = Button((WIDTH - 200) // 2, HEIGHT // 2 - 100, 200, 50, "Resume", 'green')
    main_menu_button = Button((WIDTH - 200) // 2, HEIGHT // 2, 200, 50, "Main Menu", 'green')
    exit_button = Button((WIDTH - 200) // 2, HEIGHT // 2 + 100, 200, 50, "Exit", 'red')

    resume_button.draw(level.display_surface)
    main_menu_button.draw(level.display_surface)
    exit_button.draw(level.display_surface)

    if level.paused:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.is_clicked(event.pos):
                    level.paused = False
                elif main_menu_button.is_clicked(event.pos):
                    level.go_to_menu = True
                elif exit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

def draw_pause_button(level):
    screen = level.display_surface
    if level.paused:
        draw_pause_screen(level)
        pause_text = font.render("Paused.", True, 'white')
        screen.blit(pause_text, (WIDTH-100, 100))

    pause_image = pygame.image.load('../graphics/ui/pause.png')
    pause_rect = pause_image.get_rect(center=(WIDTH-50, 50))
    level.pause_rect = pause_rect
    screen.blit(pause_image, pause_rect)


def change_to_task_image(level, task):
    if task == 'bed':
        for spr in level.visible_sprites.sprites():
            if spr.sprite_type == 'object' and spr.name==task:
                if level.interact_time:
                    spr.active = 2
                    spr.update_image()

def play_music(task, level):
    if task != 'Take a walk':
        pygame.mixer.music.set_volume(level.game_volume/100)
        pygame.mixer.music.load(f'../audio/{task}.mp3')
        pygame.mixer.music.play()

def check_keypad_code(level):
    if level.phone_keypad_content == level.correct_code:
        level.player.done_task = 1
        level.correct_code = choice(phone_codes)
    else:
        level.phone_keypad_content = ""

def draw_health_bar(level, text, pos):
    screen = level.display_surface
    current_level = int(level.happy)
    current_text = f"Mental Health: {current_level}"
    if text == "recovery":
        current_level = int(level.recovery)
        current_text = f"Recovery: {current_level}"
    y = pos
    happy_surf = font.render(current_text, True, 'white')
    happy_rect = happy_surf.get_rect(topleft = (10, y))
    screen.blit(happy_surf, happy_rect)
    y += 30
    bar_length = 200
    bar_height = 20
    bar_position = (10, y)
    fill_length = (current_level / 100) * bar_length
    color = (255, 0, 0)
    if(current_level > 50):
        color = (255*((100-current_level)/50),255, 0)
    else:
        color = (255, 255*(current_level/50), 0)
    if fill_length > 0:
        pygame.draw.rect(screen, color, (bar_position[0], bar_position[1], fill_length, bar_height))
    pygame.draw.rect(screen, 'black', (bar_position[0], bar_position[1], bar_length, bar_height), 3)


def render_tasks(level):
    task_list = level.task_list
    y = 170
    display_surf = level.display_surface
    background_surface = pygame.Surface((300, 600), pygame.SRCALPHA)
    background_surface.fill((0, 0, 0, 96))
    display_surf.blit(background_surface, (10, 10))
    draw_health_bar(level, "recovery", 20)
    draw_health_bar(level, "mentalhealth", 90)
    for task in task_list:
        txt = task
        if task == 'Take a walk':
            txt = task + f" ({level.walktask.completed_counter}/4)"
        task_surface = font.render(txt, True, 'green')
        display_surf.blit(task_surface, (10, y))
        y += 40
    if level.player.done_task==1:
        level.handle_music(2)
        level.player.textbox_content = ""
        prev = level.happy
        level.happy = min(100, level.happy+task_to_points[task_list[0]])
        if prev < 75 and level.happy >= 75:
            level.game_music_running = 1
        curr_task = level.task_list[0]
        level.task_list.pop(0)
        good_tasks.pop(good_tasks.index(curr_task))
        level.task_list.append(choice(good_tasks))
        good_tasks.append(curr_task)
        level.player.done_task = 0
        level.player.show_player = True

def render_controls(level): 
    task = level.task_list[0]
    controls = task_to_controls[task]
    display_surf = level.display_surface
    height = 80 + 20*len(controls)
    y = HEIGHT - height - 200
    background_surface = pygame.Surface((530, height), pygame.SRCALPHA)
    background_surface.fill((0, 0, 0, 96))
    display_surf.blit(background_surface, (WIDTH-580, y))
    y += 10
    txt_surface = font.render("Controls", True, 'green')
    display_surf.blit(txt_surface, (WIDTH-570, y))
    y += 30
    controls_font = pygame.font.Font("../graphics/font/joystix.ttf", 18)
    move_surface = controls_font.render('Use "WASD" to move', True, 'yellow')
    display_surf.blit(move_surface, (WIDTH-570, y))
    y += 20
    for control in controls:
        control_surface = controls_font.render(control, True, 'yellow')
        display_surf.blit(control_surface, (WIDTH-570, y))
        y += 20
    y += 32
    keyboard_image = pygame.image.load('../graphics/ui/keyboard/keyboard1.png')
    if len(controls)==4:
        keyboard_image = pygame.image.load('../graphics/ui/keyboard/keyboard2.png')
    elif len(controls)==5:
        keyboard_image = pygame.image.load('../graphics/ui/keyboard/keyboard3.png')
    keyboard_surf = pygame.transform.scale(keyboard_image, (573, 168))
    display_surf.blit(keyboard_surf, (WIDTH-580, y))

def check_for_object(list, obj):
    for i in list:
        if i and i.name == obj:
            return True
    return False

def display_task(level, task, start_time, total_time=3, content=""):
    screen = level.display_surface
    if task=='Talk on phone':
        keypad_image = pygame.image.load('../graphics/tasks/telephone.png')
        keypad_rect = keypad_image.get_rect(center=((700/1600)*WIDTH, (380/880)*HEIGHT))
        screen.blit(keypad_image, keypad_rect)

        if len(content)==0:
            text_surface = keypad_font2.render("Hint:", True, 'black')
            screen.blit(text_surface, ((705/1600)*WIDTH, (280/880)*HEIGHT))
            text_surface1 = keypad_font2.render("Check the notes", True, 'black')
            screen.blit(text_surface1, ((705/1600)*WIDTH, (300/880)*HEIGHT))
        else:
            text_surface = font.render(content, True, (0, 0, 0))
            screen.blit(text_surface, ((715/1600)*WIDTH, (280/880)*HEIGHT))

    elif task=='Check the notes':
        notes_image = pygame.image.load('../graphics/tasks/notes.png')
        notes_rect = notes_image.get_rect(center=((700/1600)*WIDTH, (400/880)*HEIGHT))
        screen.blit(notes_image, notes_rect)

        text = notes_font.render("Telephone code", True, 'red')
        text_rect = text.get_rect(center=((700/1600)*WIDTH, (350/880)*HEIGHT))
        screen.blit(text, text_rect)

        code = notes_font.render(f"{level.correct_code}", True, 'green')
        code_rect = code.get_rect(center=((700/1600)*WIDTH, (400/880)*HEIGHT))
        screen.blit(code, code_rect)
    else:
        if start_time:
            elapsed_time = time.time() - start_time
            bar_length = 200
            bar_height = 40
            bar_position = ((700/1600)*WIDTH, (200/880)*HEIGHT)
            fill_length = (elapsed_time / total_time) * bar_length

            if task=='tree4' and level.walktask.completed_counter==3:
                display_bg(level, screen, level.walk_animations)
                draw_text("Rosa cleared her head after this walk", pygame.font.Font("../graphics/font/joystix.ttf", 48), '#d4e157', screen, 300, 450, offset=2)

            text = font.render("Task Progress", True, 'white')
            text_rect = text.get_rect(center=(bar_position[0] + bar_length / 2, bar_position[1] - 30))
            pygame.draw.rect(screen, 'black', text_rect)
            screen.blit(text, text_rect)

            if fill_length > 0:
                pygame.draw.rect(screen, 'green', (bar_position[0], bar_position[1], fill_length, bar_height))
            pygame.draw.rect(screen, 'black', (bar_position[0], bar_position[1], bar_length, bar_height), 3)
        
            if task=='Do the dishes':
                sink_animations = import_folder('../graphics/tasks/sink')
                frame_index = int((elapsed_time/total_time)*4.999)

                if(frame_index<5):
                    sink_image = sink_animations[frame_index]
                    sink_rect = sink_image.get_rect(center=((800/1600)*WIDTH, (400/880)*HEIGHT))
                    screen.blit(sink_image, sink_rect)

            elif task=='Do the laundry':
                wm_animations = import_folder('../graphics/tasks/washing_machine')
                frame_index = int((elapsed_time/total_time)*2.999)

                if(frame_index<3):
                    wm_image = wm_animations[frame_index]
                    wm_rect = wm_image.get_rect(center=((800/1600)*WIDTH, (450/880)*HEIGHT))
                    screen.blit(wm_image, wm_rect)
            
            elif task=='Organize the shelf':
                shelf_animations = import_folder('../graphics/tasks/shelf')
                frame_index = int((elapsed_time/total_time)*4.999)

                if(frame_index<5):
                    shelf_image = shelf_animations[frame_index]
                    shelf_image = pygame.transform.scale(shelf_image, (400, 400))
                    shelf_rect = shelf_image.get_rect(center=((800/1600)*WIDTH, (450/880)*HEIGHT))
                    screen.blit(shelf_image, shelf_rect)

            if elapsed_time >= total_time:
                return True
            return False
        
def show_popup(level, task):
    level.player.popup.show(task, level.display_surface)

class Popup:
    def __init__(self, text, width=100, height=20):
        self.text = text
        self.font = pygame.font.Font('../graphics/font/merchant.ttf', 36)
        self.active = False

    def show(self, text, screen):
        if not self.active:
            return
        
        width = 0
        height = 0

        self.text = text
        for line in self.text:
            line_surface = self.font.render(line, True, 'white')
            line_width, line_height = line_surface.get_size()
            width = max(width, line_width)
            height += line_height
        width += 20
        height += 20

        x = 960 - width // 2
        y = 340 - height // 2

        popup_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, 'white', popup_rect)
        border = popup_rect.copy()
        pygame.draw.rect(screen, 'black', border, 3)

        y += 10
        for line in self.text:
            line_surface = self.font.render(line, True, 'black')
            screen.blit(line_surface, (x+10, y))
            y += line_surface.get_size()[1]

    def toggle(self):
        self.active = not self.active


class Button:
    def __init__(self, x, y, width, height, text, color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action
        self.font = pygame.font.Font("../graphics/font/joystix.ttf", 30)

    def draw(self, screen):
        draw_text(self.text, self.font, self.color, screen, self.rect.x, self.rect.y, 2)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)