# class and methods for various interactions between turing machine and tapes

from tape import Tape

class Machine():
    def __init__(self, s1, s2, s3, s4):
        self.T1 = Tape(s1) # tape for link's health
        self.T2 = Tape(s2) # tape for Link's turns
        self.T3 = Tape(s3) # tape for foes' health
        self.T4 = Tape(s4) # tape for foes' turns
        self.tapes = [self.T1, self.T2, self.T3, self.T4]

    
    # at round start, all tapes should have the heads at the leftmost position    
    def start_round(self):
        for i in self.tapes:
            i.left_until('end')
            
    def state_match(self, current):
        match current:
            case 0:
                self.start_round()
                self.T3.right() # step right once on foes' health so link can hit them if he wants
                print("Round start!")
                current = 1 # link always goes first
            
            case 1: # link [2,3,4,7]
                H = self.T2.get_head() # store character with the head on it
                if self.T1.get_head() == 'O': # if link's shield is still up, remove it
                    self.T1.pop()

                # do ONE of the following
                if H == 'A': # if link attacks
                    self.T2.pop() # remove char from turn queue 
                    self.T3.pop() # -1 health to the closest enemy
                    current = 7 # turn over, go to swap state
                
                elif H == 'E': # if link eats
                    self.T2.pop() # remove char from turn queue
                    self.T1.add('L') # +1 health to link 
                    self.T1.left() 
                    current = 7 # turn over, go to swap state
                    
                elif H == 'O': # if link shields 
                    self.T1.add('O') # add shield to link
                    self.T1.left()
                    current = 7 # turn over, go to swap state
                
                elif H == 'P': # if link uses a potion
                    self.T2.pop() # remove char from turn queue
                    current = 3 # move to potion state
                    
                elif H == 'S': # spin attack
                    self.T2.pop()
                    current = 2 # go to spin state
                    
                elif H == 'B': # bomb
                    self.T2.pop()
                    current = 4 # go to bomb 1 state
                    
                else:
                    print(f"rejected, invalid input to t2 ({H}) in state 1")
                    
            case 2: # spin attack [5]
                self.T1.right_until('P') # moves head right until P is found
                self.T1.pop() # remove P
                
                if self.T3.tape.index('V') < self.T3.tape.index('G'): # right until V or G, whatever's first
                    self.T3.right_until('V')
                else: 
                    self.T3.right_until('G')
                self.T3.pop() # -1 health to closest enemy
                current = 5 # go to bomb 2 state, which will take care of -1 health to all enemies
            
            case 3: # potion [7]
                self.T1.right_until('end') # go to the right end of link's health
                self.T1.add('P') # add potion charge
                current = 7 # go to swap state
            
            case 4: # bomb 1, aka the part of bomb that -1 health to link [5]
                self.T1.left_until('end') # reset link's health tape
                self.T3.left_until('end') # reset enemy health tape
                if self.T1.get_head() == 'O': # if link has his shield up
                    pass # damage blocked
                else: 
                    self.T1.pop() # -1 link health
                current = 5 # move to bomb 2
            
            case 5: # bomb 2, part 1 of a loop to -1 all enemy health [6,7]
                # this part is easiest to loop manually instead of using the right_until method
                # due to having more than 2 "move until character" transitions to consider
                for i in range(self.T3.head, len(self.T3.tape)): # check tape right of head
                    # if a lowercase is found, capitalize it, and move on
                    if self.T3.tape[i] == 'v' or self.T3.tape[i] == 'g': 
                        self.T3.tape[i] = self.T3.tape[i].capitalize()
                        self.T3.head = i + 1 # move right so the char will not be considered again
                    
                    # change upper to lowercase to indicate that this enemy was hurt    
                    elif self.T3.tape[i] == 'V' or self.T3.tape[i] == 'G':
                        self.T3.tape[i] = self.T3.tape[i].lower()
                        self.T3.head = i
                        current = 6 # to bomb 3
                        break # leave loop so state will change
                    else:
                        continue # disregard all other chars            
                self.T3.head = len(self.T3.tape)-1 # after completing the loop, make sure the head is correct
                current = 7 # to swap state
                
            case 6: # bomb 3, part 2 of the loop to -1 all enemy health [5]
                self.T3.right() # move right off the lowercase char
                self.T3.pop() # -1 health
                self.T3.left() # move left, back onto the lowercase so bomb 2 will reset it to uppercase
                current = 5 # back to bomb 2
            
            case 7: # swap [0,8]
                
                if self.T4.tape.index('V') < self.T4.tape.index('G'): # right until V or G, whatever's first
                    self.T4.right_until('V')
                else: 
                    self.T4.right_until('G') 
            
            case 8:
                pass
            
            case 9:
                pass
            
            case 10:
                pass
            
            case 11:
                pass
            
            case 12:
                pass
            
            case 13:
                pass
            
            case 14:
                pass
               
        return current