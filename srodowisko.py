import time
import pygame
import os
import sys


time_step = 0.01
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'

pygame.init()
screen = pygame.display.set_mode((300, 700))
pygame.display.set_caption('Winda')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)

def draw_multiline_text(surface, text, pos, font, color):
    x, y = pos
    line_spacing = font.get_linesize()
    for line in text.split('\n'):
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y))
        y += line_spacing

def draw_elevator(position, osoby_na_piętrach, ludzie_w_windzie, czy_stoi = False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
             sys.exit(0)
    screen.fill((0, 0, 0))
    floor_height = 50
    elevator_y = 600 - (position * floor_height) - floor_height
    pygame.draw.rect(screen, (255, 255, 255), (100, elevator_y, 100, 50))
    multi_line_text = f"Piętro: {position}\nCele: {ludzie_w_windzie}\nIlość: {len(ludzie_w_windzie)}"
    text_x = 100
    text_y = elevator_y + 5
    draw_multiline_text(screen, multi_line_text, (text_x, text_y), font, (0, 128, 0))

    for level in range(11): 
        level_y = 600 - (level * floor_height) - floor_height
        pygame.draw.rect(screen, (200, 200, 200), (210, level_y + 50, 80, 2))  
        level_text = f"{level}"
        draw_multiline_text(screen, level_text, (220, level_y + 25), font, (255, 255, 255))
        occupied_levels = [x for x in range(len(osoby_na_piętrach)) if len(osoby_na_piętrach[x]) > 0]
   
        
        if level in occupied_levels:
            pygame.draw.circle(screen, (255, 0, 0), (260, level_y + 30), 10)
            pygame.draw.rect(screen, (255, 0, 0), (255, level_y + 40, 10, 20)) 

    pygame.display.flip()
    time.sleep(time_step)
    if czy_stoi:
        time.sleep(time_step)
