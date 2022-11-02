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


class TetrisEngine:

    def __init__(self, environment, agent) -> None:
        super().__init__()
        self.__framerate = 15  # Bigger -> Slower
        pygame.init()
        pygame.time.set_timer(USEREVENT, self.__framerate * 10)
        self.__pygame = pygame
        self.__clock = pygame.time.Clock()
        self.__environment = environment
        self.__agent = agent
        self.ui_configuration = UIConfiguration(self.__pygame)


    def quit(self):
        self.__pygame.quit()

    def on_start(self):
        self.score_history()
        for event in self.__pygame.event.get():
            if event.type == QUIT:
                self.__environment.done = True
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # self.ui_configuration.click_sound.play()
                    self.__environment.start = True

        # engine.set_timer(USEREVENT, 300)
        self.ui_configuration.screen.fill(self.ui_configuration.white)
        self.__pygame.draw.rect(
            self.ui_configuration.screen,
            self.ui_configuration.grey_1,
            Rect(0, 187, 300, 187)
        )

        title = self.ui_configuration.h1.render("PYTRIS™", 1, self.ui_configuration.grey_1)
        title_start = self.ui_configuration.h5.render("Press space to start", 1, self.ui_configuration.white)
        title_info = self.ui_configuration.h6.render("Copyright (c) 2017 Jason Kim All Rights Reserved.", 1,
                                                     self.ui_configuration.white)

        leader_1 = self.ui_configuration.h5_i.render(
            '1st ' + self.ui_configuration.leaders[0][0] + ' ' + str(self.ui_configuration.leaders[0][1]), 1,
            self.ui_configuration.grey_1)
        leader_2 = self.ui_configuration.h5_i.render(
            '2nd ' + self.ui_configuration.leaders[1][0] + ' ' + str(self.ui_configuration.leaders[1][1]), 1,
            self.ui_configuration.grey_1)
        leader_3 = self.ui_configuration.h5_i.render(
            '3rd ' + self.ui_configuration.leaders[2][0] + ' ' + str(self.ui_configuration.leaders[2][1]), 1,
            self.ui_configuration.grey_1)

        if self.__environment.blink:
            self.ui_configuration.screen.blit(title_start, (92, 195))
            self.__environment.blink = False
        else:
            self.__environment.blink = True

        self.ui_configuration.screen.blit(title, (65, 120))
        self.ui_configuration.screen.blit(title_info, (40, 335))

        self.ui_configuration.screen.blit(leader_1, (10, 10))
        self.ui_configuration.screen.blit(leader_2, (10, 23))
        self.ui_configuration.screen.blit(leader_3, (10, 36))

        if not self.__environment.start:
            self.__pygame.display.update()
            self.__clock.tick(3)

    def on_pause(self):
        for event in self.__pygame.event.get():
            if event.type == QUIT:
                self.__environment.done = True
            elif event.type == USEREVENT:
                self.__pygame.time.set_timer(USEREVENT, 300)
                self.draw_board(self.__environment.next_mino, self.__environment.hold_mino, self.__environment.score,
                                self.__environment.level, self.__environment.goal)

                pause_text = self.ui_configuration.h2_b.render("PAUSED", 1, self.ui_configuration.white)
                pause_start = self.ui_configuration.h5.render("Press esc to continue", 1, self.ui_configuration.white)

                self.ui_configuration.screen.blit(pause_text, (43, 100))
                if self.__environment.blink:
                    self.ui_configuration.screen.blit(pause_start, (40, 160))
                    self.__environment.blink = False
                else:
                    self.__environment.blink = True
                self.__pygame.display.update()
            elif event.type == KEYDOWN:
                self.__environment.erase_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                              self.__environment.rotation)
                if event.key == K_ESCAPE:
                    self.__environment.pause = False
                    #                     # self.ui_configuration.click_sound.play()
                    self.__pygame.set_timer(USEREVENT, 1)

    def on_game(self):

        for event in self.__pygame.event.get():
            self.__agent.step(self.__environment.mino, self.__environment.dx)
            if event.type == QUIT:
                self.__environment.done = True
                self.__agent.save("agent.dat")
            elif event.type == USEREVENT:
                # Set speed
                if not self.__environment.game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        self.__pygame.time.set_timer(USEREVENT, self.__framerate * 1)
                    else:
                        self.__pygame.time.set_timer(USEREVENT, self.__framerate * 10)

                        #
                        # pygame.time.set_timer(pygame.KEYDOWN, self.__framerate * 10)
                        # newevent = pygame.event.Event(KEYDOWN, K_LEFT)  # create the event
                        # pygame.event.post(newevent)  # a

                # Draw a mino
                self.__environment.draw_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                             self.__environment.rotation)
                self.draw_board(self.__environment.next_mino, self.__environment.hold_mino, self.__environment.score,
                                self.__environment.level, self.__environment.goal)

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



                        self.draw_board(self.__environment.next_mino, self.__environment.hold_mino,
                                        self.__environment.score,
                                        self.__environment.level, self.__environment.goal)

                        if self.__environment.is_stackable(self.__environment.next_mino):
                            self.__environment.mino = self.__environment.next_mino
                            self.__environment.next_mino = randint(1, 7)
                            self.__environment.dx, self.__environment.dy = 3, 0
                            self.__environment.rotation = 0
                            self.__environment.hold = False
                        else:
                            self.__environment.start = False
                            self.__environment.game_over = True
                            self.__pygame.time.set_timer(USEREVENT, 1)
                    else:
                        self.__environment.bottom_count += 1

                    # Erase line
                    self.__environment.try_erase_line(self.ui_configuration)

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
                    self.ui_configuration.drop_sound.play()
                    while not self.__environment.is_bottom(self.__environment.dx, self.__environment.dy,
                                                           self.__environment.mino, self.__environment.rotation):
                        self.__environment.dy += 1
                    self.__environment.hard_drop = True
                    self.__pygame.time.set_timer(USEREVENT, 1)
                    self.__environment.draw_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                                 self.__environment.rotation)
                    self.draw_board(self.__environment.next_mino, self.__environment.hold_mino,
                                    self.__environment.score,
                                    self.__environment.level, self.__environment.goal)
                # Hold
                elif event.key == K_LSHIFT or event.key == K_c:
                    if not self.__environment.hold:
                        # self.ui_configuration.move_sound.play()
                        if self.__environment.hold_mino == -1:
                            self.__environment.hold_mino = self.__environment.mino
                            self.__environment.mino = self.__environment.next_mino
                            self.__environment.next_mino = randint(1, 7)
                            # self.environment.next_mino = randint(1, 7)
                        else:
                            self.__environment.hold_mino, self.__environment.mino = \
                                self.__environment.mino, self.__environment.hold_mino
                        self.__environment.dx, self.__environment.dy = 3, 0
                        self.__environment.rotation = 0
                        self.__environment.hold = True
                    self.__environment.draw_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                                 self.__environment.rotation)
                    self.draw_board(self.__environment.next_mino, self.__environment.hold_mino,
                                    self.__environment.score,
                                    self.__environment.level, self.__environment.goal)
                # Turn right
                elif event.key == K_UP or event.key == K_x:

                    if self.__environment.is_turnable_r(self.__environment.dx, self.__environment.dy,
                                                        self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.rotation += 1
                    # Kick
                    elif self.__environment.is_turnable_r(self.__environment.dx, self.__environment.dy - 1,
                                                          self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dy -= 1
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_r(self.__environment.dx + 1,
                                                          self.__environment.dy, self.__environment.mino,
                                                          self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dx += 1
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_r(self.__environment.dx - 1, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dx -= 1
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_r(self.__environment.dx, self.__environment.dy - 2,
                                                          self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dy -= 2
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_r(self.__environment.dx + 2, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dx += 2
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_r(self.__environment.dx - 2, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dx -= 2
                        self.__environment.rotation += 1
                    if self.__environment.rotation == 4:
                        self.__environment.rotation = 0
                    self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                                 self.__environment.mino, self.__environment.rotation)
                    self.draw_board(self.__environment.next_mino, self.__environment.hold_mino,
                                    self.__environment.score, self.__environment.level, self.__environment.goal)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if self.__environment.is_turnable_l(self.__environment.dx, self.__environment.dy,
                                                        self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.rotation -= 1
                    # Kick
                    elif self.__environment.is_turnable_l(self.__environment.dx, self.__environment.dy - 1,
                                                          self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dy -= 1
                        self.__environment.rotation -= 1
                    elif self.__environment.is_turnable_l(self.__environment.dx + 1, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dx += 1
                        self.__environment.rotation -= 1
                    elif self.__environment.is_turnable_l(self.__environment.dx - 1, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dx -= 1
                        self.__environment.rotation -= 1
                    elif self.__environment.is_turnable_l(self.__environment.dx, self.__environment.dy - 2,
                                                          self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dy -= 2
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_l(self.__environment.dx + 2, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dx += 2
                        self.__environment.rotation += 1
                    elif self.__environment.is_turnable_l(self.__environment.dx - 2, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dx -= 2
                    if self.__environment.rotation == -1:
                        self.__environment.rotation = 3
                    self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                                 self.__environment.mino, self.__environment.rotation)
                    self.draw_board(self.__environment.next_mino, self.__environment.hold_mino,
                                    self.__environment.score,
                                    self.__environment.level, self.__environment.goal)
                # Move left
                elif event.key == K_LEFT:
                    if not self.__environment.is_leftedge(self.__environment.dx, self.__environment.dy,
                                                          self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dx -= 1
                    self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                                 self.__environment.mino, self.__environment.rotation)
                    self.draw_board(self.__environment.next_mino, self.__environment.hold_mino,
                                    self.__environment.score, self.__environment.level, self.__environment.goal)
                # Move right
                elif event.key == K_RIGHT:
                    if not self.__environment.is_rightedge(self.__environment.dx, self.__environment.dy,
                                                           self.__environment.mino, self.__environment.rotation):
                        # self.ui_configuration.move_sound.play()
                        self.__environment.dx += 1
                    self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                                 self.__environment.mino, self.__environment.rotation)
                    self.draw_board(self.__environment.next_mino, self.__environment.hold_mino,
                                    self.__environment.score,
                                    self.__environment.level, self.__environment.goal)
        self.__pygame.display.update()

    def on_reset(self):
        self.__environment.next()
        self.__environment.reset(True)

    def on_game_over(self):
        for event in self.__pygame.event.get():
            if event.type == QUIT:
                self.__environment.done = True
            elif event.type == USEREVENT:
                self.__pygame.time.set_timer(USEREVENT, 300)
                over_text_1 = self.ui_configuration.h2_b.render("GAME", 1, self.ui_configuration.white)
                over_text_2 = self.ui_configuration.h2_b.render("OVER", 1, self.ui_configuration.white)
                over_start = self.ui_configuration.h5.render("Press return to continue", 1, self.ui_configuration.white)

                self.draw_board(self.__environment.next_mino, self.__environment.hold_mino, self.__environment.score,
                                self.__environment.level, self.__environment.goal)
                self.ui_configuration.screen.blit(over_text_1, (58, 75))
                self.ui_configuration.screen.blit(over_text_2, (62, 105))

                name_1 = self.ui_configuration.h2_i.render(chr(self.__environment.name[0]), 1,
                                                           self.ui_configuration.white)
                name_2 = self.ui_configuration.h2_i.render(chr(self.__environment.name[1]), 1,
                                                           self.ui_configuration.white)
                name_3 = self.ui_configuration.h2_i.render(chr(self.__environment.name[2]), 1,
                                                           self.ui_configuration.white)

                underbar_1 = self.ui_configuration.h2.render("_", 1, self.ui_configuration.white)
                underbar_2 = self.ui_configuration.h2.render("_", 1, self.ui_configuration.white)
                underbar_3 = self.ui_configuration.h2.render("_", 1, self.ui_configuration.white)

                self.ui_configuration.screen.blit(name_1, (65, 147))
                self.ui_configuration.screen.blit(name_2, (95, 147))
                self.ui_configuration.screen.blit(name_3, (125, 147))

                if self.__environment.blink:
                    self.ui_configuration.screen.blit(over_start, (32, 195))
                    self.__environment.blink = False
                else:
                    if self.__environment.name_location == 0:
                        self.ui_configuration.screen.blit(underbar_1, (65, 145))
                    elif self.__environment.name_location == 1:
                        self.ui_configuration.screen.blit(underbar_2, (95, 145))
                    elif self.__environment.name_location == 2:
                        self.ui_configuration.screen.blit(underbar_3, (125, 145))
                    self.__environment.blink = True
                self.__pygame.display.update()

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    # self.ui_configuration.click_sound.play()

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

                    with open('leaderboard.txt') as f:
                        self.ui_configuration.lines = f.readlines()
                    self.ui_configuration.lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

                    self.ui_configuration.leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in self.ui_configuration.lines:
                        self.ui_configuration.leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    self.ui_configuration.leaders = sorted(self.ui_configuration.leaders.items(),
                                                           key=operator.itemgetter(1), reverse=True)

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
                    # self.ui_configuration.click_sound.play()
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

    def draw_block(self, x, y, color):
        self.__pygame.draw.rect(
            self.ui_configuration.screen,
            color,
            Rect(x, y, self.ui_configuration.block_size, self.ui_configuration.block_size)
        )
        self.__pygame.draw.rect(
            self.ui_configuration.screen,
            self.ui_configuration.grey_1,
            Rect(x, y, self.ui_configuration.block_size, self.ui_configuration.block_size),
            1
        )

    def score_history(self):
        with open('leaderboard.txt') as f:
            self.ui_configuration.lines = f.readlines()
        self.ui_configuration.lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

        self.ui_configuration.leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
        for i in self.ui_configuration.lines:
            self.ui_configuration.leaders[i.split(' ')[0]] = int(i.split(' ')[1])
        self.ui_configuration.leaders = sorted(self.ui_configuration.leaders.items(), key=operator.itemgetter(1),
                                               reverse=True)

    # Draw game screen
    def draw_board(self, next, hold, score, level, goal):
        self.ui_configuration.screen.fill(self.ui_configuration.grey_1)

        # Draw sidebar
        self.__pygame.draw.rect(
            self.ui_configuration.screen,
            self.ui_configuration.white,
            Rect(204, 0, 96, 374)
        )

        # Draw next mino
        grid_n = TetriMino.mino_map[next - 1][0]['GRID']

        for i in range(4):
            for j in range(4):
                dx = 220 + self.ui_configuration.block_size * j
                dy = 140 + self.ui_configuration.block_size * i
                if grid_n[i][j] != 0:
                    self.__pygame.draw.rect(
                        self.ui_configuration.screen,
                        self.ui_configuration.t_color[grid_n[i][j]],
                        Rect(dx, dy, self.ui_configuration.block_size, self.ui_configuration.block_size)
                    )

        # Draw hold mino
        # grid_h = TetriMino.mino_map[hold - 1][0]['GRID']
        #
        # if self.__environment.hold_mino != -1:
        #     for i in range(4):
        #         for j in range(4):
        #             self.__environment.dx = 220 + self.ui_configuration.block_size * j
        #             self.__environment.dy = 50 + self.ui_configuration.block_size * i
        #             if grid_h[i][j] != 0:
        #                 self.__pygame.draw.rect(
        #                     self.ui_configuration.screen,
        #                     self.ui_configuration.t_color[grid_h[i][j]],
        #                     Rect(self.__environment.dx, self.__environment.dy, self.ui_configuration.block_size,
        #                          self.ui_configuration.block_size)
        #                 )

        # Set max score
        if self.__environment.score > 999999:
            self.__environment.score = 999999

        # Draw texts
        text_hold = self.ui_configuration.h5.render("HOLD", 1, self.ui_configuration.black)
        text_next = self.ui_configuration.h5.render("NEXT", 1, self.ui_configuration.black)
        text_score = self.ui_configuration.h5.render("SCORE", 1, self.ui_configuration.black)
        score_value = self.ui_configuration.h4.render(str(score), 1, self.ui_configuration.black)
        text_level = self.ui_configuration.h5.render("LEVEL", 1, self.ui_configuration.black)
        level_value = self.ui_configuration.h4.render(str(level), 1, self.ui_configuration.black)
        text_goal = self.ui_configuration.h5.render("GOAL", 1, self.ui_configuration.black)
        goal_value = self.ui_configuration.h4.render(str(goal), 1, self.ui_configuration.black)

        # Place texts
        self.ui_configuration.screen.blit(text_hold, (215, 14))
        self.ui_configuration.screen.blit(text_next, (215, 104))
        self.ui_configuration.screen.blit(text_score, (215, 194))
        self.ui_configuration.screen.blit(score_value, (220, 210))
        self.ui_configuration.screen.blit(text_level, (215, 254))
        self.ui_configuration.screen.blit(level_value, (220, 270))
        self.ui_configuration.screen.blit(text_goal, (215, 314))
        self.ui_configuration.screen.blit(goal_value, (220, 330))

        # Draw board
        for x in range(self.__environment.width):
            for y in range(self.__environment.height):
                dx = 17 + self.ui_configuration.block_size * x
                dy = 17 + self.ui_configuration.block_size * y
                self.draw_block(dx, dy, self.ui_configuration.t_color[self.__environment.matrix[x][y + 1]])
