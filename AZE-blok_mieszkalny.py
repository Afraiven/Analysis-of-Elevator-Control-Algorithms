import random
from srodowisko import draw_elevator
from metrics import summary, normal_or_odd, Pasazer_Ola
import numpy as np
# Algorytm Zgodnych Ekstremów

# Koniec symulacji
# Obsłużono pasażerów:  100000
# Czas [ilość pięter]:  109941
# Średni czas w windzie:  6.97069
# Średni czas oczekiwania na windę:  6.46927
# Średni czas podróży:  13.43996

class Winda:
    def __init__(self):
        # 0 - góra, 1 - dół
        self.kierunek = 0  
        self.pietro = 0
        self.pasazerowie_w_windzie = []
        self.zgloszenia = []
        self.historia = []
        self.czas = 0
        self.czasy_pasazerow = []
        self.czasy_oczekiwania_pasazerow = []
        self.pojemnosc = 6
        self.miejsce_postoju = 9

    def dodaj_zgloszenie(self, pasazer):
        self.historia.append(pasazer)
        self.zgloszenia.append(pasazer)

    def zarzadzaj_kierunkiem(self):
        if not self.pasazerowie_w_windzie and not self.zgloszenia:
            return  
        
        pietra_cele = {p.cel for p in self.pasazerowie_w_windzie}
        pietra_zgloszenia = {r.start for r in self.zgloszenia}
        pietra_pasujace = pietra_cele | pietra_zgloszenia
        
        if self.kierunek == 0 and self.pietro >= max(pietra_pasujace, default=self.pietro):
            self.kierunek = 1 # jazda w dół
        elif self.kierunek == 1 and self.pietro <= min(pietra_pasujace, default=self.pietro):
            self.kierunek = 0 # jazda w górę

    def zabieraj_pasazerow(self):
        zabrani = 0
        for zgloszenie in self.zgloszenia[:]:
            if zgloszenie.start == self.pietro:
                self.pasazerowie_w_windzie.append(zgloszenie)
                self.czasy_oczekiwania_pasazerow.append(zgloszenie.czas_oczekiwania_na_winde)
                self.zgloszenia.remove(zgloszenie)
                zabrani += 1
        return zabrani

    def wypuszczaj_pasazerow(self):
        wysadzeni = 0
        for pasazer in self.pasazerowie_w_windzie[:]:
            if pasazer.cel == self.pietro:
                self.pasazerowie_w_windzie.remove(pasazer)
                wysadzeni += 1
                self.czasy_pasazerow.append(pasazer.czas_w_windzie)
        return wysadzeni
    
    def prob(self):
            probabilities = [0.3, 0.25, 0.2, 0.15, 0.05, 0.05]
            values = np.arange(1, 7)
            return np.random.choice(values, size=1, p=probabilities)[0]
    
    def ruch(self):
        while len(self.historia) < 100000 or self.zgloszenia or self.pasazerowie_w_windzie:
            for _ in range(2):
                X = random.randint(0, 40)
                if X == 0 and len(self.historia) < 100000:
                    # dodaj od 1 do 6 pasażerów
                    if normal_or_odd() == 0:
                        start = random.randint(0, 10)
                        cel = random.randint(0, 10)
                        while start == cel:
                            cel = random.randint(0, 10)
                        kierunek = 0 if start < cel else 1
                    else:
                        kierunek = random.randint(0, 1)
                        if kierunek == 0:
                            start = 0
                            cel = random.randint(1, 10)
                        else:
                            start = random.randint(1, 10)
                            cel = 0
                    for _ in range(self.prob()):
                        ola = Pasazer_Ola(start, cel, kierunek)
                        self.dodaj_zgloszenie(ola)

            zabrani = self.zabieraj_pasazerow()
            wysadzeni = self.wypuszczaj_pasazerow()
            self.zarzadzaj_kierunkiem()
            if self.kierunek == 0 and self.pietro < 10 and len(self.pasazerowie_w_windzie) + len(self.zgloszenia) > 0:
                self.pietro += 1
            elif self.kierunek == 1 and self.pietro > 0 and len(self.pasazerowie_w_windzie) + len(self.zgloszenia) > 0:
                self.pietro -= 1
            # gdy stoi, jedz na miejsce postoju
            else:
                if self.pietro > self.miejsce_postoju:
                    self.pietro -= 1
                elif self.pietro < self.miejsce_postoju:
                    self.pietro += 1
                    
            self.czas += 1
            for pasazer in self.pasazerowie_w_windzie:
                pasazer.licz_czas_w_windzie()
            for pasazer in self.zgloszenia:
                pasazer.licz_czas_oczekiwania_na_winde()
            if len(self.historia)%1000 == 0:
                print(len(self.historia))
            # print("Pietro: ", self.pietro, " Kierunek: ", "góra" if self.kierunek == 0 else "dół")
            # print("Pasazerowie w windzie: ", [(p.start, p.cel) for p in self.pasazerowie_w_windzie])
            # print("Zgloszenia: ", [(z.start, z.cel) for z in self.zgloszenia])
            # print("---" * 30)
            osoby_na_pietrach = [[] for i in range(11)]
            for zgloszenie in self.zgloszenia:
                osoby_na_pietrach[zgloszenie.start].append(zgloszenie)
            # print("Zgłoszenia: ", [[x[0].start, x[0].cel] for x in self.zgloszenia])
            # draw_elevator(self.pietro, osoby_na_pietrach, [x.cel for x in self.pasazerowie_w_windzie], wysadzeni + zabrani > 0)
        summary(self.historia, self.czas, self.czasy_pasazerow, self.czasy_oczekiwania_pasazerow)

random.seed(43)
winda = Winda()
for i in range(1):
    winda.dodaj_zgloszenie(Pasazer_Ola(10, 0, 1))
winda.ruch()