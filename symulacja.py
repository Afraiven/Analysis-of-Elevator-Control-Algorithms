poziom = 0
trasa = []
requesty = []

# generuje trase przejazdu windy
def generuj_trase(trasa, requesty, poziom):
    if len(requesty) == 0:
        return trasa, requesty
    
    # dodaj pierwszy request do trasy
    trasa.append(requesty[0][0])
    trasa.append(requesty[0][1])
    requesty.remove(requesty[0])

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
    print(trasa)
    return trasa, requesty

for i in range(30):
    # losowanie requestów [tymczasowe statyczne]
    if i == 0:
        requesty.append([8, 1])
        requesty.append([7, 0])
    # losowanie requestów [tymczasowe statyczne]
    elif i == 35:
        requesty.append([3, 6])
    trasa, requesty = generuj_trase(trasa, requesty, poziom)

    # symulacja jazdy windy
    if len(trasa) > 0:
        poziom += [-1, 1][trasa[0] > poziom] 
        if poziom == trasa[0]:
            trasa.remove(trasa[0])
            print('Zatrzymano')
    print(poziom)
    input()
