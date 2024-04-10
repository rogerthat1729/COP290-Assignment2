import pygame
from random import choice
import time

good_tasks = ["Do the laundry", "Do the dishes", "Read a book", "Take a bath", "Talk on phone", "Go to balcony", "Clean out the trash"]
task_to_seq = {"Talk on phone": "phone", "Go to balcony": "balcony", "Clean out the trash":"trash", "Take a bath":"bath", "Do the dishes":"sink", 
               "Read a book":"book", 'Do the laundry':"wash"}
# taskobj = {"PHONE":"telephone", "BALCONY":"chair", "TRASH":"trashcan", }

pygame.init()
font = pygame.font.Font(None,30)

def play_music(task):
    pygame.mixer.music.load(f'../audio/{task}.mp3')
    pygame.mixer.music.play()

def render_tasks(level):
    task_list = level.task_list
    y = 20
    display_surf = level.display_surface
    happy_surf = font.render(f"Happy Index: {int(level.happy)}", True, (0, 255, 0))
    happy_rect = happy_surf.get_rect(topleft = (10, y))
    pygame.draw.rect(display_surf,'Black',happy_rect)
    display_surf.blit(happy_surf, happy_rect)
    y += 40
    for task in task_list:
        task_surface = font.render(task, True, (255, 0, 0))
        task_rect = task_surface.get_rect(topleft = (10, y))
        pygame.draw.rect(display_surf, 'white', task_rect)
        # pygame.draw.rect(display_surf, 'black', task_rect, 1)
        display_surf.blit(task_surface, (10, y))
        y += 40
    # level.happy = max(0, level.happy-0.01)
    if level.player.done_task==1:
        play_music(task_to_seq[task_list[0]])
        level.player.textbox_content = ""
        level.task_list.pop(0)
        level.task_list.append(choice(good_tasks))
        level.happy = min(100, level.happy+10)
        level.player.done_task = 0

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

def draw_loading_bar(screen, start_time, total_time=3):
    elapsed_time = time.time() - start_time
    bar_length = 200
    bar_height = 40
    bar_position = (700, 200)
    fill_length = (elapsed_time / total_time) * bar_length

    text = font.render("Task Progress", True, 'white')
    text_rect = text.get_rect(center=(bar_position[0] + bar_length / 2, bar_position[1] - 30))
    pygame.draw.rect(screen, 'black', text_rect)
    screen.blit(text, text_rect)

    # Filled part of the bar
    if fill_length > 0:
        pygame.draw.rect(screen, 'green', (bar_position[0], bar_position[1], fill_length, bar_height))
    # Background bar (empty)
    pygame.draw.rect(screen, 'black', (bar_position[0], bar_position[1], bar_length, bar_height), 3)

    if elapsed_time >= total_time:
        return True
    return False

def show_popup(level, task):
    level.player.popup.text = task
    level.player.popup.show(level.display_surface)

class Popup:
    def __init__(self, text, width=300, height=100):
        self.text = text
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)
        self.active = False

    def show(self, screen):
        if not self.active:
            return

        x = (screen.get_width() - self.width) // 2
        y = (screen.get_height() - self.height) // 2

        popup_rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, (255, 255, 255), popup_rect)
        border = popup_rect.copy()
        pygame.draw.rect(screen, (0, 0, 0), border, 3)

        y_offset = 5
        for line in self.text:
            line_surface = font.render(line, True, 'black')
            screen.blit(line_surface, (x, y+y_offset))
            y_offset += font.get_linesize()

    def toggle(self):
        self.active = not self.active
