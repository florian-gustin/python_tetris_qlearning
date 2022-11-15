import os
import pickle
import random
import shutil
import time
import lzma
from sys import getsizeof

import xxhash

from constants.config import ACTION_ROTATE, ACTION_LEFT, ACTION_RIGHT
from constants.tetri_mino import TetriMino


class Agent:
    def __init__(self, alpha=1, gamma=1, exploration=0, cooling_rate=1):
        self.last_action = 0
        self.state = [0] * 10
        self.reward_count = 0
        self.reward_count_history = []
        self.qtables = {}
        self.init_state_in_qtable()
        self.init_radar()
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate
        self.timer = time.time()
        self.previous_bp = "000000000"
        self.previous_state = [0] * 10
        self.actions = 0


    def reset_reward_counter(self):
        self.reward_count_history.append(self.reward_count)
        self.reward_count = 0

    def reset_history(self):
        self.reward_count_history = []

    def init_radar(self):
        self.radar = {"zone": [[0] * 10 for _ in range(4)],
                      "y": 19}

    def init_state_in_qtable(self):
        if len(self.qtables) == 0:
            if os.path.exists("agent.dat"):
                self.load_qtable("agent.dat")
            else:
                self.qtables = {}
        print(getsizeof(self.qtables))
        return

    def change_state(self, grid):
        tmp = []
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if y < len(grid[x]) - 1 and y + 1 == 0:
                    tmp.append(y)
                    self.state = tmp

    def table_to_str(self, table):
        return ''.join(map(str, table))

    def insert_reward_in_state_qtable(self, mino, x, value, state_str, rotation):
            # print(state_str)
            # print("ROTATION", rotation)
            # print("MINO - 1", mino - 1)
            # print(self.qtables[state_str][mino - 1][rotation])
            maxQ = None
            # print("MINOOOO", mino)
            for rot in range(len(TetriMino.mino_map[mino - 1])):
                for x_ in range(TetriMino.mino_map[mino - 1][rot]['X_RANGE']):
                    key = xxhash.xxh32_digest(state_str + ':' + str(mino - 1) + ':' + str(rotation) + ':' + str(x_))
                    reward = self.qtables[key] if key in self.qtables else 0
                    if maxQ is None or reward > maxQ:
                        maxQ = reward

            # (1 - self.__alpha) * qtable[action] + self.__alpha * (reward + self.__gamma * max_q)  <- version du projet noe pieerre
            key = xxhash.xxh32_digest(state_str + ':' + str(mino - 1) + ':' + str(rotation) + ':' + str(x))
            current_reward = self.qtables[key] if key in self.qtables else 0
            tmp = self.__alpha * (value + self.__gamma * maxQ - current_reward)
            self.qtables[xxhash.xxh32_digest(state_str+':'+str(mino - 1)+':'+str(rotation)+':'+str(x))] = tmp
            self.reward_count += tmp
            # print("INSERT QTABLE : key = ", state_str, ", mino = ", mino - 1, ", x = ", x, ", rotation = ", rotation,
            #      ", value = ", tmp)

            self.state = state_str


    def upsert_boundary_qtable(self, mino, state_str):
        self.previous_state = state_str
        state_str = self.table_to_str(state_str)
        self.previous_bp = state_str

    def best_actions(self, mino, dx, boundaries):

        table_action = []  # tout les actions que doit faire l'agent ici

        rotation, x = self.best_action(mino, boundaries)

        if dx > x:
            for i in range(x, dx):
                table_action.append(ACTION_LEFT)
            for i in range(rotation):
                table_action.append(ACTION_ROTATE)
        else:
            for i in range(rotation):
                table_action.append(ACTION_ROTATE)
            for i in range(dx, x):
                table_action.append(ACTION_RIGHT)

        # print(table_action)
        return table_action, rotation, x

    def best_action(self, mino, boundaries):
        self.actions += 1

        if random.uniform(0, 1) < self.__exploration:
            self.__exploration *= self.__cooling_rate
            rotation = len(TetriMino.mino_map[mino - 1]) - 1
            # print("MINO - 1", mino - 1)
            # print("ROTATION", rotation)
            x_range = TetriMino.mino_map[mino - 1][rotation]['X_RANGE'] - 1
            # print("XRANGE", x_range)
            return random.randint(0, rotation), random.randint(0, x_range)
        else:
            hash = ''.join(map(str, boundaries))
            best_rotation = 0
            best_x = 0
            best_reward = None
            # print("MINOOOO", mino)
            for rotation in range(len(TetriMino.mino_map[mino - 1])):
                for x in range(TetriMino.mino_map[mino - 1][rotation]['X_RANGE']):
                    key = xxhash.xxh32_digest(hash + ':' + str(mino - 1) + ':' + str(rotation) + ':' + str(x))
                    reward = self.qtables[key] if key in self.qtables else 0
                    if best_reward is None or reward > best_reward:
                        best_rotation = rotation
                        best_x = x
                        best_reward = reward
            return best_rotation, best_x

    def save_qtable(self, filename):
        self.qtables = {key: value for key, value in self.qtables.items() if value != 0}
        with lzma.open(filename + ".tmp", 'w') as file:
            pickle.dump(self.qtables, file)
        shutil.move(filename + ".tmp", filename)

    def save_history(self, filename):
        with open(filename, 'a') as file:
            for reward in self.reward_count_history:
                file.write(str(reward)+"\n")

    def load_qtable(self, filename):
        start = time.time()
        with lzma.open(filename, 'r') as file:
            self.qtables = pickle.load(file)
        print(len(self.qtables))
        self.qtables = {key: value for key, value in self.qtables.items() if value != 0}
        print(len(self.qtables))

        print(filename, " load in", time.time() - start, "sec")

    def load_history(self, filename):
        history = []
        with open(filename, 'r') as file:
            for line in file:
                history.append(int(line))
        return history