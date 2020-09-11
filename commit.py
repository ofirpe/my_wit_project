from pathlib import Path
from secrets import token_hex
from shutil import copytree
from time import localtime, strftime

import activated
import find


def create_commit_folder(path):
    folder_exist = False
    while not folder_exist:
        commit_folder = token_hex(20)
        commit_path = Path.joinpath(path, '.wit', 'images', commit_folder)
        try:
            Path.mkdir(commit_path, parents=True, exist_ok=False)
            folder_exist = True
        except FileExistsError:
            print('folder named already exist, tyring a different name')
    return commit_path


def create_txt_files(path, commit_folder, msg, merge):
    ref_file = activated.get_ref_file(path)

    metadata_file_name = commit_folder + '.txt'
    metadata_file_path = Path.joinpath(
        path, '.wit', 'images', metadata_file_name
    )

    if ref_file:
        old_head = ref_file[0][5:]
        ref_file[0] = f'HEAD={commit_folder}'

        active_name = activated.get_name(path)
        active_id, index = activated.get_active_id(path, active_name)

        if active_id == old_head:
            ref_file[index] = f'{active_name}={commit_folder}'
        new_ref_file = '\n'.join(ref_file)
    else:
        old_head = 'None'
        new_ref_file = (
            f'HEAD={commit_folder}\n'
            f'master={commit_folder}\n'
        )

    if merge:
        active_branch = activated.get_name(path)
        active_id, _ = activated.get_active_id(path, active_branch)
        if old_head != active_id:
            parents = f'{old_head}, {active_id}'
        else:
            parents = f'{old_head}'
    else:
        parents = f'{old_head}'

    with open(metadata_file_path, 'w') as txt_file:
        txt_file.write(
            f'parent={parents}\n'
            f"date={strftime('%A %b %d %H:%M:%S %Y %z', localtime())}\n"
            f'message={msg}'
        )

    ref_file_path = Path(path, '.wit', 'references.txt')
    with open(ref_file_path, 'w') as txt_file:
        txt_file.writelines(new_ref_file)

    return True


def commit(msg, merge=False):
    path = find.find_wit_folder(Path.cwd())
    if not path:
        print("'.wit' folder not found, can't run commit")
        return False

    staging_folder = Path.joinpath(path, '.wit', 'staging_area')

    commit_path = create_commit_folder(path)
    copytree(staging_folder, commit_path, dirs_exist_ok=True)

    create_txt_files(path, commit_path.name, msg, merge)
