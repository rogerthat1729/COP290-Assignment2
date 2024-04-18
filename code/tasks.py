import pygame
from random import choice
import time
import sys
from support import *
from settings import *
from start import *

good_tasks = ["Take a walk", "Organize the shelf", "Read a book", "Take a nap", "Buy groceries", 
              "Clean out the trash", "Do the dishes", "Do the laundry", 
               "Take a bath", "Go to balcony", "Talk on phone"]
task_to_seq = {"Talk on phone": "phone", "Go to balcony": "balcony", "Clean out the trash":"trash", "Take a bath":"bath", 
               "Do the dishes":"sink", "Read a book":"book", 'Do the laundry':"wash", "Buy groceries":'door', 
               "Take a nap":"bed", "Take a walk":['tree1', 'tree2', 'tree3', 'tree4'], "Organize the shelf":"shelf"}
phone_codes = ["69420", "43210", "98543", "87658", "38961"]
task_to_points = {"Talk on phone": 5, "Go to balcony": 10, "Clean out the trash": 5, "Take a bath": 10, "Do the dishes": 15, 
                    "Read a book": 10, 'Do the laundry': 15, 'Buy groceries':10, "Take a nap": 10, 
                    'Take a walk':30, 'Organize the shelf':10}
bad_tasks = {1:["You browsed through social media for 2 hours.",  "Your mental health is reduced by 10 points."],
			2:["You ate a lot of junk food.", "Your mental health is reduced by 10 points."],
			3:["You watched TV for 3 hours", "Your mental health is reduced by 15 points"],
			4:["You overthought about your bad grade", "Your mental health is reduced by 15 points"],
			5: ["You stayed in bed all day and didn't talk to anyone", "Your mental health is reduced by 20 points"]}
happiness_reduced = {1:10, 2:10, 3:15, 4:15, 5:20}
task_to_obj = {"Talk on phone":'telephone', "Go to balcony":'chair', "Clean out the trash":'trashcan',
			    "Take a bath":'bathtub', "Do the dishes":'sink', "Read a book":'books',
				'Do the laundry':'washing_machine', "Buy groceries":'door', 'Take a nap':'bed',
				"Organize the shelf":'shelf', "Take a walk":['tree1', 'tree2', 'tree3', 'tree4']}

