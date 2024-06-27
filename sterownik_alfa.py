import time
import random
import copy
from srodowisko import draw_elevator

random.seed(41)

class Winda:
    def __init__(self):
        self.kierunek = 0
        self.pietro = 0
        self.pasazerowie_w_windzie = []
        self.zgloszenia = []
        # I-teraźniejsze II-inny kierunek III-nastepny cykl
        self.kolejka = [[], [], []]
    
    def dodaj_zgloszenie(self, pasazer):
        self.zgloszenia.append([pasazer, pasazer.kierunek])
        
    def zarzadzaj_kierunkiem(self):
       # jesli winda ma pasazerów w srodku
        if len(self.pasazerowie_w_windzie) > 0:
            self.kierunek = self.pasazerowie_w_windzie[0].kierunek
        else:
            if len(self.zgloszenia) > 0:
                if self.zgloszenia[0][0].start > self.pietro:
                    self.kierunek = 0 
                else:
                    self.kierunek = 1

    def zabieraj_pasazerow(self):
        pasazerowie = 0
        for i in reversed(range(len(self.zgloszenia))):
            if self.zgloszenia[i][0].start == self.pietro:
                # jesli zgadza sie kierunek 
                if self.zgloszenia[i][1] == self.kierunek or self.pietro == 0 or self.pietro == 10:
                    print("Pasażer wsiada z piętra: ", self.pietro, "Cel: ", self.zgloszenia[i][0].cel)
                    # ZABIERAM PASAŻERA
                    self.pasazerowie_w_windzie.append(self.zgloszenia[i][0])
                    # USUWAM ZGŁOSZENIE
                    del self.zgloszenia[i]
                    pasazerowie += 1
        return pasazerowie
                    

    def wypuszczaj_pasazerow(self):
        pasazerowie = 0
        for i in reversed(range(len(self.pasazerowie_w_windzie))):
            if self.pasazerowie_w_windzie[i].cel == self.pietro:
                print("Pasażer wysiada na piętrze: ", self.pietro)
                del self.pasazerowie_w_windzie[i]
                pasazerowie += 1
        return pasazerowie

    def ruch(self):
        while len(self.zgloszenia) > 0 or len(self.pasazerowie_w_windzie) > 0:
            self.zarzadzaj_kierunkiem()
            if self.kierunek == 0:
                self.pietro += 1
            else:
                self.pietro -= 1
            wysadzeni = self.wypuszczaj_pasazerow()
            zabrani = self.zabieraj_pasazerow()
            print("Pietro: ", self.pietro, "Kierunek: ", self.kierunek)
            osoby_na_pietrach = [[] for i in range(11)]
            for zgloszenie in self.zgloszenia:
                osoby_na_pietrach[zgloszenie[0].start].append(zgloszenie[0])
            # print("Zgłoszenia: ", [[x[0].start, x[0].cel] for x in self.zgloszenia])
            draw_elevator(self.pietro, osoby_na_pietrach, [x.cel for x in self.pasazerowie_w_windzie], wysadzeni + zabrani > 0)
            

class Pasazer():
    def __init__(self):
        self.start = random.randint(0, 10)
        self.cel = random.randint(0, 10)
        while self.start == self.cel:
            self.cel = random.randint(0, 10)
        if self.start > self.cel:
            self.kierunek = 1
        else:
            self.kierunek = 0
        print("Start: ", self.start, "Cel: ", self.cel)
        

winda = Winda()
for i in range(20):
    winda.dodaj_zgloszenie(Pasazer())
print(winda.zgloszenia)
winda.ruch()