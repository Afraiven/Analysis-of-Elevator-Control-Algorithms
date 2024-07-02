import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
from gymnasium import Env
from gymnasium.spaces import Discrete, Box, Tuple, MultiBinary
import pygame

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
        reward = 0
        # Move the agent based on the selected action
        if action == 0:  # Up
            if self.pietro < 3:
                self.pietro += 1
        elif action == 1:  # Down
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
        print("Winda na piętrze: ", self.pietro)
        print([[x.start, x.cel] for x in self.zgloszenia])
        print([[x.start, x.cel] for x in self.pasazerowie_w_windzie])
        print("Stan windy: ", self.state)
    '''
    reset() : Resets the environment to the initial state, required before calling step.
    Returns the first agent observation for an episode and information, i.e. metrics, debug info.

    step() : Updates an environment with actions returning the next agent observation,
     the reward for taking that actions, if the environment has terminated or truncated
         due to the latest action and information from the environment about the step,
     i.e. metrics, debug info.

    render() : Renders the environments to help visualise what the agent see, examples
    modes are “human”, “rgb_array”, “ansi” for text.

    close() : Closes the environment, important when external software is used, i.e.
    pygame for rendering, databases
 '''
    
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
replay_buffer = deque(maxlen=4000)
batch_size = 32
discount_factor = 0.9
optimizer = Adam(learning_rate=1e-3)
loss_fn = tf.keras.losses.MeanSquaredError()

model = Sequential([
    Dense(32, activation="elu", input_shape=input_shape),
    Dense(32, activation="elu"),
    Dense(16, activation="relu"),
    Dense(n_outputs)
])

def epsilon_greedy_policy(state, epsilon=0):
    if np.random.rand() < epsilon:
        return np.random.randint(2)
    else:
        Q_values = model.predict(state[np.newaxis], verbose=0)
        return np.argmax(Q_values[0])

def sample_experiences(batch_size):
    indices = np.random.randint(len(replay_buffer), size=batch_size)
    batch = [replay_buffer[index] for index in indices]
    states, actions, rewards, next_states, dones = [
        np.array([experience[field_index] for experience in batch])
        for field_index in range(5)
    ]
    return states, actions, rewards, next_states, dones

def play_one_step(env, state, epsilon):
    action = epsilon_greedy_policy(state, epsilon)
    next_state, reward, done, _ = env.step(action)
    replay_buffer.append((state, action, reward, next_state, done))
    return next_state, reward, done

def training_step(batch_size):
    experiences = sample_experiences(batch_size)
    states, actions, rewards, next_states, dones = experiences
    next_Q_values = model.predict(next_states)
    max_next_Q_values = np.max(next_Q_values, axis=1)
    target_Q_values = (rewards +
                       (1 - dones) * discount_factor * max_next_Q_values)
    mask = tf.one_hot(actions, n_outputs)
    with tf.GradientTape() as tape:
        all_Q_values = model(states)
        Q_values = tf.reduce_sum(all_Q_values * mask, axis=1, keepdims=True)
        loss = tf.reduce_mean(loss_fn(target_Q_values, Q_values))
    grads = tape.gradient(loss, model.trainable_variables)
    clipped_grads = [tf.clip_by_value(grad, -1.0, 1.0) for grad in grads]
    optimizer.apply_gradients(zip(clipped_grads, model.trainable_variables))

rewards = []
np.random.seed(42)
random.seed(42)
tf.random.set_seed(42)
best_score = 0

for episode in range(1100):
    print(f"Episode: {episode}, len(replay_buffer): {len(replay_buffer)}")
    env = AgentWinda()
    obs = env.reset()
    total_reward = 0
    for step in range(200):
        if episode == 200 or episode == 700 or episode >= 1000:
            env.render()
            input("Press Enter to continue...")
        epsilon = max(1 - episode / 1000, 0.01)
        obs, reward, done = play_one_step(env, obs, epsilon)
        total_reward += reward
        if done:
            break
    print("Epsilon: ", epsilon)
    print("Nagroda: ", total_reward, ",w", step," krokach")
    rewards.append(total_reward)
    if episode > 100:
        training_step(batch_size)
    if episode % 100 == 0:
        model.save(f"model_at_episode_{episode}.keras")
        plt.figure(figsize=(8, 4))
        plt.plot(rewards)
        plt.xlabel("Episode", fontsize=14)
        plt.ylabel("Sum of rewards", fontsize=14)
        plt.show()
plt.figure(figsize=(8, 4))
plt.plot(rewards)
plt.xlabel("Episode", fontsize=14)
plt.ylabel("Sum of rewards", fontsize=14)
plt.show()
