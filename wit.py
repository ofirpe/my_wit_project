import sys

from add import add
from branch import branch
from checkout import checkout
from commit import commit
from graph import graph
from init import init
from merge import merge
from status import status


if __name__ == "__main__":
    args = sys.argv[2] if len(sys.argv) > 2 else None
    functions = {
        'init': init,
        'add': add,
        'commit': commit,
        'status': status,
        'checkout': checkout,
        'graph': graph,
        'branch': branch,
        'merge': merge
    }

    call_err = 'Usage: python <filename> <func_name> <param1> <param2> [...]'
    parm_err = 'Error: Invalid function name'

    if len(sys.argv) > 1:
        func = functions.get(sys.argv[1], lambda: print(parm_err))
        if args:
            func(args)
        else:
            func()
    else:
        print(call_err)
