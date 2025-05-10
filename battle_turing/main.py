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
        #print(f"state: {state}")
        state = m.state_match(state)

print(f'''%%%%% BATTLE SETUP %%%%%\n
%%   Step 1: Enter Link's health. This will be tape T1.   %%
    Accepted characters: L
    - L = 1 health''')
s1 = input("T1: ")

print(f'''\n%%   Step 2: Enter Link's actions. This will be tape T2.   %%
    Accepted characters: A, E, O, P, S, B
    - A = attack the nearest enemy (-1 health to nearest enemy)
    - E = eat food (+1 health to self)
    - O = shield (protects Link from most damage)
    - P = drink potion (adds a potion charge. Link must have a potion charge to spin attack.)
    - S = spin attack (consumes 1 potion charge. -2 health to nearest enemy, -1 health all others)
    - B = throw bomb (-1 health to all, including Link)
    
    Extra rules: 
    - if Link runs out of actions, he will flee the battle and the machine will halt.
    - Any S must have a P before it in the tape. There can be more Ps than Ss, but not the other way.''')
s2 = input("T2: ")

print(f'''\n%%   Step 3: Enter enemy health. This will be tape T3.   %%
    HOW: 1) start with an entity marker. ex: V
         2) add desired amount of health. ex: VXXX
         3) repeat as many times as you want. ex: VXXXVXVXXVXGXXXX
    Note that the entity on the leftmost side of the tape is the entity closest to Link.
         
    Accepted characters: V, G, X
    - V = entity marker for a Bokoblin (generic, indistinguishable enemy)
    - G = entity marker for Ganon (can only be one at a time)
    - X = 1 health
    
    Extra rules:
    - The left most character must be either V or G.
    - Each V or G must be followed by at least 1 X.
        Disclaimer: breaking this rule doesn't break the machine, but that enemy will just die instantly and be pointless
    - There can only be one G on the tape.''')
s3 = input("T3: ")

print(f'''\n%%   Step 4: Enter enemy actions. This will be tape T4.   %%
    HOW: 1) start with an entity marker. ex: V
         2) add desired actions. ex: VAAB
         3) repeat as many times as you want. ex: VAABVAVBBVAGTACC
         
    VERY IMPORTANT: your T3 and T4 must have the entity markers in the same order.
        Acceptable = T3: VXXVXGXX , T4: VAVBBBGACACAC. There are 2 Vs and a G.
        Not Acceptable = T3: GATVABVB, T4: VAAGTTTVBAB. T3 has G then V, but T4 has V then G.
        
    Accepted characters to follow V:
    - A = attack Link (-1 health to Link)
    - B = throw bomb (-1 health to all, including self)
    
    Accepted characters to follow G:
    - A = attack Link (-1 health to Link)
    - C = charge (breaks Link's shield if it's up. if it's not, -2 to Link)
    - T = energy ball attack (-1 to link if he is not shielding. if he is shielding, -1 to self)
    
    Extra Rules: 
    - see VERY IMPORTANT
    - Any enemy that runs out of actions will flee the battle.
    - V can only be followed by A or B, and G can only be followed by A, C, or T.
    
    Your T3 input, as a reminder: {s3}''')
s4 = input("T4: ")
main(s1,s2,s3,s4)