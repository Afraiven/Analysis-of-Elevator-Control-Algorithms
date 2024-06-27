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
        self.reset = False

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
        if self.reset:
            self.reset = False
            e = 0
            if self.aktualny_poziom < poziom:
                self.aktualny_etap = 0
            else:
                self.aktualny_etap = 1
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
        if self.reset:
            self.reset = False
            e = 0
            if self.aktualny_poziom > poziom:
                self.aktualny_etap = 1
            else:
                self.aktualny_etap = 0
        return e

    # panel wewnętrzny windy
    def panel(self, kierunek, pietro, e):
        # w górę
        if pietro == 10:
            kierunek = 1
        elif pietro == 0:
            kierunek = 0
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
        self.tablica_celow.append([pietro, cel, e])
        
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

    def ruch(self):
        global osoby_na_pietrach
        self.generator_kolejki()
        while len(self.kolejka[0]) > 0:
            print(f"Wewnątrz windy: {self.ludzie_wewnatrz}")
            self.generator_kolejki()
            draw_elevator(self.aktualny_poziom, osoby_na_pietrach, self.ludzie_wewnatrz)
            print(f"Winda stoi na piętrze {self.aktualny_poziom}")
            # pasażer wsiada
            print('Kolejka:', self.kolejka)
            while len(self.kolejka[0]) > 0 and self.aktualny_poziom != self.kolejka[0][0]:
                print('Kolejka:', self.kolejka)
                if self.aktualny_etap == 0:
                    self.aktualny_poziom += 1
                else:
                    self.aktualny_poziom -= 1
                draw_elevator(self.aktualny_poziom, osoby_na_pietrach, self.ludzie_wewnatrz)
                print(f"Winda na piętrze {self.aktualny_poziom}, jedzie w {['górę', 'dół'][self.aktualny_etap]}")
            # pasażer wsiada
            if len(osoby_na_pietrach[self.aktualny_poziom]) > 0:
                osoby_na_pietrach[self.aktualny_poziom].remove(1)
                targets_to_remove = []
                for i in self.tablica_celow:
                    if i[0] == self.aktualny_poziom and (i[2] == 0 or len(set(self.kolejka[0])) == 1):
                        targets_to_remove.append(i)
                for target in targets_to_remove:
                    self.tablica_celow.remove(target)
                    self.ludzie_wewnatrz.append(target[1])

            # ludzie wysiadają
            self.ludzie_wewnatrz = [osoba for osoba in self.ludzie_wewnatrz if osoba != self.aktualny_poziom]
            self.kolejka[0].pop(0)
        for i in self.tablica_celow:
            i[2] -= 1
        self.kolejka = self.kolejka[1:]
        self.kolejka.append([])
    
        # zmiana etapu
        self.aktualny_etap = [1, 0][self.aktualny_etap]

        # Handle new passenger requests
        if sum([len(x) for x in self.kolejka]) == 0:
            self.reset = True

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
    prob = random.randint(0, 10)
    if prob == 0:
        Pasazer(random.randint(0, 1))
    winda.ruch()


# poprawić cykliczność etapów