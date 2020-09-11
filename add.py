from pathlib import Path
from shutil import copy2, copytree

import find


def add(user_path):
    src_path = Path.joinpath(Path.cwd(), Path(user_path))
    wit_folder_path = find.find_wit_folder(src_path)

    if not wit_folder_path:
        print(
            "Error: can only run 'add' function "
            "from sub-directory of '.wit' folder"
        )
        return False

    if src_path.is_dir():
        relative_path = src_path.relative_to(wit_folder_path)
    else:
        relative_path = src_path.parent.relative_to(wit_folder_path)

    staging_folder = Path.joinpath(
        wit_folder_path, '.wit', 'staging_area', relative_path
    )
    Path.mkdir(staging_folder, parents=True, exist_ok=True)

    try:
        if src_path.is_dir():
            copytree(src_path, staging_folder, dirs_exist_ok=True)
        else:
            copy2(src_path, staging_folder)
    except FileNotFoundError as err:
        print(err)
