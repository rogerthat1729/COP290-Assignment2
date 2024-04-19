import pygame
from settings import *
import time
from tasks import display_task
from start import load_frames, display_bg
from intro import *

class BookTask:
    def __init__(self, level):
        self.book_image = pygame.image.load('../graphics/tasks/books/book.png')
        self.level = level
        self.pages = [[pygame.image.load('../graphics/tasks/cb/cb3.png'), pygame.image.load('../graphics/tasks/cb/cb1.png')],
                       [pygame.image.load('../graphics/tasks/cb/cb4.png'), pygame.image.load('../graphics/tasks/cb/cb1.png')],
                         [pygame.image.load('../graphics/tasks/cb/cb5.png')]] 
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
        self.completed_counter = 0
        self.subtasks_completed = {tree: False for tree in self.trees}
        self.all_subtasks_completed = False

    def check_subtask_completion(self, tree):
        if self.level.interact_time and self.level.check_near_object(tree):
            elapsed_time = time.time() - self.level.interact_time
            if elapsed_time >= self.level.interact_wait:
                self.subtasks_completed[tree] = True
                self.completed_counter += 1
                self.level.interact_time = None

    def update(self):
        for tree in self.trees:
            self.check_subtask_completion(tree)
        self.all_subtasks_completed = all(self.subtasks_completed.values())
        if self.all_subtasks_completed:
            self.level.player.done_task = 1
            self.completed_counter = 0
            self.subtasks_completed = {tree: False for tree in self.trees}
            self.all_subtasks_completed = False
            # print("Walk task completed")

    def render(self):
        for tree in self.trees:
            if self.subtasks_completed[tree]:
                continue
            if self.level.interact_time and self.level.check_near_object(tree):
                display_task(self.level, tree, self.level.interact_time, self.level.interact_wait)
                break