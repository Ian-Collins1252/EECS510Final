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
    
    # check and see if any tapes are empty        
    def empty_tape(self):
        a = 0
        for i in range(0, len(self.tapes)):
            if len(str(self.tapes[i])) > 0:
                a += 1 # tape isn't empty, increment counter
        if a == len(self.tapes): # if counter i = number of tapes, no tapes are empty
            return False
        else:
            return True
                
            
    def state_match(self, current):
        match current:
            case 0:
                self.start_round()
                self.T3.right() # step right once on foes' health so link can hit them if he wants
                print(f"Round start! T1: {self.T1} | T2: {self.T2} | T3: {self.T3} | T4: {self.T4}")
                current = 1 # link always goes first
            
            case 1: # link [2,3,4,7]
                print(f"Link's turn: {self.T2}")
                H = self.T2.get_head() # store character with the head on it
                if self.T1.get_head() == 'O': # if link's shield is still up, remove it
                    self.T1.pop()

                # do ONE of the following
                if H == 'A': # if link attacks
                    self.T2.pop() # remove char from turn queue 
                    self.T3.pop() # -1 health to the closest enemy
                    print(f"Link attacks. T2: {self.T2} | T3: {self.T3}")
                    current = 7 # turn over, go to swap state
                
                elif H == 'E': # if link eats
                    self.T2.pop() # remove char from turn queue
                    self.T1.add('L') # +1 health to link 
                    self.T1.left()
                    print(f"Link eats. T1: {self.T1} | T2: {self.T2}")
                    current = 7 # turn over, go to swap state
                    
                elif H == 'O': # if link shields 
                    self.T1.add('O') # add shield to link
                    self.T1.left()
                    print(f"Link shields. T1: {self.T1}")
                    current = 7 # turn over, go to swap state
                
                elif H == 'P': # if link uses a potion
                    self.T2.pop() # remove char from turn queue
                    current = 3 # move to potion state
                    
                elif H == 'S': # spin attack
                    self.T2.pop()
                    current = 2 # go to spin state
                    
                elif H == 'B': # bomb
                    self.T2.pop()
                    print(f"Link throws a bomb. T2: {self.T2}")
                    current = 4 # go to bomb 1 state
                    
                else:
                    current = 15 # string rejected
                    raise Exception(f"String rejected, invalid input to T2 ({H}) in state 1")
                    
            case 2: # spin attack [5]
                if self.T1.tape.count('P') == 0:
                    current = 15 # rejected
                    raise Exception("String rejected, no potion charge available (make sure T2 has a P before an S!)")
                    
                self.T1.right_until('P') # moves head right until P is found
                self.T1.pop() # remove P
                
                # move T3 tape head to the entity marker closest to the left
                if self.T3.tape.count('V') >= 1 and self.T3.tape.count('G') >= 1:
                    if self.T3.tape.index('V') < self.T3.tape.index('G'): # right until V or G, whatever's first
                        self.T3.right_until('V')
                    else: 
                        self.T3.right_until('G')    
                elif self.T3.tape.count('V') == 0 and self.T3.tape.count('G') >= 1: # only ganon
                    self.T3.right_until('G')  
                else: # no ganon
                    self.T3.right_until('V')
                
                self.T3.pop() # -1 health to closest enemy
                print(f"Link does a spin attack. T1: {self.T1} | T3: {self.T3}")
                current = 5 # go to bomb 2 state, which will take care of -1 health to all enemies
            
            case 3: # potion [7]
                self.T1.right_until('end') # go to the right end of link's health
                self.T1.add('P') # add potion charge
                print(f"Link uses a potion. T1: {self.T1}")
                current = 7 # go to swap state
            
            case 4: # bomb 1, aka the part of bomb that -1 health to link [5]
                self.T1.left_until('end') # reset link's health tape
                self.T3.left_until('end') # reset enemy health tape
                if self.T1.get_head() == 'O': # if link has his shield up
                    print(f"Link blocks the attack. T1: {self.T1}") # damage blocked
                else: 
                    self.T1.pop() # -1 link health
                print(f"Link hits himself with the bomb. T1: {self.T1}")
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
                print(f"All enemies take damage. T3: {self.T3}")
                current = 7 # to swap state
                
            case 6: # bomb 3, part 2 of the loop to -1 all enemy health [5]
                self.T3.right() # move right off the lowercase char
                self.T3.pop() # -1 health
                self.T3.left() # move left, back onto the lowercase so bomb 2 will reset it to uppercase
                current = 5 # back to bomb 2
            
            case 7: # swap [8,11,12]
                
                if self.empty_tape() == True:
                    # empty tape found- battle is over
                    current = 15
                    raise Exception(f"A tape is empty, the battle is over. T1: {self.T1} | T2: {self.T2} | T3: {self.T3} | T4: {self.T4}")
                    #return current
                
                self.T1.left_until('end') # reset both health tapes
                self.T3.left_until('end') 
                
                # find next to move
                if self.T4.tape[self.T4.head:].count('V') >= 1 and self.T4.tape[self.T4.head:].count('G') >= 1:
                    if self.T4.tape.index('V') < self.T4.tape.index('G'): # right until V or G, whatever's first
                        self.T4.right_until('V')
                        self.T4.right() # move past turn marker
                        print(self.T4.tape[self.T4.head], self.T4.head)
                        print(f"Bokoblin's turn. T4: {self.T4}")
                        current = 11 # enemy turn
                    else: 
                        self.T4.right_until('G')
                        self.T4.right() # move past turn marker
                        print(f"Ganon's turn. T4: {self.T4}")
                        current = 12 # ganon's turn
                        
                elif self.T4.tape[self.T4.head:].count('V') == 0 and self.T4.tape[self.T4.head:].count('G') >= 1:
                    self.T4.right_until('G')
                    self.T4.right() # move past turn marker
                    print(f"Ganon's turn. T4: {self.T4}")
                    current = 12 # ganon's turn
                    
                elif self.T4.tape[self.T4.head:].count('G') == 0 and self.T4.tape[self.T4.head:].count('V') >= 1:
                    print(self.T4.tape[self.T4.head:].count('V'))
                    self.T4.right_until('V')
                    self.T4.right() # move past turn marker
                    print(self.T4.tape[self.T4.head], self.T4.head)
                    print(f"Bokoblin's turn. T4: {self.T4}")
                    current = 11 # enemy turn
                    
                else: # if there are no more V or G in T4
                    current = 8 # go to status and do a health check
            
            case 8: # status [0,9,15] check to see if anyone's dead
                # create a temp list with only health chars on it to check if link is alive
                temp = self.T1.tape
                try: 
                    temp = self.T1.tape.remove('O') # remove shield if it's there
                except: 
                    pass # if no shield, no need to do anything
                try: 
                    temp = self.T1.tape.remove('P') # remove potion charge if it's there
                except: 
                    pass # if not no need to do anything
                
                if not temp: # if the temp string is empty
                    current = 15 # link is dead, stop the machine
                    raise Exception(f"Link is dead, the battle is over. T1: {self.T1}")
                
                # now check if any enemies have died
                self.T3.left_until('end') # reset enemy tapes first
                self.T4.left_until('end')
                
                if self.T3.tape.count('V') >= 1 and self.T3.tape.count('G') >= 1:
                    if self.T3.tape.index('V') < self.T3.tape.index('G'): # right until V or G, whatever's first
                        self.T3.right_until('V')
                        current = 9 # do a health check on this entity
                    else: 
                        self.T3.right_until('G')
                        current = 9 # health check on ganon
                elif self.T3.tape.count('V') == 0 and self.T3.tape.count('G') >= 1:
                    self.T3.right_until('G')
                    current = 9 # health check on ganon
                    
                elif self.T3.tape.count('G') == 0 and self.T3.tape.count('V') >= 1:
                    self.T3.right_until('V')
                    current = 9 # do a health check on this entity
                
                if self.empty_tape() == True: # if anything is empty
                    current = 15
                    raise Exception(f"A tape is empty, the battle is over. T1: {self.T1} | T2: {self.T2} | T3: {self.T3} | T4: {self.T4}")
                else:
                    current = 0 # back to the start of the round
                                  
            case 9: # health check [8,10] ensure a given entity has at least 1 health
                self.T3.right() # move right 1
                # check if there are 2 consecutive entity markers (if VV or VG or GV)
                if self.T3.get_head() == 'V' or self.T3.get_head() == 'G':
                    print(f"Health check found something. T3: {self.T3} | T4: {self.T4}")
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
                print(f"Body despawned. T3: {self.T3} | T4: {self.T4}")
                current = 9 # go back to health checking
            
            case 11: # enemy [4,7,14]
                H = self.T4.get_head() # save char head is on for convenience
                if H == 'V' or H == 'G':
                    current = 14 # this enemy is out of turns- remove
                    
                elif H == 'A':
                    self.T4.pop()
                    if self.T1.get_head != 'O': # if link isn't shielding
                        self.T1.pop() # -1 to link
                        print(f"Bokoblin attacks. T1: {self.T1} | T4: {self.T4}")
                    else:
                        print(f"Link blocks Bokoblin's attack. T4: {self.T4}")
                    current = 7 # turn over, go to swap
                
                elif H == 'B':
                    self.T4.pop()
                    print(f"Bokoblin throws a bomb. T4: {self.T4}")
                    current = 5 # go to bomb 1- no need to make sure enemy hits itself, bomb 1 takes care of that
            
                else: 
                    current = 15 # string rejected
                    raise Exception(f"String rejected, invalid input to T4 ({H}) in state 11")
                    
            case 12: # ganon [7,13,14]
                H = self.T4.get_head() # save char head is on for convenience
                if H == 'V' or H == 'G':
                    current = 14 # ganon is out of turns- remove
                
                elif H == 'C': # charge attack- either does 2 damage or breaks link's shield
                    self.T4.pop()
                    if self.T1.get_head() == 'O': # if link is shielding
                        self.T1.pop() # he isn't anymore!
                        print(f"Ganon charges and breaks Link's shield! T1: {self.T1} | T4: {self.T4}")
                        current = 7 # turn over
                    else: # remove 1 health
                        self.T1.pop()
                        current = 13 # go to charge state to deal the rest of the damage
                
                elif H == 'A': # regular attack
                    self.T4.pop()
                    if self.T1.get_head != 'O': # if link isn't shielding
                        self.T1.pop() # -1 to link
                        print(f"Ganon attacks Link. T1: {self.T1} | T4: {self.T4}")
                    else:
                        print(f"Link blocks Ganon's attack. T1: {self.T1} | T4: {self.T4}")
                    current = 7 # turn over, go to swap
                
                elif H == 'T': # energy ball tennis!
                    self.T4.pop()
                    print(f"Ganon uses an energy ball attack. T4: {self.T4}")
                    if self.T1.get_head != 'O': # if link isn't shielding
                        self.T1.pop() # -1 to link
                        print(f"The energy ball hits Link. T1: {self.T1}")
                    else: 
                        self.T3.right_until('G') # -1 to self
                        self.T3.pop()
                        print(f"Link deflects it with his shield! T3: {self.T3}")
                    current = 7 # turn over, go to swap
                    
                else: 
                    current = 15 # string rejected
                    raise Exception(f"String rejected, invalid input to T4 ({H}) in state 12")
            
            case 13: # charge [7] only exists so ganon's charge can do 2 damage to link
                self.T1.pop()
                print(f"Ganon charges at Link! T1: {self.T1} | T4: {self.T4}")
                current = 7 # turn over
            
            case 14:
                self.T3.left_until('end') # if we're in this state then something in this tape will be popped
                self.T3.right_until(self.T4.get_head()) # move to matching marker on health tape
                self.T3.pop() # and remove it
                    
                if self.T3.tape.count('V') > 0:
                    for i in range(self.T3.head, self.T3.tape.index('V')):
                        self.T3.pop() # remove health until next marker
                        i += 1
                elif self.T3.tape.count('G') > 0:
                    for i in range(self.T3.head, self.T3.tape.index('G')):
                        self.T4.pop() # remove health until next marker
                        i += 1
                else: # if no other markers are found, this is the last enemy on the tape
                    for i in range(self.T3.head, len(self.T3.tape)):
                        self.T3.pop() # remove health until tape ends
                        i += 1
                self.T4.pop() # finally, remove the entity marker from the action tape
                print(f"Ran away. T3: {self.T3} | T4: {self.T4}")
                current = 7 # go back to swap state          
        return current