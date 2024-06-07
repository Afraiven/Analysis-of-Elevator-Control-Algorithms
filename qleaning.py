import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
import pickle
from prototyp_wizualizacji import draw_elevator

class Winda(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(Winda, self).__init__()
        
        self.steps_done = 0
        self.num_floors = 11
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Dict({
            "current_floor": spaces.Discrete(self.num_floors),
            "doors_open": spaces.Discrete(2),
            "waiting_floors": spaces.MultiBinary(self.num_floors)  # flagi dla każdego piętra, czy ktoś czeka
        })
        self.state = None
        self.reset()
        self.Q = np.zeros((self.num_floors, 2, 2 ** self.num_floors, 4))  # Inicjalizacja tablicy Q-wartości
    def load_Q(self, filename):
                with open(filename, 'rb') as f:
                  self.Q = pickle.load(f)
    def step(self, action):
        assert self.action_space.contains(action), f"{action} nie jest prawidłową akcją"
        current_floor, doors_open, waiting_floors = self.state['current_floor'], self.state['doors_open'], self.state['waiting_floors']
        reward = 0
        done = False

        if action == 0:  # Move up
            if current_floor < self.num_floors - 1:
                if doors_open == 1:
                    reward = -1
                else:
                    current_floor += 1
            else:
                reward -= 2
        elif action == 1:  # Move down
            if current_floor > 0:
                if doors_open == 1:
                    reward = -1
                else:
                    current_floor -= 1
            else:
                reward -= 2
        elif action == 2:  # Open doors
            if doors_open == 0:
                doors_open = 1
                if waiting_floors[current_floor]:
                    reward += 2
            else:
                reward -= 1
        elif action == 3:  # Close doors
            if doors_open == 1:
                doors_open = 0
            else:
                reward -= 1
        for wait in waiting_floors:
            if wait == 1:
                reward -= 0.2
        if doors_open and waiting_floors[current_floor]:
            reward += 50  # Nagroda za otwarcie drzwi, gdy ktoś czeka
            waiting_floors[current_floor] = 0  # Usuwanie pasażera z listy oczekujących

        self.state = {
            "current_floor": current_floor,
            "doors_open": doors_open,
            "waiting_floors": waiting_floors
        }

        # if self.steps_done >= 100 or np.sum(waiting_floors) == 0:
        if np.sum(waiting_floors) == 0:
            reward /= self.normalizer
            done = True
        # else:
        #     self.new_passenger()
        self.steps_done += 1
        return self.state, reward, done, {}

    def new_passenger(self):
        if random.random() < 0.01:
            floor = random.randint(0, self.num_floors - 1)
            self.state['waiting_floors'][floor] = 1

    def reset(self):
        x = np.random.randint(0, 2, self.num_floors)
        self.state = {
            "current_floor": 0,
            "doors_open": 0,
            "waiting_floors": x
        }
        self.normalizer = sum(x)
        self.steps_done = 0
        return self.state

    def render(self, mode='human', close=False):
        if close:
            return
        waiting_floors_list = list(np.where(self.state['waiting_floors'])[0])
        waiting_floors_list_normalized = []
        for i in range(self.num_floors):
            if i in waiting_floors_list:
                waiting_floors_list_normalized.append([1])
            else:
                waiting_floors_list_normalized.append([])
        if len(results) > 0 and (len(results) % 450 == 0 or len(results) % 490 == 0):
            time_step = 0.05
        else:
            time_step = 0.05
        draw_elevator(self.state['current_floor'], waiting_floors_list_normalized, time_step)
        output = f"Winda znajduje się na piętrze {self.state['current_floor']}. "
        output += "Drzwi są otwarte. " if self.state['doors_open'] else "Drzwi są zamknięte. "
        output += f"Pasażerowie czekają na piętrach: {waiting_floors_list}."
        print(output)

    def close(self):
        pass

    def state_to_index(self, state):
        current_floor = state['current_floor']
        doors_open = state['doors_open']
        waiting_floors = int(''.join(map(str, state['waiting_floors'])), 2)
        return current_floor, doors_open, waiting_floors

    def update_Q(self, state, action, reward, next_state, alpha, gamma):
        state_idx = self.state_to_index(state)
        next_state_idx = self.state_to_index(next_state)
        old_value = self.Q[state_idx][action]
        next_max = np.max(self.Q[next_state_idx])
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        self.Q[state_idx][action] = new_value

    def choose_action(self, state, epsilon):
        if random.uniform(0, 1) < epsilon:
            return self.action_space.sample()  # losowa akcja
        else:
            state_idx = self.state_to_index(state)
            return np.argmax(self.Q[state_idx])  # najlepsza znana akcja

epsilon = 0.01
alpha = 0.3
gamma = 0.3
env = Winda()
env.load_Q('q_table.pkl')  # Załaduj wcześniej zapisaną tabelę Q
results = []
ile_epizodow = 500

for i in range(ile_epizodow):
    state = env.reset()
    done = False
    episode_rewards = 0
    print("*"*30,f"Epizod {i + 1}","*"*30)
    print(f"Epsilon: {epsilon:.2f}")
    while not done:
        action = env.choose_action(state, epsilon)
        next_state, reward, done, info = env.step(action)
        env.update_Q(state, action, reward, next_state, alpha, gamma)
        state = next_state
        episode_rewards += reward
        env.render()
    print(f"Nagrody z epizodu: {episode_rewards}")
    results.append(episode_rewards)
    epsilon *= 0.995 

env.close()

with open('final_training_results.pkl', 'wb') as f:
    pickle.dump(results, f)

with open('q_table.pkl', 'wb') as f:
    pickle.dump(env.Q, f)

import matplotlib.pyplot as plt

# Tworzenie wykresu
plt.plot(results)
plt.xlabel('Epizod')
plt.ylabel('Suma nagród')
plt.title('Postęp uczenia się agenta w każdym epizodzie')
plt.show()
