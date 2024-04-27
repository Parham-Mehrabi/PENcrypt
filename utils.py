"""
utils 
"""
import os


def unique_pickle_path(path):
    index = 0
    while os.path.exists(f"{path}-{index}.pickle"):
        index += 1
    return f"{path}-{index}.pickle"