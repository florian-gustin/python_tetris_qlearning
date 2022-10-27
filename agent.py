import random

import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_UP

ACTIONS = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=pygame.KMOD_NONE),
           pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, mod=pygame.KMOD_NONE),
           pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=pygame.KMOD_NONE)]


class Agent:
    def __init__(self, alpha=1, gamma=1, exploration=1, cooling_rate=0.9999):
        self.last_action = None
        self.__state = [0 for i in range(10)]
        self.__qtable_I = {}
        self.init_state_in_qtable()
        self.init_radar()
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate

    def init_radar(self):
        self.__radar = {"zone": [[0 for i in range(10)] for j in range(4)],
                        "y": 19}

    def init_state_in_qtable(self):
        index_array = []
        state_str = ''.join(map(str, self.__state))

        for i in range(11):
            index_array.append({'NOTHING': 0, 'LEFT': 0, 'RIGHT': 0, 'ROTATE': 0})
        self.__qtable_I[state_str] = index_array
        print(self.__qtable_I)

    def insert_reward_in_state_qtable(self, x, value):
        # self.__insert_reward_in_state_qtable(state,5, 50)
        state_str = ''.join(map(str, self.__state))
        self.__qtable_I[state_str][x][self.last_action] = value

    def action(self):
        # minos = self.__env.mino
        # print(self.__env.dx)
        return pygame.event.post(random.choice(ACTIONS))

    def best_action(self, dx):
        hash = ''.join(str(x) for x in self.__state)
        piece_x = dx
        actions = self.__qtable_I[hash][piece_x+2]
        # print(actions)

        if random.uniform(0, 1) < self.__exploration:
            self.__exploration *= self.__cooling_rate
            return random.choice(list(actions.keys()))
        else:
            return max(actions, key=actions.get)

    def step(self, dx):
        if not self.__state in self.__qtable_I.values():
            self.init_state_in_qtable()

        action = self.best_action(dx)
        self.last_action = action
        key = None

        print(action)

        if action == 'LEFT':
            key = pygame.K_LEFT
        elif action == 'RIGHT':
            key = pygame.K_RIGHT
        elif action == 'ROTATE':
            key = pygame.K_UP

        if key is not None:
            event = pygame.event.Event(pygame.KEYDOWN, key=key, mod=pygame.KMOD_NONE)
            pygame.event.post(event)
