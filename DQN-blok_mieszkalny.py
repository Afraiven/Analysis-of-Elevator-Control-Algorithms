import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
# from srodowisko import draw_elevator
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
from gymnasium import Env
from gymnasium.spaces import Discrete, Box, Tuple, MultiBinary
import pygame
from metrics import summary

class AgentWinda(Env):
    def __init__(self):
        super(AgentWinda, self).__init__()
        self.pietro = random.randint(0, 3)
        # 4 possible actions: 0=up, 1=down, 2=left, 3=right
        self.action_space = Discrete(2)
        self.state = MultiBinary(8)
        self.pasazerowie_w_windzie = []
        self.zgloszenia = []
        self.historia = []
        self.czas = 0
        self.czasy_pasazerow = []
        self.czasy_oczekiwania_pasazerow = []
        self.obsłużeni_pasażerowie = 0
        self.reset()

    def reset(self):
        # Inicjalizacja stanu początkowego
        self.pietro = random.randint(0, 3)
        self.pasazerowie_w_windzie = []
        self.zgloszenia = []
        self.historia = []
        self.czas = 0
        self.czasy_pasazerow = []
        self.czasy_oczekiwania_pasazerow = []
        self.obsłużeni_pasażerowie = 0
        state = np.zeros(8, dtype=np.int32)
        for i in range(5):
            jacek = Pasazer()
            self.dodaj_zgloszenie(jacek)
        state[self.pietro] = 1
        
        zabrani = self.zabieraj_pasazerow()
        wysadzeni = self.wypuszczaj_pasazerow()
        for i in self.zgloszenia:
            state[4+i.start] = 1
        for i in self.pasazerowie_w_windzie:
            state[4+i.cel] = 1
        

        self.state = state
        return self.state

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
        for _ in range(5):
                X = random.randint(0, 10)
                if X == 0 and len(self.historia) < 100000:
                    jacek = Pasazer()
                    self.dodaj_zgloszenie(jacek)
        reward = 0
        # Move the agent based on the selected action
        if action == 0 and len(self.zgloszenia) + len(self.pasazerowie_w_windzie) > 0:  # Up
            if self.pietro < 3:
                self.pietro += 1
        elif action == 1 and len(self.zgloszenia) + len(self.pasazerowie_w_windzie) > 0:  # Down
            if self.pietro > 0:
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
        reward -= 0.015 * sum([zgloszenie.czas_oczekiwania_na_winde for zgloszenie in self.zgloszenia])
        reward -= 0.005 * sum([pasazer.czas_w_windzie for pasazer in self.pasazerowie_w_windzie])
            
        # Nowy stan
        nowy_stan = np.zeros(8, dtype=np.int32)
        nowy_stan[self.pietro] = 1
        for i in self.zgloszenia:
            nowy_stan[4+i.start] = 1
        for i in self.pasazerowie_w_windzie:
            nowy_stan[4+i.cel] = 1

        self.state = nowy_stan
        if (len(self.zgloszenia) + len(self.pasazerowie_w_windzie)) == 0:
            done = True
        else:
            done = False
        if self.czas >= 100:
            done = True
        return nowy_stan, reward, done, {}

    def render(self):
        osoby_na_pietrach = [[] for i in range(4)]
        for zgloszenie in self.zgloszenia:
            osoby_na_pietrach[zgloszenie.start].append(zgloszenie)
        # draw_elevator(self.pietro, osoby_na_pietrach, [x.cel for x in self.pasazerowie_w_windzie], False)
        # print("Winda na piętrze: ", self.pietro)
        # print([[x.start, x.cel] for x in self.zgloszenia])
        # print([[x.start, x.cel] for x in self.pasazerowie_w_windzie])
        # print("Stan windy: ", self.state)
    
class Pasazer:
    def __init__(self):
        self.start = random.randint(0, 3)
        self.cel = random.randint(0, 3)
        while self.start == self.cel:
            self.cel = random.randint(0, 3)
        self.kierunek = 0 if self.start < self.cel else 1
        self.czas_w_windzie = 0
        self.czas_oczekiwania_na_winde = 0

    def licz_czas_w_windzie(self):
        self.czas_w_windzie += 1

    def licz_czas_oczekiwania_na_winde(self):
        self.czas_oczekiwania_na_winde += 1

input_shape = [8]
n_outputs = 2
batch_size = 32
discount_factor = 0.9
optimizer = Adam(learning_rate=1e-3)
loss_fn = tf.keras.losses.MeanSquaredError()
# Load .keras model
model = tf.keras.models.load_model("model_at_episode_1000.keras")

def epsilon_greedy_policy(state, epsilon=0):
    if np.random.rand() < epsilon:
        return np.random.randint(2)
    else:
        Q_values = model.predict(state[np.newaxis], verbose=0)
        return np.argmax(Q_values[0])

def play_one_step(env, state, epsilon):
    action = epsilon_greedy_policy(state, epsilon)
    next_state, reward, done, _ = env.step(action)
    return next_state, reward, done

rewards = []
np.random.seed(42)
random.seed(42)
tf.random.set_seed(42)
best_score = 0

env = AgentWinda()
obs = env.reset()
total_reward = 0
while len(env.historia) < 10000 or len(env.zgloszenia) + len(env.pasazerowie_w_windzie) > 0:
    if len(env.historia) % 100 == 0:
        print(len(env.historia))
    env.render()
    epsilon = 0
    obs, reward, done = play_one_step(env, obs, epsilon)
    total_reward += reward
print(len(env.historia))
summary(env.historia, env.czas, env.czasy_pasazerow, env.czasy_oczekiwania_pasazerow)
