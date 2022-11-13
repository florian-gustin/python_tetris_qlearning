import pygame
from pygame import USEREVENT, QUIT, K_DOWN, KEYDOWN
from pygame.rect import Rect

from engines.engine import Engine
from rewards import LINE_CLEAR_REWARD, HOLE_REWARD, BLOCKADE_REWARD, BUMPINESS_REWARD
from tetri_mino import TetriMino
from ui_configuration import UIConfiguration


class GUIEngine(Engine):
    def __init__(self, environment, agent, game) -> None:
        super().__init__()
        self.__framerate = 15  # Bigger -> Slower
        pygame.init()
        pygame.time.set_timer(USEREVENT, self.__framerate * 10)
        self.__pygame = pygame
        self.__clock = pygame.time.Clock()
        self.__environment = environment
        self.__agent = agent
        self.ui_configuration = UIConfiguration(self.__pygame)
        self.__game = game
        self.mino_r, self.x = 0, 0

    def execute(self):
        for event in self.__pygame.event.get():
            if event.type == QUIT:
                self.on_event_quit()
            elif event.type == USEREVENT:
                if not self.__environment.game_over:
                    self.on_userevent_start()

                if self.__game.update_state_mino() == "create":
                    self.on_userevent_placing_mino()
                    self.__environment.draw_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                                 self.__agent.last_action)
                else:
                    self.on_userevent_create_mino()
                    self.__environment.draw_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                                 self.__agent.last_action)

            self.draw_board(self.__environment.next_mino, self.__environment.hold_mino,
                            self.__environment.score, self.__environment.level, self.__environment.goal)


            self.__pygame.display.update()




    def on_event_quit(self):
        self.__environment.done = True
        self.__agent.save("agent.dat")

    def on_userevent_start(self):

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_DOWN]:
            self.__pygame.time.set_timer(USEREVENT, self.__framerate * 1)
        else:
            self.__pygame.time.set_timer(USEREVENT, self.__framerate * 10)

            #
            # pygame.time.set_timer(pygame.KEYDOWN, self.__framerate * 10)
            # newevent = pygame.event.Event(KEYDOWN, K_LEFT)  # create the event
                # pygame.event.post(newevent)  # a

    def on_userevent_create_mino(self):
        pass


    def on_userevent_placing_mino(self):
        self.mino_r, self.x = self.__agent.step(self.__environment.mino, self.__environment.dx, 22)

        self.__game.on_step(self.mino_r, self.x)

        self.__environment.dx = self.x


        hard_drop = self.__game.is_bottom_reached(self.mino_r)

        if hard_drop is True:
            # self.__agent.change_state(self.__environment.matrix)

            stackable = self.__game.create_mino_or_game_over()

            if stackable is False:
                self.__pygame.time.set_timer(USEREVENT, 1)
        radar = self.__environment.get_state_boundaries()
        print(radar)
        # self.__agent.change_state(self.__environment.matrix)


        lines_count = self.__environment.erase_count * LINE_CLEAR_REWARD
        holes_count = self.__environment.holes_created_count() * HOLE_REWARD
        bp = self.__environment.is_bumpiness_increased_by(self.__agent.previous_bp,
                                                          self.__environment.get_boundaries()) * BUMPINESS_REWARD
        is_blockade_created = self.__environment.is_blockade_created() * BLOCKADE_REWARD
        reward = lines_count + holes_count + bp + is_blockade_created


        self.__agent.insert_reward_in_state_qtable(self.__environment.mino, self.__environment.dx,
                                                   reward,
                                                   self.__environment.get_state_boundaries(),
                                                   self.mino_r)

    def on_userevent_increase_level(self):
        pass

    def on_reset(self):
        self.__environment.next()
        self.__framerate = 9  # Bigger -> Slower
        pygame.time.set_timer(USEREVENT, self.__framerate * 10)
        self.__environment.reset(True)

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
