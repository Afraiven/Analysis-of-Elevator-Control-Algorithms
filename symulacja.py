import time
import pygame
import random
from itertools import groupby
from wizualizacja import draw_elevator

debug = False
poziom = 0
trasa = []
requesty = []
osoby_w_windzie = []
osoby_na_piętrach = [[] for _ in range(11)]  # Przykład dla budynku z 11 piętrami (0-10)

def flatten(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list

def remove_consecutive_duplicates(data):
    return [key for key, _ in groupby(data)]

def generuj_trase(trasa, requesty, poziom):
    if len(requesty) == 0:
        return trasa, requesty
    
    # dodaj pierwszy request do trasy
    if len(trasa) == 0:
        trasa.append(requesty[0][0])
        trasa.append(requesty[0][1])
        requesty.remove(requesty[0])

        if len(requesty) == 0:
            return trasa, requesty
        # okresl kierunek jazdy windy
        if requesty[0][0] < requesty[0][1]:
            kierunek = 'up'
            potencjalne = [x for x in requesty if x[0] < x[1]]
            for j in potencjalne:
                trasa.append(j[0])
                trasa.append(j[1])
                requesty.remove(j)
            trasa = sorted(trasa)
        else:
            kierunek = 'down'
            potencjalne = [x for x in requesty if x[0] > x[1]]
            for j in potencjalne:
                trasa.append(j[0])
                trasa.append(j[1])
                requesty.remove(j)
            trasa = sorted(trasa)[::-1]
   
    else:
        trasa = trasa[::-1]
        trasa.append(poziom)
        trasa = trasa[::-1]
        for request in requesty:
            if request[0] < request[1]:
                kierunek = 'up'
                for i in range(len(trasa)-1):
                    if type(trasa[i]) == list:
                        now = max(trasa[i])
                    else:
                        now = trasa[i]
                    if type(trasa[i+1]) == list:
                        next = max(trasa[i+1])
                    else:
                        next = trasa[i+1]
                    if now < next:
                        if now <= request[0] <= next:
                            trasa.insert(i, request)
                            requesty.remove(request)
                            break
            else:
                kierunek = 'down'
                for i in range(len(trasa)-1):
                    if type(trasa[i]) == list:
                        now = max(trasa[i])
                    else:
                        now = trasa[i]
                    if type(trasa[i+1]) == list:
                        next = max(trasa[i+1])
                    else:
                        next = trasa[i+1]
                    if now > next:
                        if now >= request[0] >= next:
                            trasa.insert(i+1, request)
                            requesty.remove(request)
                            break
        #[0, 10, 7, 6, 5, 0]
        #[[3, 6]]
    nowa_trasa = []
    for i in trasa:
        if i == poziom:
            trasa.remove(i)
            break
    kopia_trasy = trasa.copy()
    for i in trasa:
        if i in kopia_trasy:
            kopia_trasy.remove(i)
            nowa_trasa.append(i)
    nowa_trasa = flatten(nowa_trasa)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    return nowa_trasa, requesty

while True:
    for _ in range(random.randint(1, 10)):
        prob = random.randint(0, 7)
        if prob == 0:
            start = random.randint(0, 10)
            stop = random.randint(0, 10)
            while start == stop:
                stop = random.randint(0, 10)
            requesty.append([start, stop])
            print(f" Chce jechać z {start} na {stop}")
            osoby_na_piętrach[start].append(stop)  # Dodaj osoby oczekujące na piętrach

    if len(requesty) > 0:
        trasa = remove_consecutive_duplicates(trasa)
        trasa, requesty = generuj_trase(trasa, requesty, poziom)

    if debug:
        print(f"Piętro: {poziom}")
        print(f"Trasa: {trasa}")
        print(f"Requesty: {requesty}")
        print(f"Osoby na piętrach: {osoby_na_piętrach}")
        print(f"Osoby w windzie: {osoby_w_windzie}")

    if len(trasa) == 0:
        draw_elevator(poziom, poziom, osoby_na_piętrach, osoby_w_windzie)
    else:
        draw_elevator(poziom, trasa[0], osoby_na_piętrach, osoby_w_windzie)
        if poziom == trasa[0]:
            trasa.remove(trasa[0])
            if debug:
                print('Zatrzymano')
            if len(osoby_na_piętrach[poziom]) > 0:
                # DODAC WARUNEK JEZELI ZABIERA
                for x in osoby_na_piętrach[poziom]:
                    osoby_w_windzie.append(x)
                osoby_na_piętrach[poziom] = []
            for x in osoby_w_windzie:
                if x == poziom:
                    osoby_w_windzie.remove(x)
            time.sleep(0.5)
        if len(trasa) != 0:
            poziom += [-1, 1][trasa[0] > poziom] * (poziom != trasa[0])
pygame.quit()