task_to_controls = {"Talk on phone":['Press "P" to open the keypad', 'Use number keys to type the code', 'Press "Enter" to enter the code', 'Press "Backspace" to remove last digit'],
					 "Go to balcony":['Hold "I" to relax'],
					 "Clean out the trash":['Hold "I" to clean out the trash'],
					 "Take a bath":['Hold "I" to take a bath'],
					 "Do the dishes":['Hold "I" to do the dishes'],
					 "Read a book":['Press "B" to open the book', "Use arrow keys to navigate", 'Use number keys to type the code', 'Press "Enter" to enter the code', 'Press "Backspace" to remove last digit'],
					 "Do the laundry":['Hold "I" to do the laundry'],
					 "Buy groceries":['Hold "I" to buy groceries'],
					 "Take a nap":['Hold "I" to take a nap'],
					 "Organize the shelf":['Hold "I" to organize the shelf'],
					 "Take a walk":['Hold "I" at each of the four trees']
					 }


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
        task_surface = font.render(task, True, 'green')
        display_surf.blit(task_surface, (10, y))
        y += 40
    # level.happy = max(0, level.happy-0.01)
    if level.player.done_task==1:
        level.handle_music(2)
        level.player.textbox_content = ""
        level.happy = min(100, level.happy+task_to_points[task_list[0]])
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
    background_surface = pygame.Surface((400, height), pygame.SRCALPHA)
    background_surface.fill((0, 0, 0, 96))
    display_surf.blit(background_surface, (WIDTH-410, y))
    y += 10
    txt_surface = font.render("Controls", True, 'green')
    display_surf.blit(txt_surface, (WIDTH-400, y))
    y += 30
    controls_font = pygame.font.Font("../graphics/font/joystix.ttf", 12)
    move_surface = controls_font.render('Use "WASD" to move', True, 'yellow')
    display_surf.blit(move_surface, (WIDTH-400, y))
    y += 20
    for control in controls:
        control_surface = controls_font.render(control, True, 'yellow')
        display_surf.blit(control_surface, (WIDTH-400, y))
        y += 20

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
        # pygame.draw.rect(screen, self.color, self.rect)
        draw_text(self.text, self.font, self.color, screen, self.rect.x, self.rect.y, 2)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class BookTask:
    def __init__(self, level):
        self.book_image = pygame.image.load('../graphics/tasks/books/book.png')
        self.level = level
        self.pages = [[pygame.image.load('../graphics/tasks/cb/cb3.png'), pygame.image.load('../graphics/tasks/cb/cb1.png')],
                       [pygame.image.load('../graphics/tasks/cb/cb4.png'), pygame.image.load('../graphics/tasks/cb/cb1.png')],
                         [pygame.image.load('../graphics/tasks/cb/cb5.png')]] # Example pages
        self.current_page = 0
        self.active = False
        self.code = "31415"
        self.user_input = ""
        self.font = pygame.font.Font("../graphics/font/joystix.ttf", 14)

    def start(self):
        self.active = True

    def render(self):
        if not self.active:
            return
        # Render the book image with text
        self.level.display_surface.blit(self.book_image, (WIDTH // 2 - self.book_image.get_width() // 2, HEIGHT // 2 - self.book_image.get_height() // 2))
        
        if self.current_page == 0:
            img1 = pygame.transform.scale(self.pages[0][0], (170, 170))
            img2 = pygame.transform.scale(self.pages[0][1], (200, 200))
            self.level.display_surface.blit(img1, (WIDTH // 2 - 230, HEIGHT // 2 - 80))
            self.level.display_surface.blit(img2, (WIDTH // 2 - 10, HEIGHT // 2 - 100))
        elif self.current_page == 1:
            img1 = pygame.transform.scale(self.pages[1][0], (200, 200))
            img2 = pygame.transform.scale(self.pages[1][1], (200, 200))
            self.level.display_surface.blit(img1, (WIDTH // 2 - 250, HEIGHT // 2 - 100))
            self.level.display_surface.blit(img2, (WIDTH // 2 - 10, HEIGHT // 2 - 100))
        else:
            img1 = pygame.transform.scale(self.pages[2][0], (200, 200))
            self.level.display_surface.blit(img1, (WIDTH // 2 - 250, HEIGHT // 2 - 100))

            text1 = self.font.render("Enter the code:", True, 'black')
            self.level.display_surface.blit(text1, (WIDTH // 2, HEIGHT // 2 - 50))

            pygame.draw.rect(self.level.display_surface, 'white', (WIDTH // 2 + 10, HEIGHT // 2, 150, 30))
            pygame.draw.rect(self.level.display_surface, 'black', (WIDTH // 2 + 10, HEIGHT // 2, 150, 30), 2)
            input_surface = self.font.render(self.user_input, True, (0, 0, 0))
            self.level.display_surface.blit(input_surface, (WIDTH // 2 + 15, HEIGHT // 2 + 5))
        
    def render_text(self):
        y = HEIGHT//2 - self.book_image.get_height()//2 + 90
        x = WIDTH//2 - self.book_image.get_width()//2 + 100
        #resize image to 100 x 200
        pg_image = pygame.transform.scale(self.pages[self.current_page], (100, 200))
        # for line in self.pages[self.current_page]:
        #     #resize image to 100 x 200
        #     # text_surface = self.font.render(line, True, 'black')
        #     # self.level.display_surface.blit(text_surface, (x, y))
        #     y += text_surface.get_height() + 5

    def handle_input(self, event):
        if not self.active:
            self.current_page = 0
            self.user_input = ""
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if self.current_page < len(self.pages) - 1:
                    self.current_page += 1
            elif event.key == pygame.K_LEFT:
                if self.current_page > 0:
                    self.current_page -= 1
            elif event.key == pygame.K_ESCAPE:
                self.active = False
                self.current_page = 0
                self.user_input = ""
            elif event.key == pygame.K_RETURN and self.current_page == len(self.pages) - 1:
                if self.user_input == self.code:
                    self.level.player.done_task = 1
                    print("Task completed")
                else:
                    print("Incorrect code")
                self.current_page = 0
                self.user_input = ""
                self.active = False
            elif event.unicode.isnumeric():
                if len(self.user_input) < 5 and self.current_page == len(self.pages) - 1:
                    self.user_input += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                if len(self.user_input) > 0:
                    self.user_input = self.user_input[:-1]


class WalkTask:
    def __init__(self, level):
        self.level = level
        self.trees = ['tree1', 'tree2', 'tree3', 'tree4']
        self.subtasks_completed = {tree: False for tree in self.trees}
        self.all_subtasks_completed = False

    def check_subtask_completion(self, tree):
        if self.level.interact_time and self.level.check_near_object(tree):
            elapsed_time = time.time() - self.level.interact_time
            if elapsed_time >= self.level.interact_wait:
                self.subtasks_completed[tree] = True
                self.level.interact_time = None # Reset interaction time

    def update(self):
        for tree in self.trees:
            self.check_subtask_completion(tree)
        self.all_subtasks_completed = all(self.subtasks_completed.values())
        if self.all_subtasks_completed:
            self.level.player.done_task = 1
            print("Walk task completed")

    def render(self):
        for tree in self.trees:
            if self.subtasks_completed[tree]:
                continue
            if self.level.interact_time and self.level.check_near_object(tree):
                display_task(self.level, tree, self.level.interact_time, self.level.interact_wait)
                break