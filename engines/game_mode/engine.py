import time

from constants.rewards import LINE_CLEAR_REWARD, HOLE_REWARD, BLOCKADE_REWARD, BUMPINESS_REWARD


class Engine:
    def __init__(self, environment, agent, game) -> None:
        super().__init__()
        self.environment = environment
        self.game = game
        self.agent = agent
        self.is_mino_created = self.create_mino()
        self.events = []
        self.current_rotation = 0
        self.current_x = 0
        self.agent.init_state_in_qtable()

    def execute(self):
        pass

    def preparing_piece_in_qtable(self):
        self.environment.set_previous_boundaries()
        self.agent.upsert_boundary_qtable(self.environment.mino,
                                          self.environment.previous_boundaries)

    def get_best_action(self):
        return self.agent.best_actions(
            self.environment.mino, self.environment.dx,
            self.environment.scale_boundaries(self.environment.get_boundaries()))

    def is_updating_state_mino(self):
        return self.game.update_state_mino()

    def update_display(self):
        self.environment.draw_mino(self.environment.dx, self.environment.dy, self.environment.mino,
                                   self.environment.rotation)

    def is_bottom_reached(self):
        tmp = self.game.is_bottom_reached()
        self.environment.try_erase_line()
        return tmp

    def set_game_over(self):
        self.game.set_game_over()

    def start(self):
        pass

    def create_mino(self):
        return self.game.is_mino_created()

    def placing_mino(self):
        for action in self.events:
            self.environment.erase_mino(self.environment.dx, self.environment.dy, self.environment.mino,
                                        self.environment.rotation)
            self.game.on_step(action)

    def insert_reward(self):
        lines_count = self.environment.erase_count * LINE_CLEAR_REWARD
        holes_count = self.environment.holes_created_count() * HOLE_REWARD
        bp = self.environment.is_bumpiness_increased_by(self.agent.previous_state,
                                                        self.environment.get_boundaries()) * BUMPINESS_REWARD
        is_blockade_created = self.environment.is_blockade_created() * BLOCKADE_REWARD

        reward = lines_count + holes_count + bp + is_blockade_created
        self.agent.insert_reward_in_state_qtable(self.environment.mino, self.current_x,
                                                 reward,
                                                 self.agent.table_to_str(self.environment.previous_boundaries),
                                                 self.current_rotation)

    def set_speed(self):
        pass

    def on_reset(self):
        self.environment.next()
        self.current_rotation = 0
        self.current_x = 3
        self.environment.reset(True)
