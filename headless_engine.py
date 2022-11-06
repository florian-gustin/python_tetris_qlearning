from __future__ import annotations

import operator
from abc import ABC, abstractmethod
from random import randint

from pygame import QUIT, USEREVENT, KEYDOWN, K_ESCAPE, K_DOWN, K_SPACE, K_LSHIFT, K_c, K_UP, K_x, K_z, K_LCTRL, K_LEFT, \
    K_RIGHT, K_RETURN
from pygame.rect import Rect

from rewards import HOLE_REWARD, LINE_CLEAR_REWARD
from ui_configuration import *
from tetri_mino import *
import pygame
from pygame.event import Event


class Event:
    def __init__(self, typex, key, mod) -> None:
        super().__init__()
        self.type = typex
        self.key = key
        self.mod = mod


class HeadlessEngine:

    def __init__(self, environment, agent) -> None:
        super().__init__()
        self.__framerate = 15  # Bigger -> Slower
        self.__clock = pygame.time.Clock()
        self.__environment = environment
        self.__agent = agent


        self.__events = []

        self.__keys = []


    def on_start(self):

        for event in self.__events:
            if event.type == QUIT:
                self.__environment.done = True
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # self.ui_configuration.click_sound.play()
                    self.__environment.start = True


        if self.__environment.blink:
            self.__environment.blink = False
        else:
            self.__environment.blink = True

        if not self.__environment.start:
            self.__clock.tick(3)



    def on_game(self):

        self.__events.clear()
        self.__events.append(Event(USEREVENT, pygame.K_DOWN, pygame.KMOD_NONE))
        for event in self.__events:
            self.__events.append(self.__agent.step(self.__environment.mino, self.__environment.dx, self.__events))
            # if event.type == QUIT:
            #     self.__environment.done = True
            #     self.__agent.save("agent.dat")
            if event.type == USEREVENT:
                # Set speed
                if not self.__environment.game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        self.__pygame.time.set_timer(USEREVENT, self.__framerate * 1)
                    else:
                        self.__pygame.time.set_timer(USEREVENT, self.__framerate * 10)

                # Draw a mino
                self.__environment.draw_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                             self.__environment.rotation)

                # Erase a mino
                if not self.__environment.game_over:
                    self.__environment.erase_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                                  self.__environment.rotation)

                # Move mino down
                if not self.__environment.is_bottom(self.__environment.dx, self.__environment.dy,
                                                    self.__environment.mino,
                                                    self.__environment.rotation):
                    self.__environment.dy += 1

                # Create new mino
                else:

                    if self.__environment.hard_drop or self.__environment.bottom_count == 1:
                        self.__agent.change_state(self.__environment.matrix)

                        self.__environment.set_previous_boundaries()
  # fake reward


                        self.__environment.hard_drop = False
                        self.__environment.bottom_count = 0
                        self.__environment.score += 10 * self.__environment.level
                        self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                                     self.__environment.mino,
                                                     self.__environment.rotation)

                        lines_count = self.__environment.erase_count * LINE_CLEAR_REWARD
                        holes_count = self.__environment.holes_created_count() * HOLE_REWARD
                        reward = lines_count + holes_count
                        self.__agent.insert_reward_in_state_qtable(self.__environment.mino, self.__environment.dx,
                                                                   reward,
                                                                   self.__environment.get_boundaries())

                        if self.__environment.is_stackable(self.__environment.next_mino):
                            self.__environment.mino = self.__environment.next_mino
                            self.__environment.next_mino = randint(1, 7)
                            self.__environment.dx, self.__environment.dy = 3, 0
                            self.__environment.rotation = 0
                            self.__environment.hold = False
                        else:
                            self.__environment.start = False
                            self.__environment.game_over = True
                            self.__events.clear()
                            self.__events.append(Event(USEREVENT, 0, pygame.KMOD_NONE))

                    else:
                        self.__environment.bottom_count += 1

                    # Erase line
                    self.__environment.try_erase_line()

                # Increase level
                self.__environment.goal -= self.__environment.erase_count
                if self.__environment.goal < 1 and self.__environment.level < 15:
                    self.__environment.level += 1
                    self.__environment.goal += self.__environment.level * 5
                    self.__framerate = int(self.__framerate * 0.8)

            elif event.type == KEYDOWN:
                self.__environment.erase_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                              self.__environment.rotation)
                if event.key == K_ESCAPE:
                    # self.ui_configuration.click_sound.play()
                    self.__environment.pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    while not self.__environment.is_bottom(self.__environment.dx, self.__environment.dy,
                                                           self.__environment.mino, self.__environment.rotation):
                        self.__environment.dy += 1
                    self.__environment.hard_drop = True
                    self.__events.append(Event(USEREVENT, 0, pygame.KMOD_NONE))
                    self.__environment.draw_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                                 self.__environment.rotation)
                # Turn right
                elif event.key == K_UP or event.key == K_x:

                    if self.__environment.is_turnable_r(self.__environment.dx, self.__environment.dy,
                                                        self.__environment.mino, self.__environment.rotation):
                        self.__environment.rotation += 1
                    # Kick
                    elif self.__environment.is_turnable_r(self.__environment.dx, self.__environment.dy - 1,
                                                          self.__environment.mino, self.__environment.rotation):
                        self.__environment.dy -= 1
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_r(self.__environment.dx + 1,
                                                          self.__environment.dy, self.__environment.mino,
                                                          self.__environment.rotation):
                        self.__environment.dx += 1
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_r(self.__environment.dx - 1, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        self.__environment.dx -= 1
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_r(self.__environment.dx, self.__environment.dy - 2,
                                                          self.__environment.mino, self.__environment.rotation):
                        self.__environment.dy -= 2
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_r(self.__environment.dx + 2, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        self.__environment.dx += 2
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_r(self.__environment.dx - 2, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        self.__environment.dx -= 2
                        self.__environment.rotation += 1
                    if self.__environment.rotation == 4:
                        self.__environment.rotation = 0
                    self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                                 self.__environment.mino, self.__environment.rotation)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if self.__environment.is_turnable_l(self.__environment.dx, self.__environment.dy,
                                                        self.__environment.mino, self.__environment.rotation):
                        self.__environment.rotation -= 1
                    # Kick
                    elif self.__environment.is_turnable_l(self.__environment.dx, self.__environment.dy - 1,
                                                          self.__environment.mino, self.__environment.rotation):
                        self.__environment.dy -= 1
                        self.__environment.rotation -= 1
                    elif self.__environment.is_turnable_l(self.__environment.dx + 1, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        self.__environment.dx += 1
                        self.__environment.rotation -= 1
                    elif self.__environment.is_turnable_l(self.__environment.dx - 1, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        self.__environment.dx -= 1
                        self.__environment.rotation -= 1
                    elif self.__environment.is_turnable_l(self.__environment.dx, self.__environment.dy - 2,
                                                          self.__environment.mino, self.__environment.rotation):
                        self.__environment.dy -= 2
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_l(self.__environment.dx + 2, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        self.__environment.dx += 2
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_l(self.__environment.dx - 2, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        self.__environment.dx -= 2
                    if self.__environment.rotation == -1:
                        self.__environment.rotation = 3
                    self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                                 self.__environment.mino, self.__environment.rotation)
                # Move left
                elif event.key == K_LEFT:
                    if not self.__environment.is_leftedge(self.__environment.dx, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        self.__environment.dx -= 1
                    self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                                 self.__environment.mino, self.__environment.rotation)

                # Move right
                elif event.key == K_RIGHT:
                    if not self.__environment.is_rightedge(self.__environment.dx, self.__environment.dy,
                                                           self.__environment.mino, self.__environment.rotation):
                        self.__environment.dx += 1
                    self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                                 self.__environment.mino, self.__environment.rotation)

    def on_reset(self):
        self.__environment.next()
        self.__environment.reset(True)

    def on_game_over(self):
        for event in self.__events:
            if event.type == QUIT:
                self.__environment.done = True
            elif event.type == USEREVENT:
                self.__events.append(Event(USEREVENT, pygame.KEYDOWN, pygame.KMOD_NONE))

                if self.__environment.blink:
                    self.__environment.blink = False
                else:
                    self.__environment.blink = True

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:

                    outfile = open('leaderboard.txt', 'a')
                    outfile.write(chr(self.__environment.name[0]) + chr(self.__environment.name[1]) + chr(
                        self.__environment.name[2]) + ' ' + str(self.__environment.score) + '\n')
                    outfile.close()

                    self.__environment.game_over = False
                    self.__environment.hold = False
                    self.__environment.dx, self.__environment.dy = 3, 0
                    self.__environment.rotation = 0
                    self.__environment.mino = randint(1, 7)
                    self.__environment.next_mino = randint(1, 7)
                    self.__environment.hold_mino = -1
                    self.__environment.framerate = 30
                    self.__environment.score = 0
                    self.__environment.level = 1
                    self.__environment.goal = self.__environment.level * 5
                    self.__environment.bottom_count = 0
                    self.__environment.hard_drop = False
                    self.__environment.name_location = 0
                    self.__environment.name = [65, 65, 65]
                    self.__environment.matrix = [[0 for y in range(self.__environment.height + 1)] for x in
                                                 range(self.__environment.width)]

                    # self.__pygame.time.set_timer(USEREVENT, 1)
                elif event.key == K_RIGHT:
                    if self.__environment.name_location != 2:
                        self.__environment.name_location += 1
                    else:
                        self.__environment.name_location = 0
                    # self.__pygame.time.set_timer(USEREVENT, 1)
                elif event.key == K_LEFT:
                    if self.__environment.name_location != 0:
                        self.__environment.name_location -= 1
                    else:
                        self.__environment.name_location = 2
                    # self.__pygame.time.set_timer(USEREVENT, 1)
                elif event.key == K_UP:
                    if self.__environment.name[self.__environment.name_location] != 90:
                        self.__environment.name[self.__environment.name_location] += 1
                    else:
                        self.__environment.name[self.__environment.name_location] = 65
                    # self.__pygame.time.set_timer(USEREVENT, 1)
                elif event.key == K_DOWN:
                    # self.ui_configuration.click_sound.play()
                    if self.__environment.name[self.__environment.name_location] != 65:
                        self.__environment.name[self.__environment.name_location] -= 1
                    else:
                        self.__environment.name[self.__environment.name_location] = 90
                    # self.__pygame.time.set_timer(USEREVENT, 1)
