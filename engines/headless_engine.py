import time

from rewards import LINE_CLEAR_REWARD, HOLE_REWARD, BUMPINESS_REWARD, BLOCKADE_REWARD


class HeadlessEngine:
    def __init__(self, environment, agent, game) -> None:
        super().__init__()
        self.environment = environment
        self.agent = agent
        self.game = game

    def run(self):
        if self.environment.game_over is True:
            self.environment.next()
            self.environment.reset(True)

            if time.time() - self.agent.timer > 1:
                print("Actions per sec : ", self.agent.actions)
                self.agent.actions = 0
                self.agent.timer = time.time()
            if self.environment.game_process_counter % 1000 == 0 and self.environment.game_process_counter != 0:
                print("Saving total game = ", self.environment.game_process_counter)
                self.agent.save("self.agent.dat")

        else:

            if self.game.update_state_mino() == "create":
                hard_drop = self.game.hard_drop()

                if hard_drop is True:
                    self.agent.change_state(self.environment.matrix)
                    lines_count = self.environment.erase_count * LINE_CLEAR_REWARD
                    holes_count = self.environment.holes_created_count() * HOLE_REWARD
                    bp = self.environment.is_bumpiness_increased_by(self.agent.previous_bp,
                                                               self.environment.get_boundaries()) * BUMPINESS_REWARD
                    is_blockade_created = self.environment.is_blockade_created() * BLOCKADE_REWARD

                    reward = lines_count + holes_count + bp + is_blockade_created
                    self.agent.insert_reward_in_state_qtable(self.environment.mino, self.environment.dx,
                                                        reward,
                                                        self.environment.get_state_boundaries(), self.environment.rotation)
                    self.game.is_stackable()

                self.environment.goal -= self.environment.erase_count
                if self.environment.goal < 1 and self.environment.level < 15:
                    self.environment.level += 1
                    self.environment.goal += self.environment.level * 5
            else:
                action = self.agent.step(self.environment.mino, self.environment.dx, self.environment.rotation)
                self.game.on_step(action)