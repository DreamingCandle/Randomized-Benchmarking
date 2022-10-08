import numpy as np
import random
from collections import deque

def Virtual_Z(gatelist):
    dict_VZ = {
        'XZ' : '-X',
        'XZ2': 'Y',
        'X-Z': '-X',
        'X-Z2': '-Y',
        '-XZ' : 'X',
        '-XZ2': '-Y',
        '-X-Z': 'X',
        '-X-Z2': 'Y',
        'YZ' : '-Y',
        'YZ2': '-X',
        'Y-Z' : '-Y',
        'Y-Z2' : 'X',
        '-YZ' : 'Y',
        '-YZ2': 'X',
        '-Y-Z' : 'Y',
        '-Y-Z2' : '-X',
        'X2Z' : '-X2',
        'X2Z2': 'Y2',
        'X2-Z': '-X2',
        'X2-Z2': '-Y2',
        '-X2Z' : 'X2',
        '-X2Z2': '-Y2',
        '-X2-Z': 'X2',
        '-X2-Z2': 'Y2',
        'Y2Z' : '-Y2',
        'Y2Z2': '-X2',
        'Y2-Z' : '-Y2',
        'Y2-Z2' : 'X2',
        '-Y2Z' : 'Y2',
        '-Y2Z2': 'X2',
        '-Y2-Z' : 'Y2',
        '-Y2-Z2' : '-X2',
        }

    def f(workspace):
        Z_list = ['Z','-Z','Z2','-Z2']
        first = workspace.popleft()
        second = workspace.popleft()
        if first in Z_list:
                workspace.appendleft(second)
        else:
            if second in Z_list:
                workspace.appendleft(dict_VZ[first+second])
            else:
                workspace.appendleft(second)
                workspace.appendleft(first)
        return workspace

    workspace = deque()
    eff_list = []
    workspace.append(gatelist.popleft())

    while len(gatelist) > 0 :
        while len(workspace) < 3 :
            workspace.append(gatelist.popleft())
        print(workspace)
        workspace = f(workspace)
        print(workspace)
        if len(workspace) == 3:
            eff_list.append(workspace.popleft())
        print(workspace)
    workspace = f(workspace)
    while len(workspace) > 0 :
        eff_list.append(workspace.popleft())
    
    return eff_list
