from config import ACTION_ROTATE, ACTION_LEFT, ACTION_RIGHT
from environment import Environment


class Game:

    def __init__(self, environment: Environment):
        self.__environment = environment

    def on_step(self, action):
        self.__environment.erase_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                      self.__environment.rotation)
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
