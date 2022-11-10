import os
import pickle
import random
import time

from config import ACTIONS


class Agent:
    def __init__(self, alpha=1, gamma=1, exploration=1, cooling_rate=1):
        self.last_action = None
        self.state = [0] * 10
        self.qtables = {}
        self.init_state_in_qtable()
        self.init_radar()
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate
        self.__timer = time.time()
        self.previous_bp = [0] * 10
        self.actions = 0


    def init_radar(self):
        self.radar = {"zone": [[0] * 10 for _ in range(4)],
                        "y": 19}

    def init_state_in_qtable(self):

        if os.path.exists("agent.dat"):
            self.load("agent.dat")
            return

        self.qtables = {}
        #print(self.qtables)

    def change_state(self, grid):
        tmp = []
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if y < len(grid[x])-1 and y+1 == 0:
                    tmp.append(y)
                    self.state = tmp


    def table_to_str(self, table):
        return ''.join(map(str, table))

    def insert_reward_in_state_qtable(self, mino, x, value, boundaries, rotation):
        x += 2
        self.previous_bp = boundaries
        # self.__insert_reward_in_state_qtable(state,5, 50)
        state_str = self.table_to_str(boundaries)
        self.upsert_boundary_qtable(mino, state_str, x, rotation)
        #print(rotation)
        maxQ = max(self.qtables[state_str][mino - 1][x][rotation].values())
        self.qtables[state_str][mino - 1][x][rotation][self.last_action] += self.__alpha * \
                                                                  (value + self.__gamma * maxQ -
                                                                   self.qtables[state_str][mino - 1][x][rotation][
                                                                       self.last_action])
        # print(self.qtables[mino - 1][state_str][x])

        self.state = boundaries


    def upsert_boundary_qtable(self, mino, state_str, x, rotation):
        if state_str not in self.qtables:
            self.qtables[state_str] = {}
        if state_str not in self.qtables[state_str]:
            self.qtables[state_str][mino - 1] = {}
        if state_str not in self.qtables[state_str][mino - 1]:
            self.qtables[state_str][mino - 1][x] = {}
        if x not in self.qtables[state_str][mino - 1][x]:
            self.qtables[state_str][mino - 1][x][rotation] = {'NOTHING': 0, 'LEFT': 0, 'RIGHT': 0, 'ROTATE': 0}

    def best_action(self, mino, dx, rotation):
        hash = ''.join(str(x) for x in self.state)
        piece_x = dx

        self.actions += 1

        try:
            actions = self.qtables[hash][mino - 1][piece_x + 2][rotation]

            if random.uniform(0, 1) < self.__exploration:
                self.__exploration *= self.__cooling_rate
                return random.choice(ACTIONS)
            else:
                return max(ACTIONS, key=actions.get)
        except KeyError:
            return random.choice(ACTIONS)
        # if not hash in self.qtables[mino-1]:
        #     self.qtables[mino - 1][hash] = [{'NOTHING': 0, 'LEFT': 0, 'RIGHT': 0, 'ROTATE': 0} for i in range(11)]
        #     actions = self.qtables[mino - 1][hash][piece_x + 2]
        # else:
        #     actions = self.qtables[mino - 1][hash][piece_x + 2]

        # print(actions)


    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.qtables, file)

    def load(self, filename):
        start = time.time()
        with open(filename, 'rb') as file:
            self.qtables = pickle.load(file)
        print("qtables load in", time.time() - start, "sec")

    def step(self, mino,  dx, rotation):
        if len(self.qtables) == 0:
            self.init_state_in_qtable()
        # get best rotation
        action = self.best_action(mino, dx, rotation)
        self.last_action = action

        #print(action)

        return action

    def generate_reward(self):
        pass
