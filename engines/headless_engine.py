import time

from rewards import LINE_CLEAR_REWARD, HOLE_REWARD, BUMPINESS_REWARD, BLOCKADE_REWARD
from config import AGENT_ACTIONS, PYGAME_ACTIONS


class HeadlessEngine:

    def __init__(self, environment, agent, game) -> None:
        super().__init__()
        self.__environment = environment
        self.__game = game
        self.__agent = agent
        self.__is_mino_created = self.create_mino()
        self.__is_bottom_reached = True
        self.__events = []
        self.__current_rotation = 0
        self.__current_x = 0
        self.__agent.init_state_in_qtable()
        self.__action = []
        self.time = time.time()
        self.save_time = time.time()

    def execute(self):

        if time.time() - self.time > 1:
            print("Actions per sec : ", self.__agent.actions)
            self.__agent.actions = 0
            self.time = time.time()
        if time.time() - self.save_time > 60:
            self.save_time = time.time()
            print("Saving total game = ", self.__environment.game_process_counter)
            self.__agent.save("agent.dat")

        if not self.__environment.game_over:
            self.start()
            # print("DEMARRAGE")
        # update or create the piece if False
        if self.is_updating_state_mino() is False:
            # check if bottom is reach
            if self.is_bottom_reached() is True:
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
            # placing mino, publishing events to move the piece
            self.placing_mino()

            self.handle_events()
        self.update_display()

    def preparing_piece_in_qtable(self):
        self.__environment.set_previous_boundaries()
        self.__agent.upsert_boundary_qtable(self.__environment.mino,
                                            self.__environment.previous_boundaries)

    def get_best_action(self):
        return self.__agent.best_actions(
            self.__environment.mino, self.__environment.dx, self.__environment.get_boundaries())

    def is_updating_state_mino(self):
        return self.__game.update_state_mino()

    def update_display(self):
        self.__environment.draw_mino(self.__environment.dx, self.__environment.dy, self.__environment.next_mino,
                                     self.__environment.rotation)

    def is_bottom_reached(self):
        tmp = self.__game.is_bottom_reached()
        self.__environment.try_erase_line()
        return tmp

    def handle_events(self,):
        self.__environment.erase_mino(self.__environment.dx, self.__environment.dy, self.__environment.mino,
                                      self.__environment.rotation)

        self.__game.on_step(self.__action)

    def set_game_over(self):
        self.__game.set_game_over()
        self.on_reset()

    def start(self):
        pass

    def create_mino(self):
        return self.__game.is_mino_created()

    def placing_mino(self):
        for action in self.__events:
            self.__action = action
            self.__game.on_step(PYGAME_ACTIONS[action])

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
        pass

    def on_reset(self):
        self.__environment.next()
        self.__current_rotation = 0
        self.__current_x = 3
        self.__environment.reset(True)