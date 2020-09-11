from pathlib import Path
from shutil import copy2, copytree

import activated
import find
from status import get_data


def checkout(commit_id):
    current_folder = Path.cwd()
    wit_folder = find.find_wit_folder(current_folder)

    if not wit_folder:
        return False

    data = get_data()
    if data['ready_to_commit'] or data['not_updated']:
        print('please run full system backup before runing checkout')
        return False

    active_id, index = activated.get_active_id(wit_folder, commit_id)
    if active_id:
        activated.write_name(wit_folder, commit_id)
    else:
        activated.write_name(wit_folder, "")
    ref_file = activated.get_ref_file(wit_folder)
    old_head = ref_file[0].split('=')[1]

    new_head = active_id if active_id else commit_id

    commit_path = Path.joinpath(wit_folder, '.wit', 'images', new_head)
    copytree(commit_path, wit_folder, copy_function=copy2, dirs_exist_ok=True)
    staging_path = Path(wit_folder, '.wit', 'staging_area')
    copytree(
        commit_path, staging_path, copy_function=copy2, dirs_exist_ok=True
    )

    if old_head == active_id:
        ref_file[index] = f'{commit_id}={new_head}'

    ref_file[0] = f'HEAD={new_head}'
    new_ref_file = '\n'.join(ref_file)
    commit_file_path = Path(wit_folder, '.wit', 'references.txt')
    with open(commit_file_path, 'w') as file:
        file.writelines(new_ref_file)
