import os
import pickle
from typing import Set, Dict


class Helper:
    def get_qtable_files(directory: str):
        return {os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.dat')}

    def merge_qtables(qtable_files: Set[str]):
        qtable = {}
        for filename in qtable_files:
            with open(filename, 'r') as file:
                current_qtable: Dict[bytes, Dict[str, float]] = pickle.load(file)
                for key, value in current_qtable.items():
                    if key not in qtable:
                        qtable[key] = value
                    else:
                        for action, qvalue in value.items():
                            if qvalue == 0:
                                pass
                            if qtable[key][action] == 0:
                                qtable[key][action] = qvalue
                            else:
                                qtable[key][action] = (qtable[key][action] + qvalue) / 2
        return qtable