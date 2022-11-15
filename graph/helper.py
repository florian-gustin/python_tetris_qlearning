import os
import pickle
import shutil
from typing import Set, Dict
import lzma

class Merge:
    def __init__(self, directory, output):
        self.directory = directory
        self.qtable_files = []
        self.output = output
        self.qtable = {}

    def execute(self):
        self.qtable_files = self.get_qtable_files()
        self.merge_qtables()

    def get_qtable_files(self):
        return {os.path.join(self.directory, filename) for filename in os.listdir(self.directory) if filename.endswith('.dat')}

    def merge_qtables(self):
        qtable = {}
        for filename in self.qtable_files:
            with lzma.open(filename, 'r') as file:
                current_qtable = pickle.load(file)
                for key, value in current_qtable.items():
                    if key not in qtable:
                        qtable[key] = value
                    else:
                        if value == 0:
                            pass
                        if qtable[key] == 0:
                            qtable[key] = value
                        else:
                            qtable[key] = (qtable[key] + value) / len(self.qtable_files)
        self.qtable = qtable

    def save(self):
        with lzma.open(self.output + ".tmp", 'w') as file:
            pickle.dump(self.qtable, file)
        shutil.move(self.output + ".tmp", self.output)

if __name__ == '__main__':
    test = Merge("../records", "../agent.dat")
    test.execute()
    test.save()