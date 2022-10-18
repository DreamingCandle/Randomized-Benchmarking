from QuantumCompilerV2.waveform import Shape,Bus
from QuantumCompilerV2.symbol import Gate
from typing import Union
import numpy as np
from numpy import NaN
from collections import deque


def Virtual_Z(gatelist : Union[list , deque]):
    dict_VZ = {
        'XZ' : '-X', 'XZ2': 'Y', 'X-Z': '-X', 'X-Z2': '-Y',
        '-XZ' : 'X', '-XZ2': '-Y', '-X-Z': 'X', '-X-Z2': 'Y',
        'YZ' : '-Y', 'YZ2': '-X', 'Y-Z' : '-Y', 'Y-Z2' : 'X',
        '-YZ' : 'Y', '-YZ2': 'X', '-Y-Z' : 'Y', '-Y-Z2' : '-X',
        'X2Z' : '-X2', 'X2Z2': 'Y2', 'X2-Z': '-X2', 'X2-Z2': '-Y2',
        '-X2Z' : 'X2', '-X2Z2': '-Y2', '-X2-Z': 'X2', '-X2-Z2': 'Y2',
        'Y2Z' : '-Y2', 'Y2Z2': '-X2', 'Y2-Z' : '-Y2', 'Y2-Z2' : 'X2',
        '-Y2Z' : 'Y2', '-Y2Z2': 'X2', '-Y2-Z' : 'Y2', '-Y2-Z2' : '-X2',
        }

    def f(workspace:deque):
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

    gatedeque = deque(gatelist)
    workspace = deque()
    eff_list = []
    workspace.append(gatedeque.popleft())
    while gatedeque:
        if len(workspace) == 1:
            workspace.append(gatedeque.popleft())
        workspace = f(workspace)
        if len(workspace) == 2:
            eff_list.append(workspace.popleft())
    if len(workspace) == 2:
        workspace = f(workspace)
    eff_list += list(workspace)
    
    return eff_list


class Gate_1q:
    def __init__(self, flatlist,gauss_sig,num_sig):
        self.statedict = np.array([
            [0,0,NaN], [1,NaN,1],
            [2,2,NaN], [3,NaN,3],
            [NaN,1,2], [NaN,3,0]
            ])
        self.gatelist = ['X','Y','Z','-X','-Y','-Z','X2','Y2','Z2','-X2','-Y2','-Z2','I']
        self.flat_list = flatlist
        self.gauss_sig = gauss_sig
        self.num_sig = num_sig
        self.gatewave()
        

    def operator(self,idx,state):
        half = idx//6 #half pi or not, 1 = pi_half; 0 = pi
        sign = idx%6//3 #positive or not, 0 = pos; 1 = neg
        axis = idx%3
        state[axis] = (state[axis]+(2-half)*((-1)**sign))%4
        if np.isnan(state[axis]):
            state_new = state
        else:
            result = np.where(self.statedict[:,axis] == state[axis])
            state_new = self.statedict[result,:][0,0]
        return state_new

    def reverse(self,state):
        '''
        Input: current state
        Output: (Rotation state, rotation axis)
        '''
        
        temp = np.array([0,0,NaN]) - state
        axis = np.where(~np.isnan(temp) == True)[0][0]
        R_state = int(temp[axis])%4
        idx = 12 if R_state == 0 else axis + (R_state%2)*6 + (R_state%3 == 0)*3

        return idx
    
    def gatewave(self):
        sampling_rate = 1e9
        self.perform_gate_list = ['X','Y','-X','-Y','X2','Y2','-X2','-Y2']
        self.gate_seq = [None]*(len(self.perform_gate_list)+1)

        for idx, gate in enumerate(self.perform_gate_list):

            channel_name = 'Q' if idx%2 else 'I'
            channel_name2 = 'I' if idx%2 else 'Q'
            pos = ~idx%4//2
            half = idx//4

            gate_pulse = ~(Shape('gaussian_square',
            {'first_peak_x': self.num_sig*self.gauss_sig, 'flat': self.flat_list[idx%2 + 2*half], 'sigma': self.gauss_sig},
                2*self.num_sig*self.gauss_sig+self.flat_list[idx%2 + 2*half], sampling_rate, name = channel_name
            )*(-1)**pos)

            empty = ~Shape('const',{'lv' : 0},
                2*self.num_sig*self.gauss_sig+self.flat_list[idx%2 + 2*half], sampling_rate, name = channel_name2)
            
            bus = Bus([empty,gate_pulse],name = gate) if idx%2 else Bus([gate_pulse,empty],name = gate)
            self.gate_seq[idx] = Gate(name = gate)
            self.gate_seq[idx]['Q1'] = bus

        readout_pulse = ~Shape('gaussian_square',
                {'first_peak_x': self.num_sig*self.gauss_sig, 'flat': 6e-6, 'sigma': self.gauss_sig},
                2*self.num_sig*self.gauss_sig+6e-6, sampling_rate, name = 'readout'
                )
        marker_dur = 1e-6
        marker = ~Shape(
            'square', {'start': 0,'flat': marker_dur}, marker_dur, sampling_rate, name = 'marker'
        )

        self.gate_seq[-1] = Gate(name = 'readout')
        self.gate_seq[-1]['readout'] = Bus([readout_pulse,marker])
        self.gate_seq[-1]['Q1'] = Bus.null((2,1e-9))
        


if __name__ == '__main__':
    flat_list = np.array([35.7,34.3,12.4,12])*1e-9 #I_pi, Q_pi, I_pi/2, Q_pi/2
    G = Gate_1q(flat_list)
    random_list = [1,4,3,2,6,0]
    gate = Gate()
    gate['Q1'] = Bus.null((2,1e-9))
    gate['readout'] = Bus.null((2,1e-9))

    # gate.plot()
    for i,id in enumerate(random_list):
        gate += G.gate_seq[id]
    gate += G.gate_seq[-1]

    Q1 = gate.compile_device('Q1')
    Q1.wires = {0: 'I', 1: 'Q'}
    channel_readout = gate.compile_device('readout')
    channel_readout.wires = {0: 'readout', 1: 'marker'}
    
    # Q1.plot()
    # channel_readout.plot()