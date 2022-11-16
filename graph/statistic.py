from matplotlib import pyplot as plt


class Statistic:
    def apply(self, history):
        plt.plot(history)
        plt.show()
