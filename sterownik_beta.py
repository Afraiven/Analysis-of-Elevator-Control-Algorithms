import random
from srodowisko import draw_elevator

# STEROWNIK ten wybiera za priorytet osobę pierwszą ktora sie zglosiła 
# i jedzie do niej, a potem do kolejnych osób które się zgłosiły

# Koniec symulacji
# Obsłużono pasażerów:  201
# Czas:  288
# Średni czas w windzie:  6.388349514563107

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

    def dodaj_zgloszenie(self, pasazer):
        self.historia.append(pasazer)
        self.zgloszenia.append(pasazer)

    def zarzadzaj_kierunkiem(self):
        if not self.pasazerowie_w_windzie and not self.zgloszenia:
            return  
        
        # jesli winda ma pasazerów w srodku
        if len(self.pasazerowie_w_windzie) > 0:
            self.kierunek = self.pasazerowie_w_windzie[0].kierunek
        else:
            if len(self.zgloszenia) > 0:
                if self.zgloszenia[0].start > self.pietro:
                    self.kierunek = 0 
                else:
                    self.kierunek = 1

    def zabieraj_pasazerow(self):
        zabrani = 0
        for zgloszenie in self.zgloszenia[:]:
            if zgloszenie.start == self.pietro:
                self.pasazerowie_w_windzie.append(zgloszenie)
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

    def ruch(self):
        while self.zgloszenia or self.pasazerowie_w_windzie:
            X = random.randint(0, 2)
            if X == 0 and len(self.historia) < 200:
                jacek = Pasazer()
                self.dodaj_zgloszenie(jacek)
                self.historia.append(jacek)

            zabrani = self.zabieraj_pasazerow()
            wysadzeni = self.wypuszczaj_pasazerow()
            self.zarzadzaj_kierunkiem()
            if self.kierunek == 0 and self.pietro < 10:
                self.pietro += 1
            elif self.kierunek == 1 and self.pietro > 0:
                self.pietro -= 1
            self.czas += 1
            for pasazer in self.pasazerowie_w_windzie:
                pasazer.licz()
            print("Pietro: ", self.pietro, " Kierunek: ", "góra" if self.kierunek == 0 else "dół")
            print("Pasazerowie w windzie: ", [(p.start, p.cel) for p in self.pasazerowie_w_windzie])
            print("Zgloszenia: ", [(z.start, z.cel) for z in self.zgloszenia])
            print("---" * 30)
            osoby_na_pietrach = [[] for i in range(11)]
            for zgloszenie in self.zgloszenia:
                osoby_na_pietrach[zgloszenie.start].append(zgloszenie)
            # print("Zgłoszenia: ", [[x[0].start, x[0].cel] for x in self.zgloszenia])
            draw_elevator(self.pietro, osoby_na_pietrach, [x.cel for x in self.pasazerowie_w_windzie], wysadzeni + zabrani > 0)
        print("Koniec symulacji")
        print("Obsłużono pasażerów: ", len(self.historia))
        print("Czas: ", self.czas)
        print("Średni czas w windzie: ", sum(self.czasy_pasazerow) / len(self.czasy_pasazerow))

class Pasazer:
    def __init__(self):
        self.start = random.randint(0, 10)
        self.cel = random.randint(0, 10)
        while self.start == self.cel:
            self.cel = random.randint(0, 10)
        self.kierunek = 0 if self.start < self.cel else 1
        self.czas_w_windzie = 0
    
    def licz(self):
        self.czas_w_windzie += 1

random.seed(42)
winda = Winda()
for i in range(5):
    winda.dodaj_zgloszenie(Pasazer())
winda.ruch()
