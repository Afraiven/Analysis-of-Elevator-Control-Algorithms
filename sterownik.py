import time
import random
from srodowisko import draw_elevator
import copy

# etap 0 to jazda w górę
etap0 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
# etap 1 to jazda w dół
etap1 = {10: 0, 9: 0, 8: 0, 7: 0, 6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0: 0}
# cykl to dwa etapy
cykl = [etap0, etap1]
random.seed(41)
osoby_na_pietrach = [[], [], [], [], [], [], [], [], [], [], []]

class Winda:
    def __init__(self, cykl):
        self.cykl = cykl
        self.cykl_celow = copy.deepcopy(cykl)
        for i in range(len(self.cykl_celow)):
            for pietro in self.cykl_celow[i]:
                self.cykl_celow[i][pietro] = []
        self.aktualny_etap = 0
        self.aktualny_poziom = 0
        self.kolejka = [[],[], [], [], [], []]
        self.ludzie_wewnatrz = []
        self.tablica_celow = []

    def up_arrow(self, poziom):
        if self.aktualny_etap == 0:
            if self.aktualny_poziom <= poziom:
                # zlecenie odbędzie się w aktualnym etapie
                e = 0
            else:
                # zlecenie odbędzie się w przyszłym etapie w pierwszym cyklu
                e = 2
        else:
            e = 1
        return e

    def down_arrow(self, poziom):
        if self.aktualny_etap == 1:
            if self.aktualny_poziom >= poziom:
                # zlecenie odbędzie się w aktualnym etapie
                e = 0
            else:
                # zlecenie odbędzie się w przyszłym etapie w drugim cyklu
                e = 2
        else:
            e = 1
        return e

    # panel wewnętrzny windy
    def panel(self, kierunek, pietro, e):
        # w górę
        if kierunek%2 == 0:
            floor = pietro + 1
            ceiling = 10
        # w dół
        else:
            floor = 0
            ceiling = pietro - 1
        cel = random.randint(floor, ceiling)
        print(f"Pasażer chce jechać z {pietro} na {cel}")
        # pasażer wybiera cel
        self.cykl_celow[0][cel].append(e + 2)
        self.tablica_celow.append([pietro, cel])
        
    def generator_kolejki(self):
        for i in range(len(self.cykl)):
            for pietro in self.cykl[i]:
                if self.cykl[i][pietro] > 0:
                    if i == 1:
                        e = self.down_arrow(pietro)
                    else:
                        e = self.up_arrow(pietro)
                    # Zlecenie na piętro {pietro} zostanie zrealizowane na etapie {e}
                    self.panel(e + self.aktualny_etap, pietro, e)
                    self.kolejka[e].append(pietro)
                    # kasuj zgłoszenie
                    self.cykl[i][pietro] = 0
        for i in range(len(self.cykl_celow)):
            for pietro in self.cykl_celow[i]:
                if len(self.cykl_celow[i][pietro]) > 0:
                    for j in self.cykl_celow[i][pietro]:
                        e = j - 2
                        self.kolejka[e].append(pietro)
                        # kasuj zgłoszenie
                        self.cykl_celow[i][pietro].remove(j)
        for i in range(len(self.kolejka)):
            if (i + self.aktualny_etap) % 2 == 0:
                self.kolejka[i].sort()
            else:
                self.kolejka[i].sort(reverse=True)
        input(self.kolejka)

    def ruch(self):
        global osoby_na_pietrach
        self.generator_kolejki()
        while len(self.kolejka[0]) > 0:
            print(f"Wewnątrz windy: {self.ludzie_wewnatrz}")
            self.generator_kolejki()
            draw_elevator(self.aktualny_poziom, osoby_na_pietrach, self.ludzie_wewnatrz)
            print(f"Winda stoi na piętrze {self.aktualny_poziom}")
            while len(self.kolejka[0]) > 0 and self.aktualny_poziom != self.kolejka[0][0]:
                if self.aktualny_etap == 0:
                    self.aktualny_poziom += 1
                else:
                    self.aktualny_poziom -= 1
                draw_elevator(self.aktualny_poziom, osoby_na_pietrach, self.ludzie_wewnatrz)
                print(f"Winda na piętrze {self.aktualny_poziom}, jedzie w {['górę', 'dół'][self.aktualny_etap]}")
            # pasażer wsiada
            if len(osoby_na_pietrach[self.kolejka[0][0]]) > 0:
                osoby_na_pietrach[self.kolejka[0][0]].remove(1)
                for i in self.tablica_celow:
                    if i[0] == self.aktualny_poziom:
                        self.tablica_celow.remove(i)
                        self.ludzie_wewnatrz.append(i[1])
            else:
                for i in self.ludzie_wewnatrz:
                    if i == self.aktualny_poziom:
                        self.ludzie_wewnatrz.remove(i)
            self.kolejka[0].pop(0)
        self.kolejka = self.kolejka[1:]
        self.kolejka.append([])
        # zmiana etapu
        self.aktualny_etap = [1, 0][self.aktualny_etap]

class Pasazer():
    def __init__(self, kierunek):
        global osoby_na_pietrach
        self.poziom = random.randint(0, 10)
        self.kierunek = kierunek
        cykl[self.kierunek][self.poziom] = 1
        osoby_na_pietrach[self.poziom].append(1)
        
Pasazer(0)
Pasazer(0)
Pasazer(0)
Pasazer(1)
Pasazer(1)
Pasazer(1)
winda = Winda(cykl)
while True:
    winda.ruch()
