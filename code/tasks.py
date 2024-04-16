import pygame
from random import choice
import time
from support import *

good_tasks = ["Take a nap", "Buy groceries", "Clean out the trash", "Do the dishes", "Talk on phone", "Do the laundry", 
              "Read a book", "Take a bath", "Go to balcony"]
task_to_seq = {"Talk on phone": "phone", "Go to balcony": "balcony", "Clean out the trash":"trash", "Take a bath":"bath", "Do the dishes":"sink", 
               "Read a book":"book", 'Do the laundry':"wash", "Buy groceries":'door', "Take a nap":"bed"}
phone_codes = ["69420", "43210", "98543", "87658", "38961"]
task_to_points = {"Talk on phone": 5, "Go to balcony": 10, "Clean out the trash": 5, "Take a bath": 10, "Do the dishes": 15, 
                    "Read a book": 10, 'Do the laundry': 15, 'Buy groceries':10, "Take a nap": 10}

pygame.init()
font = pygame.font.Font('../graphics/font/joystix.ttf',15)
keypad_font2 = pygame.font.Font(None,20)
notes_font = pygame.font.Font(None, 40)

def fade_to_black(level):
    overlay = pygame.Surface(level.display_surface.get_size(), pygame.SRCALPHA)
    color = int(((time.time() - level.interact_time)/level.interact_wait)*255)
    overlay.fill((0, 0, 0, color))  # Semi-transparent black
    level.display_surface.blit(overlay, (0, 0))

def draw_pause_screen(level):
    screen = level.display_surface
    surface = screen.copy()
    amt = 10
    scale = 1.0 / float(amt)
    surf_size = (1600, 880)
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    screen.blit(surf, (0, 0))

def draw_pause_button(level):
    screen = level.display_surface
    if level.paused:
        draw_pause_screen(level)
        pause_text = font.render("Paused.", True, 'white')
        screen.blit(pause_text, (1500, 100))

    pause_image = pygame.image.load('../graphics/ui/pause.png')
    pause_rect = pause_image.get_rect(center=(1550, 50))
    level.pause_rect = pause_rect
    screen.blit(pause_image, pause_rect)


def change_to_task_image(level, task):
    for spr in level.visible_sprites.sprites():
        if spr.sprite_type == 'object' and spr.name==task:
            if level.interact_time:
                spr.active = 2
                spr.update_image()

def play_music(task):
    pygame.mixer.music.load(f'../audio/{task}.mp3')
    pygame.mixer.music.play()

def check_keypad_code(level):
    if level.phone_keypad_content == level.correct_code:
        level.player.done_task = 1
        level.correct_code = choice(phone_codes)
    else:
        level.phone_keypad_content = ""

def draw_health_bar(level):
    screen = level.display_surface
    y = 20
    happy_surf = font.render(f"Mental Health: {level.happy}", True, 'white')
    happy_rect = happy_surf.get_rect(topleft = (10, y))
    screen.blit(happy_surf, happy_rect)
    y += 30
    bar_length = 150
    bar_height = 20
    bar_position = (10, y)
    fill_length = (level.happy / 100) * bar_length
    color = (255, 0, 0)
    if(level.happy > 50):
        color = (255*((100-level.happy)/50),255, 0)
    else:
        color = (255, 255*(level.happy/50), 0)
    if fill_length > 0:
        pygame.draw.rect(screen, color, (bar_position[0], bar_position[1], fill_length, bar_height))
    pygame.draw.rect(screen, 'black', (bar_position[0], bar_position[1], bar_length, bar_height), 3)


def render_tasks(level):
    task_list = level.task_list
    y = 80
    display_surf = level.display_surface
    background_surface = pygame.Surface((250, 450), pygame.SRCALPHA)
    background_surface.fill((0, 0, 0, 64))
    display_surf.blit(background_surface, (10, 10))
    draw_health_bar(level)
    for task in task_list:
        task_surface = font.render(task, True, 'green')
        display_surf.blit(task_surface, (10, y))
        y += 40
    # level.happy = max(0, level.happy-0.01)
    if level.player.done_task==1:
        # play_music(task_to_seq[task_list[0]])\
        pygame.mixer.stop()
        level.player.textbox_content = ""
        level.happy = min(100, level.happy+task_to_points[task_list[0]])
        curr_task = level.task_list[0]
        level.task_list.pop(0)
        good_tasks.pop(good_tasks.index(curr_task))
        level.task_list.append(choice(good_tasks))
        good_tasks.append(curr_task)
        level.player.done_task = 0
        level.player.show_player = True

# def render_textbox(task, content, level):
#     if not level.player.is_textbox_active:
#         return
#     screen = level.display_surface
#     # Draw the textbox background
#     textbox_rect = pygame.Rect(600, 100, 200, 50)
#     pygame.draw.rect(screen, (255, 255, 255), textbox_rect)
#     border_rect = textbox_rect.copy()
#     pygame.draw.rect(screen, (0, 0, 0), border_rect, 3)
#     # Render the textbox content
#     text_surface = font.render(content, True, (0, 0, 0))
#     screen.blit(text_surface, (610, 110))
#     if content == task_to_seq[task] and level.check_near_object(taskobj[task_to_seq[task]]):
#         level.player.done_task = 1
#         level.player.is_textbox_active = False

def check_for_object(list, obj):
    for i in list:
        if i.name == obj:
            return True
    return False

def display_task(level, task, start_time, total_time=3, content=""):
    screen = level.display_surface
    if task=='Talk on phone':
        keypad_image = pygame.image.load('../graphics/tasks/telephone.png')
        keypad_rect = keypad_image.get_rect(center=(700, 400))
        screen.blit(keypad_image, keypad_rect)

        if len(content)==0:
            text_surface = keypad_font2.render("Hint:", True, 'black')
            screen.blit(text_surface, (705, 280))
            text_surface1 = keypad_font2.render("Check the notes", True, 'black')
            screen.blit(text_surface1, (705, 300))
        else:
            text_surface = font.render(content, True, (0, 0, 0))
            screen.blit(text_surface, (725, 280))
    elif task=='Check the notes':
        notes_image = pygame.image.load('../graphics/tasks/notes.png')
        notes_rect = notes_image.get_rect(center=(700, 400))
        screen.blit(notes_image, notes_rect)

        text = notes_font.render("Telephone code", True, 'red')
        text_rect = text.get_rect(center=(700, 350))
        screen.blit(text, text_rect)

        code = notes_font.render(f"{level.correct_code}", True, 'green')
        code_rect = code.get_rect(center=(700, 400))
        screen.blit(code, code_rect)
    else:
        if start_time:
            elapsed_time = time.time() - start_time
            bar_length = 200
            bar_height = 40
            bar_position = (700, 200)
            fill_length = (elapsed_time / total_time) * bar_length

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
                    sink_rect = sink_image.get_rect(center=(800, 400))
                    screen.blit(sink_image, sink_rect)
            elif task=='Do the laundry':
                wm_animations = import_folder('../graphics/tasks/washing_machine')
                frame_index = int((elapsed_time/total_time)*2.999)

                if(frame_index<3):
                    wm_image = wm_animations[frame_index]
                    wm_rect = wm_image.get_rect(center=(800, 450))
                    screen.blit(wm_image, wm_rect)

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
            line_surface = self.font.render(line, True, 'black')
            line_width, line_height = line_surface.get_size()
            width = max(width, line_width)
            height += line_height
        width += 20
        height += 20

        x = 800 - width // 2
        y = 440 - height // 2

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
