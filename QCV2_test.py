from QuantumCompilerV2.waveform import Shape,Bus
from QuantumCompilerV2.symbol import Gate
import numpy as np
from numpy import NaN
import sys
sys.path.append(r'C:\Users\edwin\Desktop\Python\Lab005\Script')

class Gate_1q:
    def __init__(self,):
        self.statedict = np.array([
            [0,0,NaN], [1,NaN,1],
            [2,2,NaN], [3,NaN,3],
            [NaN,1,2], [NaN,3,0]
            ])
        self.gatelist = ['X','Y','Z','-X','-Y','-Z','X2','Y2','Z2','-X2','-Y2','-Z2']

    def operator(self,idx,state):
        half = idx//6 #half pi or not, 1 = pi_half; 0 = pi
        pos = ~idx%6//3 #positive or not, 1 = pos; 0 = neg
        axis = idx%3
        state[axis] = (state[axis]+pos*(2-half))%4
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
        idx = 0 if R_state == 0 else axis + (R_state%2)*6 + (R_state%3 == 0)*3

        return idx

G = Gate_1q()

gauss_sig = 1e-9*100
num_sig = 3
I_pi_flat = 35.7e-9


pulse = ~Shape('gaussian_square',
    {'first_peak_x': num_sig*gauss_sig, 'flat': I_pi_flat, 'sigma': gauss_sig},
    2*num_sig*gauss_sig+I_pi_flat, name = 'test pulse')



perform_gate_list = ['X','Y','-X','-Y','X2','Y2','-X2','-Y2']

gate_seq = [None]*len(perform_gate_list)
flat_list = np.array([35.7,34.3,12.4,12])*1e-9 #I_pi, Q_pi, I_pi/2, Q_pi/2

for idx, gate in enumerate(perform_gate_list):
    gate_seq[idx] = Gate(name = gate)
    
    channel_name = 'Q' if idx%2 else 'I'
    pos = ~idx%4//2
    half = idx//4

    gate_pulse = ~Shape('gaussian_square',
    {'first_peak_x': num_sig*gauss_sig, 'flat': flat_list[idx%2 + 2*half], 'sigma': gauss_sig},
    2*num_sig*gauss_sig+I_pi_flat, name = 'I_pi'
    )

    gate_seq[idx][channel_name] = Bus([gate_pulse])
