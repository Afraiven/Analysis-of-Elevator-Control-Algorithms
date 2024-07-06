import time
import pygame
import os
import sys

time_step = 0.01
os.environ['SDL_VIDEO_WINDOW_POS'] = '30,30'

pygame.init()
screen = pygame.display.set_mode((300, 700))
pygame.display.set_caption('Elevator')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)

def draw_multiline_text(surface, text, pos, font, color):
    x, y = pos
    line_spacing = font.get_linesize()
    for line in text.split('\n'):
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y))
        y += line_spacing

def draw_stick_figure(surface, x, y, number=None):
    # Head
    pygame.draw.circle(surface, (255, 0, 0), (x, y), 5)
    # Body
    pygame.draw.line(surface, (255, 0, 0), (x, y + 5), (x, y + 20), 2)
    # Arms
    pygame.draw.line(surface, (255, 0, 0), (x - 5, y + 10), (x + 5, y + 10), 2)
    # Legs
    pygame.draw.line(surface, (255, 0, 0), (x, y + 20), (x - 5, y + 30), 2)
    pygame.draw.line(surface, (255, 0, 0), (x, y + 20), (x + 5, y + 30), 2)
    # Number above head
    if number is not None:
        number_surface = font.render(str(number), True, (255, 0, 0))
        surface.blit(number_surface, (x+55- number_surface.get_width() // 2, y ))

def draw_elevator(position, osoby_na_piętrach, ludzie_w_windzie, czy_stoi=False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    
    screen.fill((30, 30, 30))
    floor_height = 60
    elevator_y = 700 - (position * floor_height) - floor_height
    pygame.draw.rect(screen, (200, 200, 200), (100, elevator_y, 100, 50))
    
    # Draw elevator door lines
    pygame.draw.line(screen, (100, 100, 100), (150, elevator_y), (150, elevator_y + 50), 2)
    
    multi_line_text = f"Piętro: {position}\nCele: {ludzie_w_windzie}\nIlość pasażerów: {len(ludzie_w_windzie)}"
    text_x = 10
    text_y = 10
    draw_multiline_text(screen, multi_line_text, (text_x, text_y), font, (0, 255, 0))
    
    for level in range(11):
        level_y = 700 - (level * floor_height) - floor_height
        pygame.draw.rect(screen, (100, 100, 100), (210, level_y + 50, 80, 2))
        level_text = f"{level}"
        draw_multiline_text(screen, level_text, (220, level_y + 25), font, (255, 255, 255))
        
        occupied_levels = [x for x in range(len(osoby_na_piętrach)) if len(osoby_na_piętrach[x]) > 0]
        if level in occupied_levels:
            for i, person in enumerate(osoby_na_piętrach[level]):
                draw_stick_figure(screen, 260 + (i * 15), level_y + 30)
    
    if ludzie_w_windzie:
        draw_stick_figure(screen, 120, elevator_y + 15, number=len(ludzie_w_windzie))
    
    pygame.display.flip()
    time.sleep(time_step)
    if czy_stoi:
        time.sleep(time_step)

