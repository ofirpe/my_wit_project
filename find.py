import os


def find_wit_folder(path):
    if path.is_dir() and '.wit' in os.listdir(path):
        return path
    for p in path.parents:
        if '.wit' in os.listdir(p):
            return p
    return None
