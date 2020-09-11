from pathlib import Path


def get_name(wit_folder):
    activated_file = Path(wit_folder, '.wit', 'activated.txt')
    with open(activated_file, 'r') as file:
        active_name = file.read()
    return active_name


def write_name(wit_folder, name):
    activated_file = Path(wit_folder, '.wit', 'activated.txt')
    with open(activated_file, 'w') as file:
        file.write(name)
    return True


def get_active_id(wit_folder, name):
    ref_file = Path(wit_folder, '.wit', 'references.txt')
    with open(ref_file, 'r') as file:
        file_date = file.readlines()
        for line in file_date:
            if line.startswith(f'{name}='):
                name_id = line.split('=')[1].strip()
                index = file_date.index(line)
                return name_id, index
    return None, None


def get_ref_file(wit_folder):
    ref_file = Path.joinpath(wit_folder, '.wit', 'references.txt')
    if ref_file.exists():
        with open(ref_file, 'r') as txt_file:
            ref_file_data = txt_file.read().split('\n')
            return ref_file_data
    return None
