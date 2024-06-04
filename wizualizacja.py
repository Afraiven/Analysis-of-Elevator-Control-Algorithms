import time
import pygame
import random 

random.seed(1234)
levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
timer = True
time_step = 0.5
current = 0
debug = False

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



def go_up(start, levels, desired):
    global current 
    if debug:
        print(f"Jazda w góre, Winda jest na piętrze {current}, pasażer zaczyna jazdę z piętra {start}, a cel to {desired}")
        print("*"*20)
    # jeżeli winda jest za nisko to jedzie do góry
    if start > current:
        current = go_up(current, levels, start)
    elif start < current:
        current = go_down(current, levels, start)
    # funkcja opisująca ruch windy w górę
   
    for i in range(start, desired + 1):
        if debug:
            print('Winda jest na piętrze', levels[i])
        draw_elevator(levels[i], desired)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
    if debug:
        print("*"*20)
    time.sleep(3)
    return desired

def go_down(start, levels, desired=0):
    global current
    if debug:
        print(f"Jazda w dół, Winda jest na piętrze {current}, pasażer zaczyna jazdę z piętra {start}, a cel to {desired}")
        print("*"*20)
    # jeżeli winda jest za nisko to jedzie do góry
    if start > current:
        current = go_up(current, levels, start)
    elif start < current:
        current = go_down(current, levels, start)
    # funkcja opisująca ruch windy w dół
    
    for i in range(start, desired - 1, -1):
        if debug:
            print('Winda jest na piętrze', levels[i])
        draw_elevator(levels[i], desired)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    if debug:
        print("*"*20)
    time.sleep(3)
    return desired

for i in range(10):
    start = random.choice(levels)
    desired = random.choice(levels)
    while desired == start:
        desired = random.choice(levels)
    print(f"Start: {start}Cel: {desired}")
    if start < desired:
        current = go_up(start, levels, desired)
    elif start > desired:
        current = go_down(start, levels, desired)
    time.sleep(1)

# current = 0
# current = go_up(current, 0, levels, 5)
# current = go_down(current, 10, levels)
pygame.quit()

# TODO
# Asynchroniczny ruch windy względem requestów od pasażerów
# Requesty w ustalonym typie danych ( stos / kolejka / lista)
# Wielu pasażerów jednocześnie
# Limit pasażerów


# import threading
# import time


# class Pasazer():
#     def __init__(self, start) -> None:
#         self.start = start

#     # planuje jechać w dół z pietra start
#     def call_down(self):
#         # jeśli jedzie i ma po drodze to zatrzymaj
#         # jesli jedzie i nie ma po drodze to dodaj na koniec trasy
#         # jesli stoi to dodaj do trasy
#         global poziom
#         global trasa

#     # planuje jechać w górę z pietra start
#     def call_up(self):
#         # jeśli jedzie i ma po drodze to zatrzymaj
#         # jesli jedzie i nie ma po drodze to dodaj na koniec trasy
#         # jesli stoi to dodaj do trasy
#         global poziom
#         global trasa

#     # pasażer w windzie wybiera cel
#     def jedz_na(self, cel):
#         global requesty
#         requesty.append([self.start, cel])


# class Winda():
#     def __init__(self):
#         self.poziom = 0
#         self.trasa = []
#         self.requesty = []
#         self.stop = False
#         self.going_up = False

#     def generuj_trasa(self):
#         # generuje trasę na podstawie requestów
        

#     def jedz(self):
#         while len(trasa) > 0:
#             self.fix_trasa()
            

# poziom = 0
# trasa = []
# winda = Winda()
# filip = Pasazer(8)
# filip.call_down()
# filip.jedz_na(0)
# kuba = Pasazer(7)
# kuba.call_down()
# kuba.jedz_na(0)
# winda.jedz()

