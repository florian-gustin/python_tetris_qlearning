import time

from engines.game_mode.engine import Engine


class HeadlessAgentEngine(Engine):

    def __init__(self, environment, agent, game) -> None:
        super().__init__(environment, agent, game)
        self.time = time.time()
        self.save_time = time.time()

    def execute(self):
        super().execute()
        if time.time() - self.time > 1:
            print("Actions per sec : ", self.agent.actions)
            self.agent.actions = 0
            self.time = time.time()
        if time.time() - self.save_time > 600:
            print("Saving total game = ", self.environment.game_process_counter, ", taille qtable = ", len(self.agent.qtables))
            self.environment.game_process_counter = 0
            self.agent.save_qtable("agent.dat")
            self.agent.save_history("history.dat")
            self.agent.reset_history()
            self.save_time = time.time()

        if not self.environment.game_over:
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
        elif self.environment.dy < 2 and self.environment.dx == 3 and self.environment.rotation == 0:
            # get boundaries
            # init the key values formula in qtable if not existing
            self.preparing_piece_in_qtable()
            # find all the events to move the piece
            # find the current rotation desired
            # find the current x desired
            self.events, self.current_rotation, self.current_x = self.get_best_action()
            # placing mino, publishing events to move the piece
            self.placing_mino()

        self.update_display()

    def set_game_over(self):
        super().set_game_over()
        self.on_reset()






