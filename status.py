import filecmp
from pathlib import Path

import find


def list_of_files(src, ignore=None):
    files = [
        f for f in src.rglob('*')
        if f.is_file() and ignore not in f.parents
    ]
    return files


def compare_files(files, base, relative_to, dst_path, new, different):
    for file in files:
        src = file.relative_to(relative_to)
        dst = Path(base, dst_path, src)
        if not dst.is_file():
            new.extend([file])
        else:
            if not filecmp.cmp(file, dst):
                different.extend([file])
    return new, different


def get_data():
    current_folder = Path.cwd()
    wit_folder = find.find_wit_folder(current_folder)

    if not wit_folder:
        return False

    ready_to_commit = []
    not_updated = []
    new = []

    files = list_of_files(wit_folder, ignore=Path(wit_folder, '.wit'))
    staging_path = Path('.wit', 'staging_area')
    compare_files(
        files, wit_folder, wit_folder, staging_path, new, not_updated
    )

    with open(Path(wit_folder, '.wit', 'references.txt'), 'r') as txt_file:
        head = txt_file.read().split('\n')[0][5:]

    src_path = Path(wit_folder, staging_path)
    files = list_of_files(src_path)

    img_path = Path('.wit', 'images', head)
    compare_files(
        files, wit_folder, src_path, img_path,
        ready_to_commit, ready_to_commit
    )

    data = {
        'head': head,
        'ready_to_commit': ready_to_commit,
        'not_updated': not_updated,
        'new': new
    }

    return data


def status():
    data = get_data()
    if not data:
        return False

    print(
        f'commit id: {data["head"]}'
        '\nChanges to be committed:\n',
        '\n'.join(map(str, data['ready_to_commit'])),
        '\nChanges not staged for commit:\n',
        '\n'.join(map(str, data['not_updated'])),
        '\nuntracked_files:\n',
        '\n'.join(map(str, data['new']))
    )

    return True
