import pygame
from random import choice
import time

good_tasks = ["Talk on phone", "Do the laundry", "Do the dishes", "Read a book", "Take a bath", "Go to balcony", "Clean out the trash"]
task_to_seq = {"Talk on phone": "phone", "Go to balcony": "balcony", "Clean out the trash":"trash", "Take a bath":"bath", "Do the dishes":"sink", 
               "Read a book":"book", 'Do the laundry':"wash"}
# taskobj = {"PHONE":"telephone", "BALCONY":"chair", "TRASH":"trashcan", }
phone_codes = ["69420", "43210", "98543", "87658", "38961"]

pygame.init()
font = pygame.font.Font(None,30)
keypad_font2 = pygame.font.Font(None,20)
notes_font = pygame.font.Font(None, 40)

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
    background_surface = pygame.Surface((200, 350), pygame.SRCALPHA)
    background_surface.fill((0, 0, 0, 64))
    display_surf.blit(background_surface, (10, 10))
    draw_health_bar(level)
    for task in task_list:
        task_surface = font.render(task, True, 'green')
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
