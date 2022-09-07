import numpy as np
import random
'''
take advantage of binary, mapping matrix operation to binary addition
'''
pauli_list = ['I','X','Z','Y']

def pauli2_gate(idx:int):
    '''
    only input 0 - 255
    '''
    binary = '{:08b}'.format(idx)
    pauli = idx%16
    p1 = pauli_list[pauli//4]
    p2 = pauli_list[pauli%4]
    if int(binary[3]):
        p2 = 'i'+p2
    if int(binary[2]):
        p2 = '-'+p2
    if int(binary[1]):
        p1 = 'i'+p1
    if int(binary[0]):
        p1 = '-'+p1

    gatelist = [p1,p2]
    return gatelist


# for i in range(256):
#     print(pauli2_gate(i),i)

def reverse(sequence:list):
    q1w_sum, q2w_sum, q11, q21, q12, q22, q1n, q2n, q1i, q2i = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for i,idx in np.ndenumerate(sequence):
        b = '{:08b}'.format(idx)
        q1n += q1w_sum*int(b[4]) + int(b[0])#negative
        q2n += q2w_sum*int(b[6]) + int(b[2])
        q1w_sum +=int(b[5])
        q2w_sum +=int(b[7])
        q1i += int(b[1])
        q2i += int(b[3])
        q11 +=int(b[4])
        q12 +=int(b[5])
        q21 +=int(b[6])
        q22 +=int(b[7])
    reverse = str((q1n+(q1i%4//2))%2)+str(q1i%2)+str((q2n+(q2i%4//2))%2)+str(q2i%2)+str(q11%2)+str(q12%2)+str(q21%2)+str(q22%2)
    idx_r = int(reverse,2)
    return idx_r

