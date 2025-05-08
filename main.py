# Names: Del Endecott, Ian Collins, Zeidan Abdelrahman
# KUIDs: , 3051520, 
# Date: 4/25/25
# Date last modified: 4/26/25
# Course: EECS 510
# Purpose: Run main simulation of Zelda character interactions

import regex as re
from characters import Link, Zelda, Impa, NPC

def accept(w, i):
    # Zelda Dialog Accept String = {E((RTER)+(FS))*R(YQ+N)B}
    # Impa Dialog Accept String = {ER(TE)*(YQ+N)B}
    match i:
        case 0: # Impa's Dialog
            accept_str = '^(E)(TE)*(YQ|N)(BB)$'
            x = re.match(accept_str, w)
            return True if x != None else False
        case 1: # Zelda's Dialog
            accept_str = '^(E)(FS)*(TE(FS)*)*(YQ|N)(BB)$'
            x = re.match(accept_str, w)
            return True if x != None else False

def simulate_dialog(link: Link, character: NPC, w: str):
    # Setting up structures and string format
    w = w.upper().strip()
    l = len(w)
    if l < 3 or w[0] != 'E': #Min length of any string in Zelda grammar
        return False
    i = 0 # Word iterator
    c = w[i] # Current letter in string
    cur_character = character # Track who is speaking
    #Until stack is empty or speech exceeds word length
    while i < l:
        c = w[i]
        if i + 1 == l and c != 'B':
            return False
        # Consumes stack item and pushes appropriate stack valiable
        match c:
            case 'E': # Exposistion
                if w[i+1] not in {'T', 'F', 'Y', 'N'}:
                    return False
                character.speak(c)
                cur_character = link
            case 'T': # Tell me more
                if w[i+1] not in {'E'}:
                    return False
                link.speak(c)
                cur_character = character
            case 'F': # Feed
                if w[i+1] not in {'S'} and character == Impa():
                    return False
                character.speak('F')
                cur_character = character
            case 'S':
                if w[i+1] not in {'T', 'F', 'Y', 'N'}:
                    return False
                link.speak('S')
                cur_character = character
            case 'Q': # Quest
                if w[i+1] not in {'B'}:
                    return False
                character.speak(c)
                cur_character = link
            case 'Y': # Yes
                if w[i+1] not in {'Q'}:
                    return False
                link.speak(c)
                cur_character = character
            case 'N': # No
                if w[i+1] not in {'B'}:
                    return False
                link.speak(c)
                cur_character = character
            case 'B': # Bye
                if c == 'B' and i >= l:
                    return False
                # Correct character responds 
                if cur_character == character and i + 1 == l:
                    link.speak(c)
                    character.speak(c)
                elif i + 1 == l:
                    character.speak(c)
                    link.speak(c)
        i += 1

    return True

def main():
    impa_str = ['ENBB', 'EYQBB', 'FETEYQBB' 'ETETEYQBB', 'ETETETBB'] # True, True, False, True, False
    zelda_str = ['EFSTEYQBB', 'EFSBB', 'YQB', 'ETEFSNBB', 'ENBB'] # True, False, False, True, True
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