import pygame
from random import choice

all_tasks = ["Talk on phone", "Go to balcony", "Clean your room"]
task_to_seq = {"Talk on phone": "PHONE", "Go to balcony": "BALCONY", "Clean your room":"CLEAN"}
pygame.init()
font = pygame.font.Font(None,30)

def render_tasks(level):
    task_list = level.task_list
    y = 20
    display_surf = pygame.display.get_surface()
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
        level.task_list.append(choice(all_tasks))
        level.happy = min(100, level.happy+5)
        level.player.done_task = 0

def render_textbox(task, content, level):
    if not level.player.is_textbox_active:
        return
    screen = pygame.display.get_surface()
    # Draw the textbox background
    textbox_rect = pygame.Rect(600, 100, 200, 50)
    pygame.draw.rect(screen, (255, 255, 255), textbox_rect)
    # Render the textbox content
    text_surface = font.render(content, True, (0, 0, 0))
    screen.blit(text_surface, (610, 110))
    if content == task_to_seq[task]:
        level.player.done_task = 1
