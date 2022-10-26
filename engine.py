from __future__ import annotations

import operator
from abc import ABC, abstractmethod
from random import randint

from pygame import QUIT, USEREVENT, KEYDOWN, K_ESCAPE, K_DOWN, K_SPACE, K_LSHIFT, K_c, K_UP, K_x, K_z, K_LCTRL, K_LEFT, \
    K_RIGHT, K_RETURN
from pygame.rect import Rect

from ui_configuration import *
from tetri_mino import *
import pygame
from pygame.event import Event


class TetrisEngine:

    def __init__(self, environment) -> None:
        super().__init__()
        self.__framerate = 30  # Bigger -> Slower
        pygame.init()
        pygame.time.set_timer(USEREVENT, self.__framerate * 10)
        self.__pygame = pygame
        self.__clock = pygame.time.Clock()
        self.environment = environment
        self.ui_configuration = UIConfiguration(self.__pygame)

    def quit(self):
        self.__pygame.quit()

    def on_start(self):

        for event in self.__pygame.event.get():
            if event.type == QUIT:
                self.environment.done = True
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.ui_configuration.click_sound.play()
                    self.environment.start = True

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

        leader_1 = self.ui_configuration.h5_i.render('1st ' +  self.ui_configuration.leaders[0][0] + ' ' + str( self.ui_configuration.leaders[0][1]), 1,
                                                     self.ui_configuration.grey_1)
        leader_2 = self.ui_configuration.h5_i.render('2nd ' +  self.ui_configuration.leaders[1][0] + ' ' + str( self.ui_configuration.leaders[1][1]), 1,
                                                     self.ui_configuration.grey_1)
        leader_3 = self.ui_configuration.h5_i.render('3rd ' +  self.ui_configuration.leaders[2][0] + ' ' + str( self.ui_configuration.leaders[2][1]), 1,
                                                     self.ui_configuration.grey_1)

        if self.environment.blink:
            self.ui_configuration.screen.blit(title_start, (92, 195))
            self.environment.blink = False
        else:
            self.environment.blink = True

        self.ui_configuration.screen.blit(title, (65, 120))
        self.ui_configuration.screen.blit(title_info, (40, 335))

        self.ui_configuration.screen.blit(leader_1, (10, 10))
        self.ui_configuration.screen.blit(leader_2, (10, 23))
        self.ui_configuration.screen.blit(leader_3, (10, 36))

        if not self.environment.start:
            self.__pygame.display.update()
            self.__clock.tick(3)

    def on_pause(self):
        for event in self.__pygame.event.get():
            if event.type == QUIT:
                self.environment.done = True
            elif event.type == USEREVENT:
                self.__pygame.time.set_timer(USEREVENT, 300)
                self.draw_board(self.environment.next_mino, self.environment.hold_mino, self.environment.score,
                                self.environment.level, self.environment.goal)

                pause_text = self.ui_configuration.h2_b.render("PAUSED", 1, self.ui_configuration.white)
                pause_start = self.ui_configuration.h5.render("Press esc to continue", 1, self.ui_configuration.white)

                self.ui_configuration.screen.blit(pause_text, (43, 100))
                if self.environment.blink:
                    self.ui_configuration.screen.blit(pause_start, (40, 160))
                    self.environment.blink = False
                else:
                    self.environment.blink = True
                self.__pygame.display.update()
            elif event.type == KEYDOWN:
                self.environment.erase_mino(self.environment.dx, self.environment.dy, self.environment.mino,
                                            self.environment.rotation)
                if event.key == K_ESCAPE:
                    self.environment.pause = False
                    self.ui_configuration.click_sound.play()
                    self.__pygame.set_timer(USEREVENT, 1)

    def on_game(self):
        for event in self.__pygame.event.get():
            if event.type == QUIT:
                self.environment.done = True
            elif event.type == USEREVENT:
                # Set speed
                if not self.environment.game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        self.__pygame.time.set_timer(USEREVENT, self.__framerate * 1)
                    else:
                        self.__pygame.time.set_timer(USEREVENT, self.__framerate * 10)
                        # pygame.time.set_timer(pygame.KEYDOWN, framerate * 10)
                        # newevent = pygame.event.Event(pygame.locals.KEYDOWN, unicode="a", key=pygame.locals.K_LEFT,
                        #                               mod=pygame.locals.KMOD_NONE)  # create the event
                        # pygame.event.post(newevent)  # a

                # Draw a mino
                self.environment.draw_mino(self.environment.dx, self.environment.dy, self.environment.mino,
                                           self.environment.rotation)
                self.draw_board(self.environment.next_mino, self.environment.hold_mino, self.environment.score,
                                self.environment.level, self.environment.goal)

                # Erase a mino
                if not self.environment.game_over:
                    self.environment.erase_mino(self.environment.dx, self.environment.dy, self.environment.mino,
                                                self.environment.rotation)

                # Move mino down
                if not self.environment.is_bottom(self.environment.dx, self.environment.dy, self.environment.mino,
                                                  self.environment.rotation):
                    self.environment.dy += 1

                # Create new mino
                else:
                    if self.environment.hard_drop or self.environment.bottom_count == 6:
                        self.environment.hard_drop = False
                        self.environment.bottom_count = 0
                        self.environment.score += 10 * self.environment.level
                        self.environment.draw_mino(self.environment.dx, self.environment.dy, self.environment.mino,
                                                   self.environment.rotation)
                        self.draw_board(self.environment.next_mino, self.environment.hold_mino, self.environment.score,
                                        self.environment.level, self.environment.goal)
                        if self.environment.is_stackable(self.environment.next_mino):
                            self.environment.mino = self.environment.next_mino
                            self.environment.next_mino = randint(1, 7)
                            self.environment.dx, self.environment.dy = 3, 0
                            self.environment.rotation = 0
                            self.environment.hold = False
                        else:
                            self.environment.start = False
                            self.environment.game_over = True
                            self.__pygame.time.set_timer(USEREVENT, 1)
                    else:
                        self.environment.bottom_count += 1

                # Erase line
                self.environment.try_erase_line(self.ui_configuration)

                # Increase level
                self.environment.goal -= self.environment.erase_count
                if self.environment.goal < 1 and self.environment.level < 15:
                    self.environment.level += 1
                    self.environment.goal += self.environment.level * 5
                    self.__framerate = int(self.__framerate * 0.8)

            elif event.type == KEYDOWN:
                self.environment.erase_mino(self.environment.dx, self.environment.dy, self.environment.mino,
                                            self.environment.rotation)
                if event.key == K_ESCAPE:
                    self.ui_configuration.click_sound.play()
                    self.environment.pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    self.ui_configuration.drop_sound.play()
                    while not self.environment.is_bottom(self.environment.dx, self.environment.dy,
                                                         self.environment.mino, self.environment.rotation):
                        self.environment.dy += 1
                    self.environment.hard_drop = True
                    self.__pygame.time.set_timer(USEREVENT, 1)
                    self.environment.draw_mino(self.environment.dx, self.environment.dy, self.environment.mino,
                                               self.environment.rotation)
                    self.draw_board(self.environment.next_mino, self.environment.hold_mino, self.environment.score,
                                    self.environment.level, self.environment.goal)
                # Hold
                elif event.key == K_LSHIFT or event.key == K_c:
                    if not self.environment.hold:
                        self.ui_configuration.move_sound.play()
                        if self.environment.hold_mino == -1:
                            self.environment.hold_mino = self.environment.mino
                            self.environment.mino = self.environment.next_mino
                            self.environment.next_mino = randint(1, 7)
                        else:
                            self.environment.hold_mino, self.environment.mino = \
                                self.environment.mino, self.environment.hold_mino
                        self.environment.dx, self.environment.dy = 3, 0
                        self.environment.rotation = 0
                        self.environment.hold = True
                    self.environment.draw_mino(self.environment.dx, self.environment.dy, self.environment.mino,
                                               self.environment.rotation)
                    self.draw_board(self.environment.next_mino, self.environment.hold_mino, self.environment.score,
                                    self.environment.level, self.environment.goal)
                # Turn right
                elif event.key == K_UP or event.key == K_x:

                    if self.environment.is_turnable_r(self.environment.dx, self.environment.dy,
                                                      self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.rotation += 1
                    # Kick
                    elif self.environment.is_turnable_r(self.environment.dx, self.environment.dy - 1,
                                                        self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dy -= 1
                        self.environment.rotation += 1
                    elif self.environment.is_turnable_r(self.environment.dx + 1,
                                                        self.environment.dy, self.environment.mino,
                                                        self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dx += 1
                        self.environment.rotation += 1
                    elif self.environment.is_turnable_r(self.environment.dx - 1, self.environment.dy,
                                                        self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dx -= 1
                        self.environment.rotation += 1
                    elif self.environment.is_turnable_r(self.environment.dx, self.environment.dy - 2,
                                                        self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dy -= 2
                        self.environment.rotation += 1
                    elif self.environment.is_turnable_r(self.environment.dx + 2, self.environment.dy,
                                                        self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dx += 2
                        self.environment.rotation += 1
                    elif self.environment.is_turnable_r(self.environment.dx - 2, self.environment.dy,
                                                        self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dx -= 2
                        self.environment.rotation += 1
                    if self.environment.rotation == 4:
                        self.environment.rotation = 0
                    self.environment.draw_mino(self.environment.dx, self.environment.dy,
                                               self.environment.mino, self.environment.rotation)
                    self.draw_board(self.environment.next_mino, self.environment.hold_mino,
                                    self.environment.score, self.environment.level, self.environment.goal)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if self.environment.is_turnable_l(self.environment.dx, self.environment.dy,
                                                      self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.rotation -= 1
                    # Kick
                    elif self.environment.is_turnable_l(self.environment.dx, self.environment.dy - 1,
                                                        self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dy -= 1
                        self.environment.rotation -= 1
                    elif self.environment.is_turnable_l(self.environment.dx + 1, self.environment.dy,
                                                        self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dx += 1
                        self.environment.rotation -= 1
                    elif self.environment.is_turnable_l(self.environment.dx - 1, self.environment.dy,
                                                        self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dx -= 1
                        self.environment.rotation -= 1
                    elif self.environment.is_turnable_l(self.environment.dx, self.environment.dy - 2,
                                                        self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dy -= 2
                        self.environment.rotation += 1
                    elif self.environment.is_turnable_l(self.environment.dx + 2, self.environment.dy,
                                                        self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dx += 2
                        self.environment.rotation += 1
                    elif self.environment.is_turnable_l(self.environment.dx - 2, self.environment.dy,
                                                        self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dx -= 2
                    if self.environment.rotation == -1:
                        self.environment.rotation = 3
                    self.environment.draw_mino(self.environment.dx, self.environment.dy,
                                               self.environment.mino, self.environment.rotation)
                    self.draw_board(self.environment.next_mino, self.environment.hold_mino, self.environment.score,
                                    self.environment.level, self.environment.goal)
                # Move left
                elif event.key == K_LEFT:
                    if not self.environment.is_leftedge(self.environment.dx, self.environment.dy,
                                                        self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dx -= 1
                    self.environment.draw_mino(self.environment.dx, self.environment.dy,
                                               self.environment.mino, self.environment.rotation)
                    self.draw_board(self.environment.next_mino, self.environment.hold_mino,
                                    self.environment.score, self.environment.level, self.environment.goal)
                # Move right
                elif event.key == K_RIGHT:
                    if not self.environment.is_rightedge(self.environment.dx, self.environment.dy,
                                                         self.environment.mino, self.environment.rotation):
                        self.ui_configuration.move_sound.play()
                        self.environment.dx += 1
                    self.environment.draw_mino(self.environment.dx, self.environment.dy,
                                               self.environment.mino, self.environment.rotation)
                    self.draw_board(self.environment.next_mino, self.environment.hold_mino, self.environment.score,
                                    self.environment.level, self.environment.goal)
        self.__pygame.display.update()

    def on_game_over(self):
        for event in self.__pygame.event.get():
            if event.type == QUIT:
                self.environment.done = True
            elif event.type == USEREVENT:
                self.__pygame.time.set_timer(USEREVENT, 300)
                over_text_1 = self.ui_configuration.h2_b.render("GAME", 1, self.ui_configuration.white)
                over_text_2 = self.ui_configuration.h2_b.render("OVER", 1, self.ui_configuration.white)
                over_start = self.ui_configuration.h5.render("Press return to continue", 1, self.ui_configuration.white)

                self.draw_board(self.environment.next_mino, self.environment.hold_mino, self.environment.score,
                                self.environment.level, self.environment.goal)
                self.ui_configuration.screen.blit(over_text_1, (58, 75))
                self.ui_configuration.screen.blit(over_text_2, (62, 105))

                name_1 = self.ui_configuration.h2_i.render(chr(self.environment.name[0]), 1,
                                                           self.ui_configuration.white)
                name_2 = self.ui_configuration.h2_i.render(chr(self.environment.name[1]), 1,
                                                           self.ui_configuration.white)
                name_3 = self.ui_configuration.h2_i.render(chr(self.environment.name[2]), 1,
                                                           self.ui_configuration.white)

                underbar_1 = self.ui_configuration.h2.render("_", 1, self.ui_configuration.white)
                underbar_2 = self.ui_configuration.h2.render("_", 1, self.ui_configuration.white)
                underbar_3 = self.ui_configuration.h2.render("_", 1, self.ui_configuration.white)

                self.ui_configuration.screen.blit(name_1, (65, 147))
                self.ui_configuration.screen.blit(name_2, (95, 147))
                self.ui_configuration.screen.blit(name_3, (125, 147))

                if self.environment.blink:
                    self.ui_configuration.screen.blit(over_start, (32, 195))
                    self.environment.blink = False
                else:
                    if self.environment.name_location == 0:
                        self.ui_configuration.screen.blit(underbar_1, (65, 145))
                    elif self.environment.name_location == 1:
                        self.ui_configuration.screen.blit(underbar_2, (95, 145))
                    elif self.environment.name_location == 2:
                        self.ui_configuration.screen.blit(underbar_3, (125, 145))
                    self.environment.blink = True
                self.__pygame.display.update()

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.ui_configuration.click_sound.play()

                    outfile = open('leaderboard.txt', 'a')
                    outfile.write(chr(self.environment.name[0]) + chr(self.environment.name[1]) + chr(
                        self.environment.name[2]) + ' ' + str(self.environment.score) + '\n')
                    outfile.close()

                    self.environment.game_over = False
                    self.environment.hold = False
                    self.environment.dx, self.environment.dy = 3, 0
                    self.environment.rotation = 0
                    self.environment.mino = randint(1, 7)
                    self.environment.next_mino = randint(1, 7)
                    self.environment.hold_mino = -1
                    self.environment.framerate = 30
                    self.environment.score = 0
                    self.environment.level = 1
                    self.environment.goal = self.environment.level * 5
                    self.environment.bottom_count = 0
                    self.environment.hard_drop = False
                    self.environment.name_location = 0
                    self.environment.name = [65, 65, 65]
                    self.environment.matrix = [[0 for y in range(self.environment.height + 1)] for x in
                                               range(self.environment.width)]

                    with open('leaderboard.txt') as f:
                        lines = f.readlines()
                    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

                    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in lines:
                        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

                    self.__pygame.time.set_timer(USEREVENT, 1)
                elif event.key == K_RIGHT:
                    if self.environment.name_location != 2:
                        self.environment.name_location += 1
                    else:
                        self.environment.name_location = 0
                    self.__pygame.time.set_timer(USEREVENT, 1)
                elif event.key == K_LEFT:
                    if self.environment.name_location != 0:
                        self.environment.name_location -= 1
                    else:
                        self.environment.name_location = 2
                    self.__pygame.time.set_timer(USEREVENT, 1)
                elif event.key == K_UP:
                    self.ui_configuration.click_sound.play()
                    if self.environment.name[self.environment.name_location] != 90:
                        self.environment.name[self.environment.name_location] += 1
                    else:
                        self.environment.name[self.environment.name_location] = 65
                    self.__pygame.time.set_timer(USEREVENT, 1)
                elif event.key == K_DOWN:
                    self.ui_configuration.click_sound.play()
                    if self.environment.name[self.environment.name_location] != 65:
                        self.environment.name[self.environment.name_location] -= 1
                    else:
                        self.environment.name[self.environment.name_location] = 90
                    self.__pygame.time.set_timer(USEREVENT, 1)

    def get_constants(self):
        return self.__pygame.constants

    def draw_block(self, x, y, color):
        pygame.draw.rect(
            self.ui_configuration.screen,
            color,
            pygame.Rect(x, y, self.ui_configuration.block_size, self.ui_configuration.block_size)
        )
        pygame.draw.rect(
            self.ui_configuration.screen,
            self.ui_configuration.grey_1,
            pygame.Rect(x, y, self.ui_configuration.block_size, self.ui_configuration.block_size),
            1
        )

    def score_history(self):
        with open('leaderboard.txt') as f:
            self.ui_configuration.lines = f.readlines()
        self.ui_configuration.lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

        self.ui_configuration.leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
        for i in self.ui_configuration.lines:
            self.ui_configuration.leaders[i.split(' ')[0]] = int(i.split(' ')[1])
        self.ui_configuration.leaders = sorted(self.ui_configuration.leaders.items(), key=operator.itemgetter(1), reverse=True)

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
        grid_n = TetriMino.mino_map[next - 1][0]

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
        grid_h = TetriMino.mino_map[hold - 1][0]

        if self.environment.hold_mino != -1:
            for i in range(4):
                for j in range(4):
                    self.environment.dx = 220 + self.ui_configuration.block_size * j
                    self.environment.dy = 50 + self.ui_configuration.block_size * i
                    if grid_h[i][j] != 0:
                        self.__pygame.draw.rect(
                            self.ui_configuration.screen,
                            self.ui_configuration.t_color[grid_h[i][j]],
                            Rect(self.environment.dx, self.environment.dy, self.ui_configuration.block_size, self.ui_configuration.block_size)
                        )

        # Set max score
        if score > 999999:
            score = 999999

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
        for x in range(self.environment.width):
            for y in range(self.environment.height):
                dx = 17 + self.ui_configuration.block_size * x
                dy = 17 + self.ui_configuration.block_size * y
                self.draw_block(dx, dy, self.ui_configuration.t_color[self.environment.matrix[x][y + 1]])
