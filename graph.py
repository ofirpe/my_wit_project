from pathlib import Path

import find
from graphviz import Digraph


def get_next_edge(commit_id, wit_folder):
    file = commit_id + '.txt'
    path = Path(wit_folder, '.wit', 'images', file)
    if not path.is_file():
        return None

    with open(path, 'r') as next_file:
        parent_id = next_file.readlines()[0].split('=')[1].strip()
    return parent_id


def id_list(current_id, wit_folder):
    ids = [current_id]

    parent_exist = True
    while parent_exist:
        next_id = get_next_edge(current_id, wit_folder)
        if not next_id or next_id == "None":
            parent_exist = False
        else:
            ids.append(next_id)
            current_id = next_id

    return ids


def graph():
    current_folder = Path.cwd()
    wit_folder = find.find_wit_folder(current_folder)

    if not wit_folder:
        return False

    with open(Path(wit_folder, '.wit', 'references.txt'), 'r') as txt_file:
        current_id = txt_file.readlines()[1].split('=')[1].strip()

    edges = id_list(current_id, wit_folder)

    wit_graph = Digraph(filename='wit', format='png')
    # wit_graph.attr(size='50, 50')

    for i in range(len(edges) - 1):
        tail = edges[i]
        head = edges[i + 1]
        if ',' in head:
            heads = head.split(',')
            wit_graph.edge(tail, heads[0])
            wit_graph.edge(tail, heads[1])
        else:
            wit_graph.edge(tail, head)
    wit_graph.view()
