import pygame
from random import choice

good_tasks = ["Talk on phone - type PHONE", "Go to balcony - type BALCONY", "Clean your room - type CLEAN"]
task_to_seq = {"Talk on phone - type PHONE": "PHONE", "Go to balcony - type BALCONY": "BALCONY", "Clean your room - type CLEAN":"CLEAN"}

bad_tasks = [["You browsed through social media for 2 hours.",  "Your happiness is reduced by 10 points."]]

pygame.init()
font = pygame.font.Font(None,30)

def render_tasks(level):
    task_list = level.task_list
    y = 20
    display_surf = level.display_surface
    happy_surf = font.render(f"Happy Index: {int(level.happy)}", True, (0, 255, 0))
    task_rect = happy_surf.get_rect(topleft = (10, y))
    pygame.draw.rect(display_surf,'Black',task_rect)
    display_surf.blit(happy_surf, task_rect)
    y += 40
    for task in task_list:
        task_surface = font.render(task, True, (255, 255, 255))
        display_surf.blit(task_surface, (10, y))
        y += 40
    level.happy = max(0, level.happy-0.01)
    if level.player.done_task==1:
        level.player.textbox_content = ""
        level.task_list.pop(0)
        level.task_list.append(choice(good_tasks))
        level.happy = min(100, level.happy+10)
        level.player.done_task = 0

def render_textbox(task, content, level):
    if not level.player.is_textbox_active:
        return
    screen = level.display_surface
    # Draw the textbox background
    textbox_rect = pygame.Rect(600, 100, 200, 50)
    pygame.draw.rect(screen, (255, 255, 255), textbox_rect)
    border_rect = textbox_rect.copy()
    pygame.draw.rect(screen, (0, 0, 0), border_rect, 3)
    # Render the textbox content
    text_surface = font.render(content, True, (0, 0, 0))
    screen.blit(text_surface, (610, 110))
    if content == task_to_seq[task]:
        level.player.done_task = 1
        level.player.is_textbox_active = False

def show_popup(level, task):
    # bad_task = bad_tasks[0]
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
