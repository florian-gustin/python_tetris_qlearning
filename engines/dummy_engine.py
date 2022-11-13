import pygame
from pygame import USEREVENT, QUIT, K_DOWN, KEYDOWN
from pygame.rect import Rect

from config import PYGAME_ACTIONS, AGENT_ACTIONS
from rewards import LINE_CLEAR_REWARD, HOLE_REWARD, BUMPINESS_REWARD, BLOCKADE_REWARD
from tetri_mino import TetriMino
from ui_configuration import UIConfiguration


class DummyEngine:

    def __init__(self, environment, agent, game) -> None:
        super().__init__()
        self.__framerate = 5  # Bigger -> Slower
        pygame.init()
        pygame.time.set_timer(USEREVENT, self.__framerate * 10)
        self.__pygame = pygame
        self.__clock = pygame.time.Clock()
        self.__environment = environment
        self.__game = game
        self.__agent = agent
        self.ui_configuration = UIConfiguration(self.__pygame)
        self.__is_mino_created = self.create_mino()
        self.__is_bottom_reached = True
        self.__events = []
        self.__current_rotation = 0
        self.__current_x = 0
        self.__agent.init_state_in_qtable()

    def execute(self):
        for event in self.__pygame.event.get():

            # MAIN LOGIC
            if event.type == USEREVENT:
                # is started
                if not self.__environment.game_over:
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
                elif self.__environment.dy < 2:
                    # get boundaries
                    # init the key values formula in qtable if not existing
                    self.preparing_piece_in_qtable()
                    # find all the events to move the piece
                    # find the current rotation desired
                    # find the current x desired
                    self.__events, self.__current_rotation, self.__current_x = self.get_best_action()
                    print("RECUPERATION DE LA DESTINATION : events = ", self.__events, ", rotation = ",
                          self.__current_rotation, ", x = ", self.__current_x)
                    # placing mino, publishing events to move the piece
                    self.placing_mino()

            # use events to move the piece
            if event.type == KEYDOWN:
                self.handle_events(event)

            # is game quitted
            if event.type == QUIT:
                self.is_quitted()

        # update display
        self.update_display()

    def preparing_piece_in_qtable(self):
        self.__environment.set_previous_boundaries()
        print("PREVIOUS BOUNDARIES SETTED : ", self.__environment.previous_boundaries)
        self.__agent.upsert_boundary_qtable(self.__environment.mino,
                                            self.__environment.previous_boundaries)
        print("INSERTION DU BOUNDARIES DANS LA QTABLE : ", self.__environment.previous_boundaries)

    def get_best_action(self):
        return self.__agent.best_actions(
            self.__environment.mino, self.__environment.dx, self.__environment.get_boundaries())

    def is_updating_state_mino(self):
        return self.__game.update_state_mino()

    def is_quitted(self):
        self.__environment.done = True
        # self.__agent.save("agent.dat")

    def is_bottom_reached(self):
        tmp = self.__game.is_bottom_reached()
        self.__environment.try_erase_line()
        return tmp

    def update_display(self):
        self.__environment.draw_mino(self.__environment.dx, self.__environment.dy, self.__environment.next_mino,
                                     self.__environment.rotation)
        self.draw_board(self.__environment.next_mino, self.__environment.hold_mino,
                        self.__environment.score, self.__environment.level, self.__environment.goal)
        self.__pygame.display.update()

    def handle_events(self, event):
        self.__environment.erase_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                      self.__environment.rotation)

        self.__game.on_step(AGENT_ACTIONS[event.key])

    def set_game_over(self):
        self.__game.set_game_over()
        self.__pygame.time.set_timer(USEREVENT, 1)

    def start(self):
        self.set_speed()

    def create_mino(self):
        return self.__game.is_mino_created()

    def placing_mino(self):
        for action in self.__events:
            self.__pygame.event.post(PYGAME_ACTIONS[action])
            print("EVENT PUBLISHED : ", PYGAME_ACTIONS[action])

    def insert_reward(self):

        lines_count = self.__environment.erase_count * LINE_CLEAR_REWARD
        holes_count = self.__environment.holes_created_count() * HOLE_REWARD
        bp = self.__environment.is_bumpiness_increased_by(self.__agent.previous_state,
                                                          self.__environment.get_boundaries()) * BUMPINESS_REWARD
        is_blockade_created = self.__environment.is_blockade_created() * BLOCKADE_REWARD

        reward = lines_count + holes_count + bp + is_blockade_created
        self.__agent.insert_reward_in_state_qtable(self.__environment.mino, self.__current_x,
                                                   reward,
                                                   self.__agent.table_to_str(self.__environment.previous_boundaries),
                                                   self.__current_rotation)

    def set_speed(self):
        keys_pressed = self.__pygame.key.get_pressed()
        if keys_pressed[K_DOWN]:
            self.__pygame.time.set_timer(USEREVENT, self.__framerate * 1)
        else:
            self.__pygame.time.set_timer(USEREVENT, self.__framerate * 10)

            #
            # pygame.time.set_timer(pygame.KEYDOWN, self.__framerate * 10)
            # newevent = pygame.event.Event(KEYDOWN, K_LEFT)  # create the event
            # pygame.event.post(newevent)  # a

    def on_reset(self):
        self.__environment.next()
        self.__framerate = 9  # Bigger -> Slower
        pygame.time.set_timer(USEREVENT, self.__framerate * 10)
        self.__current_rotation = 0
        self.__current_x = 3
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
