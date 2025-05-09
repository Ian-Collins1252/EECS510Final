# main file 

from tape import Tape
from machine import Machine

# main takes four string inputs that go on the tapes
def main(s1, s2, s3, s4):
    m = Machine(s1,s2,s3,s4)
    
    '''each state of the machine is assigned a number for ease of implementation 
        [states w/available transitions are in brackets, not including self loops]
        0: start round (initial state) [1]
        1: link [2,3,4,7]
        2: spin attack [5]
        3: potion [7]
        4: bomb 1 [5]
        5: bomb 2 [6,7]
        6: bomb 3 [5]
        7: swap [8,11,12]
        8: status [0,9,15]
        9: check health [8,10]
        10: remove dead [9]
        11: enemy [4,8,14]
        12: ganon [8,13,14]
        13: charge [8]
        14: remove fled [aaaaaaaaaaa]
        15: battle over (halt state)
    '''
    state = 0 # start in state 0
    while state != 15: # while not in the halt state
        m.state_match(state)

s1 = LLL
s2 = AAA
s3 = VXXX
s4 = VA       
main(s1,s2,s3,s4)