import random
import time
from gymnasium import Env
from gymnasium.spaces import Discrete, Box
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from collections import deque
import matplotlib.pyplot as plt

class Winda(Env):
    def __init__(self):
        super(Winda, self).__init__()
        self.kierunek = 0  
        self.pietro = random.randint(0, 2)
        self.pasazerowie_w_windzie = []
        self.zgloszenia = []
        self.historia = []
        self.czas = 0
        self.czasy_pasazerow = []
        self.czasy_oczekiwania_pasazerow = []
        self.obsłużeni_pasażerowie = 0
        self.action_space = Discrete(2)
        self.observation_space = Box(low=0, high=2, shape=(10,), dtype=np.int32)
        
        self.state_size = 10  # 1 (pozycja) + 3 (pasażerowie czekający) + 6 (pasażerowie w windzie)
        self.action_size = 2  # Jazda w górę, jazda w dół
        self.memory = deque(maxlen=5000) # bufor odtwarzania
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99
        self.learning_rate = 0.001
        self.model = None

    def dodaj_zgloszenie(self, pasazer):
        self.historia.append(pasazer)
        self.zgloszenia.append(pasazer)

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

    def step(self, action):
        # jedź w górę
        if action == 0 and self.pietro < 2:
            self.pietro += 1
        # jedź w dół
        elif action == 1 and self.pietro > 0:
            self.pietro -= 1

        # Aktualizacja stanu pasażerów
        self.czas += 1
        for pasazer in self.pasazerowie_w_windzie:
            pasazer.licz_czas_w_windzie()
        for zgloszenie in self.zgloszenia:
            zgloszenie.licz_czas_oczekiwania_na_winde()

        # Zabieranie i wypuszczanie pasażerów
        zabrani = self.zabieraj_pasazerow()
        wysadzeni = self.wypuszczaj_pasazerow()

        # Obliczanie nagrody
        reward = wysadzeni - 0.1 * (1 if zabrani == 0 and wysadzeni == 0 else 0) 
        - 0.1 * sum([zgloszenie.czas_oczekiwania_na_winde for zgloszenie in self.zgloszenia])
        - 0.05 * sum([zgloszenie.czas_w_windzie for zgloszenie in self.pasazerowie_w_windzie])
        # Stan następny
        next_state = self._get_state()

        # Sprawdzenie, czy epizod się zakończył
        done = self.czas >= 20 or (len(self.zgloszenia) == 0 and len(self.pasazerowie_w_windzie) == 0)
        if done:
            reward -= 10 * len(self.zgloszenia) + 10 * len(self.pasazerowie_w_windzie)
        return next_state, reward, done, {}

    def reset(self):
        self.kierunek = 0  
        self.pietro = random.randint(0, 2)
        self.pasazerowie_w_windzie = []
        self.zgloszenia = []
        self.historia = []
        self.czas = 0
        self.czasy_pasazerow = []
        self.czasy_oczekiwania_pasazerow = []
        self.obsłużeni_pasażerowie = 0
        return self._get_state()

    def render(self, mode='human'):
        print(f"Piętro: {self.pietro}, Pasażerowie w windzie: {len(self.pasazerowie_w_windzie)}, Zgłoszenia: {len(self.zgloszenia)}")

    def _get_state(self):
        # Pozycja windy
        state = [self.pietro]

        # Pasażerowie czekający
        oczekujacy = [0, 0, 0]
        for zgloszenie in self.zgloszenia:
            oczekujacy[zgloszenie.start] += 1
        state.extend(oczekujacy)

        # Pasażerowie w windzie
        pasazerowie = [0, 0, 0, 0, 0, 0]
        for pasazer in self.pasazerowie_w_windzie:
            if pasazer.cel == 0:
                pasazerowie[0] += 1
            elif pasazer.cel == 1:
                pasazerowie[2] += 1
            elif pasazer.cel == 2:
                pasazerowie[4] += 1
        state.extend(pasazerowie)
        
        return np.array(state, dtype=np.float32)

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(np.array([state]), verbose=0)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        start_time = time.time()  # Profilowanie czasu dla replay
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(np.array([next_state]), verbose=0)[0]))
            target_f = self.model.predict(np.array([state]), verbose=0)
            target_f[0][action] = target
            self.model.fit(np.array([state]), target_f, epochs=2, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        end_time = time.time()  # Koniec profilowania czasu dla replay
        print(f"Replay time: {end_time - start_time:.4f} seconds")  # Wyświetlenie czasu trwania replay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


class Pasazer:
    def __init__(self):
        self.start = random.randint(0, 2)
        self.cel = random.randint(0, 2)
        while self.start == self.cel:
            self.cel = random.randint(0, 2)
        self.kierunek = 0 if self.start < self.cel else 1
        self.czas_w_windzie = 0
        self.czas_oczekiwania_na_winde = 0
    
    def licz_czas_w_windzie(self):
        self.czas_w_windzie += 1

    def licz_czas_oczekiwania_na_winde(self):
        self.czas_oczekiwania_na_winde += 1

# Main training loop
winda = Winda()
episodes = 200
batch_size = 32

# Przechowywanie wyników do analizy
rewards = []
steps = []

for e in range(episodes):
    state = winda.reset()
    total_reward = 0
    for _ in range(3):
        jacek = Pasazer()
        winda.dodaj_zgloszenie(jacek)
    for timer in range(20):
        if timer % 10 == 0:
            print(f"Time: {timer}")
        action = winda.act(state)
        next_state, reward, done, _ = winda.step(action)
        total_reward += reward
        winda.remember(state, action, reward, next_state, done)
        state = next_state
        if done:
            break
        if len(winda.memory) > batch_size and timer % 10 == 0:  # Zmniejszenie częstotliwości treningu
            winda.replay(batch_size)
    rewards.append(total_reward)
    steps.append(timer)
    print(f"Episode: {e+1}/{episodes}, Reward: {total_reward}, Steps: {timer}, Epsilon: {winda.epsilon:.2}")

    if (e + 1) % 50 == 0:
        winda.save(f"winda_dqn_{e+1}.weights.h5")
winda.save(f"winda_dqn_final.weights.h5")

# Analiza wyników
plt.plot(range(episodes), rewards)
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.show()

plt.plot(range(episodes), steps)
plt.xlabel('Episode')
plt.ylabel('Steps')
plt.show()
