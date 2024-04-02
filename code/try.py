import pygame
import sys

pygame.init()

# Screen dimensions and settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Task List Game")
font = pygame.font.Font(None, 36)

# Initial tasks and player index
tasks = ["Task 1: Collect coins", "Task 2: Defeat enemies"]
player_x_index = 0

def render_tasks(tasks, y=50):
    for task in tasks:
        task_surface = font.render(task, True, (255, 255, 255))
        screen.blit(task_surface, (50, y))
        y += 40

def update_player_index():
    global player_x_index
    player_x_index += 1  # Modify this logic as needed for your game

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Example task completion condition
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if tasks:
                    tasks.pop(0)  # Remove the first task
                    update_player_index()  # Update player's index
                    tasks.append(f"New Task: {len(tasks)+1}")  # Add a new task

    screen.fill((0, 0, 0))  # Clear screen with black
    render_tasks(tasks)  # Render updated task list
    pygame.display.flip()  # Update the screen

    pygame.time.wait(100)  # Wait a bit before the next loop iteration

pygame.quit()
sys.exit()
