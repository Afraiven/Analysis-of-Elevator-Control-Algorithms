import time
import pygame
levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
timer = True
time_step = 0.2
# założenie, że winda jeździ tylko od 0 piętra n > 0 lub od piętra n > 0 do 0

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((300, 700))
pygame.display.set_caption('Winda')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def draw_multiline_text(surface, text, pos, font, color):
    x, y = pos
    line_spacing = font.get_linesize()
    for line in text.split('\n'):
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y))
        y += line_spacing 

def draw_elevator(position, desired):
    screen.fill((0, 0, 0))
    floor_height = 50
    elevator_y = 600 - (position * floor_height) - floor_height
    pygame.draw.rect(screen, (255, 255, 255), (100, elevator_y, 100, 100))
    multi_line_text = f"Piętro: {position}\nCel: {desired}"
    text_x = 100  
    text_y = elevator_y + 5  
    draw_multiline_text(screen, multi_line_text, (text_x, text_y), font, (0, 128, 0))
    pygame.display.flip()
    time.sleep(time_step)



def go_up(current, start, levels, desired):
    # jeżeli winda jest za nisko to jedzie do góry
    if start > current:
        current = go_up(current, current, levels, start)
    elif start < current:
        current = go_down(current, current, levels, start)
    # funkcja opisująca ruch windy w górę
    print("Jazda w góre")
    print("*"*20)
    for i in range(start, desired + 1):
        print('Winda jest na piętrze', levels[i])
        draw_elevator(levels[i], desired)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    print("*"*20)
    return desired

def go_down(current, start, levels, desired=0):
    # jeżeli winda jest za nisko to jedzie do góry
    if start > current:
        current = go_up(current, current, levels, start)
    elif start < current:
        current = go_down(current, current, levels, start)
    # funkcja opisująca ruch windy w dół
    print("Jazda w dół")
    print("*"*20)
    for i in range(start, desired - 1, -1):
        print('Winda jest na piętrze', levels[i])
        draw_elevator(levels[i], desired)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    print("*"*20)
    return desired

current = 0
current = go_up(current, 0, levels, 5)
current = go_down(current, 10, levels)
pygame.quit()

