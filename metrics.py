import random
from matplotlib import pyplot as plt
import math
import numpy as np

def summary(historia, czas, czasy_pasazerow, czasy_oczekiwania_pasazerow):
    laczne_czasy = [x + y for x, y in zip(czasy_pasazerow, czasy_oczekiwania_pasazerow)]
    print("Koniec symulacji")
    print("Obsłużono pasażerów: ", len(historia))
    print("Czas [ilość pięter]: ", czas)
    print("Średni czas w windzie: ", sum(czasy_pasazerow) / len(czasy_pasazerow))
    print("Średni czas oczekiwania na windę: ", sum(czasy_oczekiwania_pasazerow) / len(czasy_oczekiwania_pasazerow))
    print("Średni czas podróży: ", (sum(laczne_czasy)) / len(laczne_czasy))
    bins_count = int(math.sqrt(len(laczne_czasy)))
    bins = np.linspace(min(laczne_czasy), max(laczne_czasy), bins_count + 1)
    plt.hist(laczne_czasy, bins=bins, color='blue', alpha=0.5, label='Czasy podróży [+oczekiwanie]')
    plt.xlabel('Czas podróży')
    plt.title("Czasy podróży")
    plt.show()


class Pasazer:
    def __init__(self):
        self.start = random.randint(0, 10)
        self.cel = random.randint(0, 10)
        while self.start == self.cel:
            self.cel = random.randint(0, 10)
        self.kierunek = 0 if self.start < self.cel else 1
        self.czas_w_windzie = 0
        self.czas_oczekiwania_na_winde = 0
    
    def licz_czas_w_windzie(self):
        self.czas_w_windzie += 1

    def licz_czas_oczekiwania_na_winde(self):
        self.czas_oczekiwania_na_winde += 1