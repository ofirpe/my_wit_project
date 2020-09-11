from pathlib import Path

import find


def branch(name):
    current_folder = Path.cwd()
    wit_folder = find.find_wit_folder(current_folder)

    if not wit_folder:
        return False

    references_file = Path(wit_folder, '.wit', 'references.txt')
    with open(references_file, 'r') as ref_file:
        head = ref_file.readlines()[0].split('=')[1].strip()

    with open(references_file, 'a') as ref_file:
        ref_file.write(f'{name}={head}\n')
