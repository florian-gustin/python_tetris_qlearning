from random import randint

from constants.config import ACTION_ROTATE, ACTION_LEFT, ACTION_RIGHT
from environment import Environment
from constants.tetri_mino import *

class Game:

    def __init__(self, environment: Environment):
        self.__environment = environment


    def is_mino_created(self):
        if self.__environment.is_stackable(self.__environment.next_mino):
            self.__environment.mino = self.__environment.next_mino
            self.__environment.next_mino = randint(1,4)
            self.__environment.dx, self.__environment.dy = 3, 0
            self.__environment.rotation = 0
            self.__environment.hold = False
            return True
        else:
            self.set_game_over()
            return False

    def set_game_over(self):
        self.__environment.start = False
        self.__environment.game_over = True

    def is_bottom_reached(self):
        if self.__environment.hard_drop or self.__environment.bottom_count == 0:
            self.__environment.hard_drop = False
            self.__environment.bottom_count = 0
            self.__environment.score += 10 * self.__environment.level
            self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                         self.__environment.mino,
                                         self.__environment.rotation)
            return True

        else:
            self.__environment.bottom_count += 1
            return False

    def update_state_mino(self):
        status = False
        # Erase a mino
        if not self.__environment.game_over:
            self.__environment.erase_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                          self.__environment.rotation)

        # Move mino down
        if not self.__environment.is_bottom(self.__environment.dx, self.__environment.dy,
                                            self.__environment.mino,
                                            self.__environment.rotation):
            self.__environment.dy += 1
            status = True

        return status



    def on_step(self, action):
        # Turn right
        if action == ACTION_ROTATE:

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
            if self.__environment.rotation == len(TetriMino.mino_map[self.__environment.mino - 1]):
                self.__environment.rotation = 0
            self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                         self.__environment.mino, self.__environment.rotation)
        # Move left
        elif action == ACTION_LEFT:
            if not self.__environment.is_leftedge(self.__environment.dx, self.__environment.dy,
                                                  self.__environment.mino, self.__environment.rotation):
                # self.ui_configuration.move_sound.play()
                self.__environment.dx -= 1
            self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                         self.__environment.mino, self.__environment.rotation)

        # Move right
        elif action == ACTION_RIGHT:
            if not self.__environment.is_rightedge(self.__environment.dx, self.__environment.dy,
                                                   self.__environment.mino, self.__environment.rotation):
                # self.ui_configuration.move_sound.play()
                self.__environment.dx += 1
            self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                         self.__environment.mino, self.__environment.rotation)

        #print("EVENT CONSUMED : ", action, ", x = ", self.__environment.dx)