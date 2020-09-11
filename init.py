from pathlib import Path

import activated


def init():
    folders = [Path('.wit', 'images'), Path('.wit', 'staging_area')]
    for folder in folders:
        target = Path.joinpath(Path.cwd(), folder)
        try:
            Path.mkdir(target, parents=True, exist_ok=False)
        except FileExistsError:
            print(f"[Error]: '{folder}' already exits")

    activated.write_name(Path.cwd(), 'master')
