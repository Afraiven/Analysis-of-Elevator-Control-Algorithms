import random
from srodowisko import draw_elevator
from metrics import summary, Pasazer

# Priorytet najbliższego zgłoszenia
# Algorytm priorytetyzuje najbliższe zgłoszenie,
# minimalizując odległość do najbliższego pasażera lub celu.
# Kierunek windy jest ustalany na podstawie najbliższego zgłoszenia 
# lub celu pasażerów w windzie. Winda najpierw zabiera pasażerów,
# którzy chcą wsiąść na bieżącym piętrze, a następnie wysadza pasażerów na ich docelowych piętrach.
# Algorytm dynamicznie reaguje na nowe zgłoszenia, stale aktualizując trasę windy.

# Koniec symulacji
# Obsłużono pasażerów:  100000
# Czas [ilość pięter]:  110378
# Średni czas w windzie:  6.85558
# Średni czas oczekiwania na windę:  8.2083
# Średni czas podróży:  15.06388

class Winda:
    def __init__(self):
        self.kierunek = 0
        self.pietro = 0
        self.pasazerowie_w_windzie = []
        self.zgloszenia = []
        self.historia = []
        self.czas = 0
        self.czasy_pasazerow = []
        self.czasy_oczekiwania_pasazerow = []

    def dodaj_zgloszenie(self, pasazer):
        self.historia.append(pasazer)
        self.zgloszenia.append(pasazer)

    def znajdz_najblizsze_zgloszenie(self):
        if self.pasazerowie_w_windzie:
            najblizsze_zgloszenie = min(self.pasazerowie_w_windzie, key=lambda x: abs(self.pietro - x.cel))
            return najblizsze_zgloszenie
        elif self.zgloszenia:
            najblizsze_zgloszenie = min(self.zgloszenia, key=lambda x: abs(self.pietro - x.start))
            return najblizsze_zgloszenie
        else:
            return None

    def zarzadzaj_kierunkiem(self):
        najblizsze_zgloszenie = self.znajdz_najblizsze_zgloszenie()
        if najblizsze_zgloszenie:
            if self.pasazerowie_w_windzie:
                self.kierunek = 0 if najblizsze_zgloszenie.cel > self.pietro else 1
            else:
                self.kierunek = 0 if najblizsze_zgloszenie.start > self.pietro else 1

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

    def ruch(self):
        while self.zgloszenia or self.pasazerowie_w_windzie:
            for _ in range(10):
                X = random.randint(0, 10)
                if X == 0 and len(self.historia) < 100000:
                    jacek = Pasazer()
                    self.dodaj_zgloszenie(jacek)

            zabrani = self.zabieraj_pasazerow()
            wysadzeni = self.wypuszczaj_pasazerow()
            self.zarzadzaj_kierunkiem()
            if self.kierunek == 0 and self.pietro < 10:
                self.pietro += 1
            elif self.kierunek == 1 and self.pietro > 0:
                self.pietro -= 1
            self.czas += 1
            for pasazer in self.pasazerowie_w_windzie:
                pasazer.licz_czas_w_windzie()
            for pasazer in self.zgloszenia:
                pasazer.licz_czas_oczekiwania_na_winde()
            osoby_na_pietrach = [[] for _ in range(11)]
            for zgloszenie in self.zgloszenia:
                osoby_na_pietrach[zgloszenie.start].append(zgloszenie)
            # draw_elevator(self.pietro, osoby_na_pietrach, [x.cel for x in self.pasazerowie_w_windzie], wysadzeni + zabrani > 0)
        summary(self.historia, self.czas, self.czasy_pasazerow, self.czasy_oczekiwania_pasazerow)

random.seed(43)
winda = Winda()
for i in range(5):
    winda.dodaj_zgloszenie(Pasazer())
winda.ruch()
