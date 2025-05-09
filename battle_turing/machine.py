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
                        i += 1 # increment counter
                    
                    # change upper to lowercase to indicate that this enemy was hurt    
                    elif self.T3.tape[i] == 'V' or self.T3.tape[i] == 'G':
                        self.T3.tape[i] = self.T3.tape[i].lower()
                        self.T3.head = i
                        current = 6 # to bomb 3
                        break # leave loop so state will change
                    else:
                        i += 1 # keep moving            
                self.T3.head = len(self.T3.tape)-1 # after completing the loop, make sure the head is correct
                current = 7 # to swap state
                
            case 6: # bomb 3, part 2 of the loop to -1 all enemy health [5]
                self.T3.right() # move right off the lowercase char
                self.T3.pop() # -1 health
                self.T3.left() # move left, back onto the lowercase so bomb 2 will reset it to uppercase
                current = 5 # back to bomb 2
            
            case 7: # swap [0,8,11,12]
                self.T1.left_until('end') # reset both health tapes
                self.T3.left_until('end') 
                
                if self.T4.tape.count('V') > 0 or self.T4.tape.count('G') > 0:
                    if self.T4.tape.index('V') < self.T4.tape.index('G'): # right until V or G, whatever's first
                        self.T4.right_until('V')
                        current = 11 # enemy turn
                    else: 
                        self.T4.right_until('G')
                        current = 12 # ganon's turn
                    
                else: # if there are no more V or G in T4
                    current = 8 # go to status and do a health check
            
            case 8: # status [0,9,15] check to see if anyone's dead
                # create a temp list with only health chars on it to check if link is alive
                temp = self.t1.tape
                try: 
                    temp = self.T1.tape.remove('O') # remove shield if it's there
                except: 
                    continue # if no shield, no need to do anything
                try: 
                    temp = self.T1.tape.remove('P') # remove potion charge if it's there
                except: 
                    continue # if not no need to do anything
                
                if not temp: # if the temp string is empty
                    current = 15 # link is dead, stop the machine
                    break
                
                # now check if any enemies have died
                self.T3.left_until('end') # reset enemy tapes first
                self.T4.left_until('end')
                
                if self.T3.tape.count('V') > 0 or self.T3.tape.count('G') > 0:
                    if self.T3.tape.index('V') < self.T3.tape.index('G'): # right until V or G, whatever's first
                        self.T3.right_until('V')
                        current = 9 # do a health check on this entity
                        break
                    else: 
                        self.T3.right_until('G')
                        current = 9 # health check on ganon
                        break
                else: # last enemy found but i forgor how handl
                    
                            
            case 9: # health check [8,10] ensure a given entity has at least 1 health
                self.T3.right() # move right 1
                # check if there are 2 consecutive entity markers (if VV or VG or GV)
                if self.T3.get_head() == 'V' or self.T3.get_head() == 'G':
                    
                    self.T3.left() # move left 1 so the head is on the marker for the dead enemy
                    if self.T3.get_head() == 'V': 
                        self.T4.right_until('V') # find the first enemy on the turn tape
                        # enemies are indistinguishable, so deleting the first one found is fine
                    else: 
                        self.T4.right_until('G') # find ganon's turns    
                    self.T4.pop() # remove the enemy marker
                    current = 10 # go to remove dead to start loop
                current = 8 # entity is alive, return to status checks
                    
            
            case 10: # remove dead [9] state that loops thru a tape until a section of actions is removed
                if self.T4.tape.count('V') > 0:
                    for i in range(self.T4.head, self.T4.tape.index('V')):
                        self.T4.pop() # remove actions until next marker
                        i += 1
                elif self.T4.tape.count('G') > 0:
                    for i in range(self.T4.head, self.T4.tape.index('G')):
                        self.T4.pop() # remove actions until next marker
                        i += 1
                else: # if no other markers are found, this is the last enemy on the tape
                    for i in range(self.T4.head, len(self.T4.tape)):
                        self.T4.pop() # remove actions until tape ends
                        i += 1
                self.T3.pop() # finally, remove the dead enemy from health tape
                current = 9 # go back to health checking
            
            case 11:
                pass
            
            case 12:
                pass
            
            case 13:
                pass
            
            case 14:
                pass
               
        return current