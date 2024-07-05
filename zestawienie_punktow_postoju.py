import matplotlib.pyplot as plt

# Zbiór danych z symulacji
# dane = {
#     "symulacja": list(range(11)),
#     "sredni_czas_w_windzie": [5.812071879281207, 5.75657486850263, 5.73955, 5.733052669473305, 5.725052749472505, 5.733565328693426, 5.73382, 5.71672566548669, 5.734427967160985, 5.72515, 5.73748],
#     "sredni_czas_oczekiwania_na_winde": [4.247847521524784, 4.140407191856163, 4.13573, 4.1950180498195015, 4.333576664233358, 4.56264874702506, 4.83512, 5.142547149057019, 5.5073047808565745, 5.88826, 6.28996],
#     "sredni_czas_podrozy": [10.059919400805992, 9.896982060358793, 9.87528, 9.928070719292807, 10.058629413705862, 10.296214075718485, 10.56894, 10.85927281454371, 11.24173274801756, 11.61341, 12.02744],
#     "wariancja_czasow_podrozy": [33.003739592107785, 30.030726477328617, 27.5823449216, 25.709459032248407, 24.050652050953918, 23.445426557959507, 22.885267276399997, 22.941126640657924, 23.205267367473212, 23.362958171899997, 23.798087046399996]
# }
# dane = {
#     "symulacja": list(range(11)),
#     "sredni_czas_podrozy": [10.27279, 10.32638, 10.312193756124877, 10.357886421135788,
#     10.54067, 10.679729608111757, 10.970490590188197, 11.268304633907322,
#     11.640487190256195, 12.02938, 12.504634953650463],

#     "wariancja_czasow_podrozy": [47.5579956159, 44.912216095599995, 44.356365982018175, 40.44038162492347,
#     39.1732859511, 35.938845633517026, 36.69208533560974, 34.79208534196948,
#     36.42605943345223, 36.0969968156, 37.036870648283355]
#     }

dane = {
    "symulacja": list(range(6)),
    "sredni_czas_podrozy": [
        10.26512,  # Simulation 0
        10.20471,  # Simulation 1
        10.18186,  # Simulation 2
        10.18836,  # Simulation 3
        10.21555,  # Simulation 4
        10.25785   # Simulation 5
    ],
    "wariancja_czasow_podrozy": [
        49.6001313856,  # Simulation 0
        47.1560238158,  # Simulation 1
        46.4019869404,  # Simulation 2
        46.3525805104,  # Simulation 3
        47.4555281975,  # Simulation 4
        48.7066633775   # Simulation 5
    ]
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
ax1.axhline(y=10.30, color='black', linestyle='--', label='Czas podróży z samym punktem postoju = 10.30')

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Wariancja czasów podróży', color=color)
ax2.plot(dane['symulacja'], dane['wariancja_czasow_podrozy'], label='Wariancja czasów podróży', color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.axhline(y=49.40732, color='red', linestyle='--', label='Wariancja z samym punktem postoju = 49.40732')

fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
plt.title('Wyniki symulacji windy')
plt.show()

