import random

import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_UP

ACTIONS = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=pygame.KMOD_NONE),
           pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, mod=pygame.KMOD_NONE),
           pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=pygame.KMOD_NONE)]


class Agent:
    def __init__(self, alpha=1, gamma=1, exploration=0.5, cooling_rate=0.9999):
        self.last_action = None
        self.state = [0 for i in range(10)]
        self.qtables = [{}, {}, {}, {}, {}, {}, {}, ]
        self.init_state_in_qtable()
        self.init_radar()
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate


    def init_radar(self):
        self.radar = {"zone": [[0 for i in range(10)] for j in range(4)],
                        "y": 19}

    def init_state_in_qtable(self):
        index_array = []
        state_str = ''.join(map(str, self.state))

        for i in range(11):
            index_array.append({'NOTHING': 0, 'LEFT': 0, 'RIGHT': 0, 'ROTATE': 0})
        for i in range(7):
            self.qtables[i][state_str] = index_array
        # self.__qtable_I[state_str] = index_array
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

    def insert_reward_in_state_qtable(self, mino, x, value, boundaries):
        # self.__insert_reward_in_state_qtable(state,5, 50)
        state_str = self.table_to_str(boundaries)
        self.upsert_boundary_qtable(mino, state_str)

        self.qtables[mino - 1][state_str][x][self.last_action] = value
        #print(self.qtables)

        self.state = boundaries


    def upsert_boundary_qtable(self, mino, state_str):
        self.qtables[mino - 1][state_str] = []
        if len(self.qtables[mino - 1][state_str]) == 0:
            for i in range(11):
                self.qtables[mino - 1][state_str] = [{'NOTHING': 0, 'LEFT': 0, 'RIGHT': 0, 'ROTATE': 0} for i in range(11)]
    def action(self):
        # minos = self.__env.mino
        # print(self.__env.dx)
        return pygame.event.post(random.choice(ACTIONS))

    def best_action(self, mino, dx):
        hash = ''.join(str(x) for x in self.state)
        piece_x = dx

        if hash in self.qtables[mino-1]:
            actions = self.qtables[mino - 1][hash][piece_x + 2]

            if random.uniform(0, 1) < self.__exploration:
                self.__exploration *= self.__cooling_rate
                return random.choice(list(actions.keys()))
            else:
                return max(actions, key=actions.get)

        return random.choice(list({'NOTHING': 0, 'LEFT': 0, 'RIGHT': 0, 'ROTATE': 0}.keys()))

        # if not hash in self.qtables[mino-1]:
        #     self.qtables[mino - 1][hash] = [{'NOTHING': 0, 'LEFT': 0, 'RIGHT': 0, 'ROTATE': 0} for i in range(11)]
        #     actions = self.qtables[mino - 1][hash][piece_x + 2]
        # else:
        #     actions = self.qtables[mino - 1][hash][piece_x + 2]

        # print(actions)



    def step(self, mino,  dx):
        if len(self.qtables) == 0:
            self.init_state_in_qtable()
        # get best rotation
        action = self.best_action(mino, dx)
        self.last_action = action
        key = None

        #print(action)

        if action == 'LEFT':
            key = pygame.K_LEFT
        elif action == 'RIGHT':
            key = pygame.K_RIGHT
        elif action == 'ROTATE':
            key = pygame.K_UP

        if key is not None:
            event = pygame.event.Event(pygame.KEYDOWN, key=key, mod=pygame.KMOD_NONE)
            # pygame.event.post(event)

    def generate_reward(self):
        pass
