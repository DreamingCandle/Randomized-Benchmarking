import numpy as np
import QuantumCompilerV2 as QC2
from numpy import NaN


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
        


if __name__ == '__main__':
    list = [1,7,9,2]
    ground = np.array([0,0,NaN])
    result_list = []

    G = Gate_1q()
    state = ground
    for i in list:
        state = G.operator(i,state)
        result_list.append(G.gatelist[i])

    print(G.reverse(ground))


