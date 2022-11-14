from matplotlib import pyplot as plt


class Statistic:
    def apply(self, agent):
        plt.plot(agent.history)
        plt.show()
