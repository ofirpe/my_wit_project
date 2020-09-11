from pathlib import Path
from shutil import copy2

import activated
import commit
import find
import graph
import status


def find_common_id(branch_id_list, head_id_list):
    for b in branch_id_list:
        for h in head_id_list:
            if b == h:
                return b


def merge(branch_name):
    current_folder = Path.cwd()
    wit_folder = find.find_wit_folder(current_folder)

    if not wit_folder:
        return False

    branch_id, index = activated.get_active_id(wit_folder, branch_name)
    branch_id_list = graph.id_list(branch_id, wit_folder)

    head_id = activated.get_ref_file(wit_folder)[0].split('=')[1].strip()
    head_id_list = graph.id_list(head_id, wit_folder)

    common_id = find_common_id(branch_id_list, head_id_list)

    base_files_path = Path(wit_folder, '.wit', 'images', common_id)
    # base_files = [f for f in base_files_path.rglob('*') if f.is_file()]
    branch_files_path = Path(wit_folder, '.wit', 'images', branch_id)
    branch_files = [f for f in branch_files_path.rglob('*') if f.is_file()]

    new_files = []
    status.compare_files(
        branch_files, "", branch_files_path, base_files_path,
        new_files, new_files
    )

    for file in new_files:
        src = file.relative_to(branch_files_path)
        dst = Path(wit_folder, '.wit', 'staging_area', src)
        copy2(src, dst)

    commit.commit('merge', merge=True)
