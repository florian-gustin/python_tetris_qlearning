import os
import pickle
import random
import time

from config import ACTIONS, ACTION_ROTATE, ACTION_LEFT, ACTION_RIGHT


class Agent:
    def __init__(self, alpha=1, gamma=1, exploration=0, cooling_rate=1):
        self.last_action = 0
        self.state = [0] * 10
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

        self.best_rewards = [-9999]*10


    def init_radar(self):
        self.radar = {"zone": [[0] * 10 for _ in range(4)],
                        "y": 19}

    def init_state_in_qtable(self):
        if len(self.qtables) == 0:
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

    def insert_reward_in_state_qtable(self, mino, x, value, state_str, rotation):
        # x += 2
        # self.previous_bp = boundaries
        # self.__insert_reward_in_state_qtable(state,5, 50)
        #print(rotation)
        print(state_str)
        maxQ = max(self.qtables[state_str][mino - 1][x])
        tmp = self.__alpha * \
              (value + self.__gamma * maxQ -
               self.qtables[state_str][mino - 1][x][rotation])
        self.qtables[state_str][mino - 1][x][rotation] += tmp
        print("INSERT QTABLE : key = ", state_str, ", mino = ", mino-1, ", x = ", x, ", rotation = ", rotation, ", value = ", tmp)

        self.state = state_str

    def upsert_boundary_qtable(self, mino, state_str):
        self.previous_state = state_str
        state_str = self.table_to_str(state_str)
        self.previous_bp = state_str
        if state_str not in self.qtables:
            self.qtables[state_str] = {}
        if mino - 1 not in self.qtables[state_str]:
            self.qtables[state_str][mino - 1] = {}
        if len(self.qtables[state_str][mino - 1]) == 0:
            for i in range(10):
                self.qtables[state_str][mino - 1][i] = {}
                self.qtables[state_str][mino - 1][i][0] = 0
                self.qtables[state_str][mino - 1][i][1] = 0
                self.qtables[state_str][mino - 1][i][2] = 0
                self.qtables[state_str][mino - 1][i][3] = 0

    def calcul_best_actions(self, mino, dx):

        best_actions = [-99999] * 10

        for i in range(0, 10):
            _, best_actions[i] = self.best_action(mino, i)

        # return best_actions
        return max(best_actions), best_actions.index(max(best_actions))


    def best_actions(self, mino, dx, boundaries):
        self.actions += 1

        table_action = [] # tout les actions que doit faire l'agent ici

        rotation, x = self.best_action(mino, boundaries)

        for i in range(rotation):
            table_action.append(ACTION_ROTATE)
        if dx > x:
            for i in range(x, dx):
                table_action.append(ACTION_LEFT)
        else:
            for i in range(dx, x):
                table_action.append(ACTION_RIGHT)
        print(table_action)
        return table_action, rotation , x


    def best_action(self, mino, boundaries):
        self.actions += 1

        if random.uniform(0, 1) < self.__exploration:
            self.__exploration *= self.__cooling_rate
            return random.randint(0, 3), random.randint(0, 9)
        else:

            try:
                hash = ''.join(map(str, boundaries))
                rotations_indexes = []
                rotations_rewards = []
                for x, rotations in self.qtables[hash][mino - 1].items():
                    c_key = max(rotations, key=rotations.get)
                    c_rew = max(rotations.values())
                    rotations_indexes.append(c_key)
                    rotations_rewards.append(c_rew)

                x_reward = max(rotations_rewards)
                tmp_index = rotations_rewards.index(x_reward)
                x_rotation = rotations_indexes[tmp_index]

                # rotation = list(self.qtables[hash][mino - 1][x_index].keys())[list(self.qtables[hash][mino - 1][x_index]).index(max(x_rewards))]
                return x_rotation, tmp_index
            except:
                pass




    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.qtables, file)

    def load(self, filename):
        start = time.time()
        with open(filename, 'rb') as file:
            self.qtables = pickle.load(file)
        print("qtables load in", time.time() - start, "sec")

    def step(self, mino,  dx):
        if len(self.qtables) == 0:
            self.init_state_in_qtable()
        # get best rotation
        actions, rotation = self.best_actions(mino, dx)
        self.last_action = rotation

        return actions

    def generate_reward(self):
        pass
