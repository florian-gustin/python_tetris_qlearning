import pygame
from pygame import USEREVENT, QUIT, K_DOWN
from pygame.rect import Rect

from constants.tetri_mino import TetriMino
from constants.ui_configuration import UIConfiguration
from engines.game_mode.engine import Engine


class GUIAgentEngine(Engine):

    def __init__(self, environment, agent, game) -> None:
        super().__init__(environment, agent, game)
        self.framerate = 2  # Bigger -> Slower
        pygame.init()
        pygame.time.set_timer(USEREVENT, self.framerate * 10)
        self.pygame = pygame
        self.clock = pygame.time.Clock()
        self.ui_configuration = UIConfiguration(self.pygame)

    def execute(self):
        super().execute()
        for event in self.pygame.event.get():

            # MAIN LOGIC
            if event.type == USEREVENT:
                # is started
                if not self.environment.game_over:
                    self.start()
                    # print("DEMARRAGE")
                # update or create the piece if False
                if self.is_updating_state_mino() is False:
                    # check if bottom is reach
                    if self.is_bottom_reached() is True:
                        print("BAS DU TERRAIN ATTEINT")
                        # insert the reward only if bottom is reached
                        self.insert_reward()
                        # then create a mino if possible
                        # if not created it means the grid is full
                        if self.create_mino() is False:
                            self.set_game_over()
                # preparing the piece
                elif self.environment.dy < 2 and self.environment.dx == 3 and self.environment.rotation == 0:
                    # get boundaries
                    # init the key values formula in qtable if not existing
                    self.preparing_piece_in_qtable()
                    # find all the events to move the piece
                    # find the current rotation desired
                    # find the current x desired
                    self.events, self.current_rotation, self.current_x = self.get_best_action()
                    print("RECUPERATION DE LA DESTINATION : events = ", self.events, ", rotation = ",
                          self.current_rotation, ", x = ", self.current_x)
                    # placing mino, publishing events to move the piece
                    self.placing_mino()

            # is game quitted
            if event.type == QUIT:
                self.is_quitted()

        # update display
        self.update_display()

    def preparing_piece_in_qtable(self):
        super().preparing_piece_in_qtable()
        print("PREVIOUS BOUNDARIES SETTED : ", self.environment.previous_boundaries)
        print("INSERTION DU BOUNDARIES DANS LA QTABLE : ", self.environment.previous_boundaries)

    def is_quitted(self):
        self.environment.done = True
        self.agent.save("agent.dat")

    def update_display(self):
        super().update_display()
        self.draw_board(self.environment.next_mino, self.environment.hold_mino,
                        self.environment.score, self.environment.level, self.environment.goal)
        self.pygame.display.update()

    def set_game_over(self):
        super().set_game_over()
        self.pygame.time.set_timer(USEREVENT, 1)

    def start(self):
        super().start()
        self.set_speed()

    def set_speed(self):
        super().set_speed()
        keys_pressed = self.pygame.key.get_pressed()
        if keys_pressed[K_DOWN]:
            self.pygame.time.set_timer(USEREVENT, self.framerate * 1)
        else:
            self.pygame.time.set_timer(USEREVENT, self.framerate * 10)

    def on_reset(self):
        super().on_reset()
        self.framerate = 2  # Bigger -> Slower
        pygame.time.set_timer(USEREVENT, self.framerate * 1)

    def draw_block(self, x, y, color):
        self.pygame.draw.rect(
            self.ui_configuration.screen,
            color,
            Rect(x, y, self.ui_configuration.block_size, self.ui_configuration.block_size)
        )
        self.pygame.draw.rect(
            self.ui_configuration.screen,
            self.ui_configuration.grey_1,
            Rect(x, y, self.ui_configuration.block_size, self.ui_configuration.block_size),
            1
        )

        # Draw game screen

    def draw_board(self, next, hold, score, level, goal):
        self.ui_configuration.screen.fill(self.ui_configuration.grey_1)

        # Draw sidebar
        self.pygame.draw.rect(
            self.ui_configuration.screen,
            self.ui_configuration.white,
            Rect(204, 0, 96, 374)
        )

        # Draw next mino
        grid_n = TetriMino.mino_map[next - 1][0]['GRID']

        for i in range(4):
            for j in range(4):
                dx = 220 + self.ui_configuration.block_size * j
                dy = 65 + self.ui_configuration.block_size * i
                if grid_n[i][j] != 0:
                    self.pygame.draw.rect(
                        self.ui_configuration.screen,
                        self.ui_configuration.t_color[grid_n[i][j]],
                        Rect(dx, dy, self.ui_configuration.block_size, self.ui_configuration.block_size)
                    )

        # Set max score
        if self.environment.score > 999999:
            self.environment.score = 999999

        # Draw texts
        # text_hold = self.ui_configuration.h5.render("HOLD", 1, self.ui_configuration.black)
        text_next = self.ui_configuration.h5.render("NEXT", 1, self.ui_configuration.black)
        text_reward = self.ui_configuration.h5.render("REWARDS", 1, self.ui_configuration.black)
        text_score = self.ui_configuration.h5.render("SCORE", 1, self.ui_configuration.black)
        score_value = self.ui_configuration.h4.render(str(score), 1, self.ui_configuration.black)
        reward_value = self.ui_configuration.h4.render(str(self.agent.reward_count), 1, self.ui_configuration.black)
        # text_level = self.ui_configuration.h5.render("LEVEL", 1, self.ui_configuration.black)
        # level_value = self.ui_configuration.h4.render(str(level), 1, self.ui_configuration.black)
        text_goal = self.ui_configuration.h5.render("GOAL", 1, self.ui_configuration.black)
        goal_value = self.ui_configuration.h4.render(str(goal), 1, self.ui_configuration.black)

        # Place texts
        # self.ui_configuration.screen.blit(text_hold, (215, 14))
        self.ui_configuration.screen.blit(text_next, (215, 14))
        self.ui_configuration.screen.blit(text_reward, (215, 120))
        self.ui_configuration.screen.blit(reward_value, (220, 140))
        self.ui_configuration.screen.blit(text_score, (215, 194))
        self.ui_configuration.screen.blit(score_value, (220, 215))
        # self.ui_configuration.screen.blit(text_level, (215, 254))
        # self.ui_configuration.screen.blit(level_value, (220, 270))
        self.ui_configuration.screen.blit(text_goal, (215, 314))
        self.ui_configuration.screen.blit(goal_value, (220, 330))

        # Draw board
        for x in range(self.environment.width):
            for y in range(self.environment.height):
                dx = 17 + self.ui_configuration.block_size * x
                dy = 17 + self.ui_configuration.block_size * y
                self.draw_block(dx, dy, self.ui_configuration.t_color[self.environment.matrix[x][y + 1]])

    def quit(self):
        self.pygame.quit()
