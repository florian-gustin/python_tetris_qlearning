from random import randint

from config import ACTION_ROTATE, ACTION_LEFT, ACTION_RIGHT
from environment import Environment
from rewards import HOLE_REWARD, LINE_CLEAR_REWARD


class Game:

    def __init__(self, environment: Environment):
        self.__environment = environment


    def is_stackable(self):
        if self.__environment.is_stackable(self.__environment.next_mino):
            self.__environment.mino = self.__environment.next_mino
            self.__environment.next_mino = randint(1, 7)
            self.__environment.dx, self.__environment.dy = 3, 0
            self.__environment.rotation = 0
            self.__environment.hold = False

            return True
        else:
            self.__environment.start = False
            self.__environment.game_over = True

        return False

    def hard_drop(self):
        if self.__environment.hard_drop or self.__environment.bottom_count == 0:

            self.__environment.set_previous_boundaries()

            self.__environment.hard_drop = False
            self.__environment.bottom_count = 0
            self.__environment.score += 10 * self.__environment.level
            self.__environment.draw_mino(self.__environment.dx, self.__environment.dy,
                                         self.__environment.mino,
                                         self.__environment.rotation)

            self.__environment.try_erase_line()

            return True

        else:
            self.__environment.bottom_count += 1

        # Erase line
        self.__environment.try_erase_line()

        return False

    def update_state_mino(self):
        state = "nothing"
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
            state = "create"
                # is stackable here

        return state
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
            if self.__environment.rotation == 4:
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
