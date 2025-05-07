# Names: Del Endecott, Ian Collins, Zeidan Abdelrahman
# KUIDs: , 3051520, 
# Date: 4/25/25
# Date last modified: 4/26/25
# Course: EECS 510
# Purpose: Run main simulation of Zelda character interactions

import regex as re
from random import randint
from characters import Link, Zelda, Impa, NPC

# Stack for PDA
class Stack():
    def __init__(self):
        self.stack = []

    def top(self):
        if self.size() > 0:
            return self.stack[0]
        
    def pop(self):
        top = ''
        if self.size() > 0:
            top = self.stack.pop(0)
        return top

    def push(self, c):
        self.stack.insert(0, c)

    def size(self):
        return len(self.stack)

def accept(w, i):
    # Zelda Dialog Accept String = {E((RTER)+(FS))*R(YQ+N)B}
    # Impa Dialog Accept String = {ER(TE)*(YQ+N)B}
    match i:
        case 0: # Impa's Dialog
            accept_str = '^(HHE)(TE)*(YQ|N)B$'
            x = re.match(accept_str, w)
            return True if x != None else False
        case 1: # Zelda's Dialog
            accept_str = '^(HHE)(FS)*(TE(FS)*)*(YQ|N)B$'
            x = re.match(accept_str, w)
            return True if x != None else False

def simulate_dialog(link: Link, character: NPC, w: str):
    # Setting up structures and string format
    stack = Stack()
    stack.push('E')
    w = w.upper().strip()
    if len(w) < 3: #Min length of any string in Zelda grammar
        return False
    i = 0 # Word iterator
    cur_character = character # Track who is speaking
    # Greeting (coin flip who speaks first as sometimes Link walks up and interacts (Link speaks first) or gets caught in a cut-scene (character speaks first))
    if randint(0, 1) == 0:
        link.speak('H')
        character.speak('H')
    else:
        character.speak('H')
        link.speak('H')
    i += 2
    #Until stack is empty or speech exceeds word length
    while stack.size() != 0 and i < len(w):
        # Handle accept state outside of given character dialog method for how strings function
        if stack.top() == 'B' and i + 1 != len(w):
            print('unaccpet bye char')
            return False
        # Verify iteraction is valid
        elif not character.dialog(stack.top(), w[i]) or not link.dialog(stack.top(), w[i]):
            print('invalid interaction on either side')
            return False
        # Feeding link consumes nothing from the stack, so this blocks popping anything off the stack
        if w[i] == 'F':
            character.speak('F')
            i += 1
            stack.push('F')
            continue
        # Consumes stack item and pushes appropriate stack valiable
        c = stack.pop()
        match c:
            case 'E': # Exposistion
                character.speak(c)
                i += 1
                stack.push('R')
                cur_character = link
            case 'F': # Feed
                link.speak('S')
                i += 1
                stack.push('E')
                cur_character = character
            case 'R': # Responce
                # Push variable depends upon the following vocab in word
                if w[i] == 'T':
                    link.speak(w[i])
                    i += 1
                    stack.push('E')
                elif w[i] == 'Y':
                    link.speak(w[i])
                    i += i
                    stack.push('Q')
                elif w[i] == 'N':
                    link.speak(w[i])
                    i += 1
                    stack.push('B')
                cur_character = character
            case 'Q': # Quest
                character.speak(c)
                i += 1
                stack.push('B')
                cur_character = link
            case 'B': # Bye
                # Correct character responds 
                if cur_character == link:
                    link.speak(c)
                    character.speak(c)
                else:
                    character.speak(c)
                    link.speak(c)
                i += 1

    return True

def main():
    impa_str = ['HHENB', 'HHEYQB', 'HHEB', 'HHETETEYQB', 'HHETETETQ'] # True, True, False, True, False
    zelda_str = ['HHEFSTEYQB', 'EFSB', 'YQB', 'HHETEFSNB', 'HHENB'] # True, False, False, True, True
    link = Link()
    zelda = Zelda()
    impa = Impa()
    characters = [impa, zelda]
    test_case = [impa_str, zelda_str]
    for i, test in enumerate(test_case): # Loop through all test cases 
        character = characters[i]
        for w in test: # Loop through all strings in test case
            result = accept(w, i)
            print(f'\nAccepted String for {character} Dialog? {w}\n{result}')
            print(f'Simulate accepted string between {character} and Link for str: {w}')
            sim_result = simulate_dialog(link, character, w)
            print(sim_result)


if __name__ == "__main__":
    main()