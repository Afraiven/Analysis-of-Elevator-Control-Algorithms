import time

# cykl 0 to jazda w górę
cykl0 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
# cykl 1 to jazda w dół
cykl1 = {10: 0, 9: 0, 8: 0, 7: 0, 6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0: 0}
# etap to dwa cykle
etap = [cykl0, cykl1]

class Winda:
    def __init__(self, etap):
        self.etap = etap
        self.aktualny_cykl = 0
        self.aktualny_poziom = 0
        self.kolejka = [[],[], [], []]

    def up_arrow(self, poziom):
        if self.aktualny_cykl == 0:
            if self.aktualny_poziom <= poziom:
                # zlecenie odbędzie się w aktualnym etapie
                c = 0
            else:
                # zlecenie odbędzie się w przyszłym etapie w pierwszym cyklu
                c = 2
            return c
        else:
            c = 1
        return c

    def down_arrow(self, poziom):
        if self.aktualny_cykl == 1:
            if self.aktualny_poziom >= poziom:
                # zlecenie odbędzie się w aktualnym etapie
                c = 0
            else:
                # zlecenie odbędzie się w przyszłym etapie w drugim cyklu
                c = 2
        else:
            c = 1
        return c

    def generator_kolejki(self):
        for i in range(len(self.etap)):
            for pietro in self.etap[i]:
                if self.etap[i][pietro] > 0:
                    if i == 1:
                        c = self.down_arrow(pietro)
                    else:
                        c = self.up_arrow(pietro)
                    # print(f"Zlecenie na piętro {pietro} zostanie zrealizowane w cyklu {c}")
                    self.kolejka[c].append(pietro)
                    # kasuj zgłoszenie
                    self.etap[i][pietro] = 0
                    # time.sleep(0.1)
                else:
                    pass
                    # print(f"Brak zleceń na piętro {pietro}")
                    # time.sleep(0.1)
        print(self.kolejka)

    def ruch(self):
        self.generator_kolejki()
        for i in self.kolejka[0]:
            print(f"Winda na piętrze {self.aktualny_poziom}")
            while self.aktualny_poziom != i:
                if self.aktualny_cykl == 0:
                    self.aktualny_poziom += 1
                else:
                    self.aktualny_poziom -= 1
                print(f"Winda na piętrze {self.aktualny_poziom}")
                # pasażer wsiada
        self.kolejka = self.kolejka[1:]
        # zmiana cyklu
        self.aktualny_cykl = [0, 1][self.aktualny_cykl]

etap[0][3] = 1
etap[0][4] = 1
etap[0][8] = 1
etap[1][3] = 1
winda = Winda(etap)
winda.ruch()