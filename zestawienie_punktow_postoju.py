import matplotlib.pyplot as plt

# Zbiór danych z symulacji
dane = {
    "symulacja": list(range(11)),
    "sredni_czas_w_windzie": [5.812071879281207, 5.75657486850263, 5.73955, 5.733052669473305, 5.725052749472505, 5.733565328693426, 5.73382, 5.71672566548669, 5.734427967160985, 5.72515, 5.73748],
    "sredni_czas_oczekiwania_na_winde": [4.247847521524784, 4.140407191856163, 4.13573, 4.1950180498195015, 4.333576664233358, 4.56264874702506, 4.83512, 5.142547149057019, 5.5073047808565745, 5.88826, 6.28996],
    "sredni_czas_podrozy": [10.059919400805992, 9.896982060358793, 9.87528, 9.928070719292807, 10.058629413705862, 10.296214075718485, 10.56894, 10.85927281454371, 11.24173274801756, 11.61341, 12.02744],
    "wariancja_czasow_podrozy": [33.003739592107785, 30.030726477328617, 27.5823449216, 25.709459032248407, 24.050652050953918, 23.445426557959507, 22.885267276399997, 22.941126640657924, 23.205267367473212, 23.362958171899997, 23.798087046399996]
}

print("Najmniejszy średni czas podróży: ", min(dane["sredni_czas_podrozy"]))
print("Najmniejsza wariancja czasów podróży: ", min(dane["wariancja_czasow_podrozy"]))
print("Indeks najmniejszego średniego czasu podróży: ", dane["sredni_czas_podrozy"].index(min(dane["sredni_czas_podrozy"])))
print("Indeks najmniejszej wariancji czasów podróży: ", dane["wariancja_czasow_podrozy"].index(min(dane["wariancja_czasow_podrozy"])))

fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Symulacja')
ax1.set_ylabel('Średni czas (w minutach)', color=color)
ax1.plot(dane['symulacja'], dane['sredni_czas_podrozy'], label='Średni czas podróży', color='black')
ax1.tick_params(axis='y', labelcolor=color)
ax1.axhline(y=10.41958, color='black', linestyle='--', label='Czas podróży bez punktu postoju = 10.41958')

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Wariancja czasów podróży', color=color)
ax2.plot(dane['symulacja'], dane['wariancja_czasow_podrozy'], label='Wariancja czasów podróży', color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.axhline(y=28.8216, color='red', linestyle='--', label='Wariancja bez puntku postoju= 28.8216')

fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
plt.title('Wyniki symulacji windy')
plt.show()
