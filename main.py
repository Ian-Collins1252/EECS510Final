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
            accept_str = '^ER(TER)*(YQ|N)B$'
            x = re.search(accept_str, w)
            return True if len(w) == x+1 else False
        case 1: # Zelda's Dialog
            accept_str = '^E((RTER)|(FS))*R(YQ|N)B$'
            x = re.search(accept_str, w)
            return True if len(w) == x+1 else False

def simulate_dialog(link: Link, character: NPC, w: str):
    w = w.upper().strip()
    if len(w) >= 3: #Min length of any string in Zelda grammar
        c = w[0]
        w = w[1:]
    else:
        return False
    cur_character = character
    while len(w) != 0:
        if c in {'E', 'Y', 'F', 'N'}: #Determines speaker based on stack item
            result = character.dialog(c, w)
            c = w[0]
            w = '' if len(w) == 1 else w[1:]
            cur_character = link
        elif c in {'R', 'S', 'Q'}: #Determines speaker based on stack item
            result = link.dialog(c, w)
            c = w[0]
            w = '' if len(w) == 1 else w[1:]
            cur_character = character
        # Escape character
        elif c in {'B'}:
            if cur_character == link:
                result = link.dialog(c, w)
            else:
                result = character.dialog(c, w)
        #Checks if string is invalid
        if not result:
            return result

    return result


def main():
    impa_str = ['ERTENB', 'ERYQB', 'B', 'ERTETEYQB', 'ERTERTETQ'] # True, True, False, True, False
    zelda_str = ['EFSRTERYQB', 'EFSB', 'YQB', 'ERTERFSRNB', 'ERNB'] # True, False, False, True, True
    test_case = [impa_str, zelda_str]
    for test, i in enumerate(test_case): # Loop through all test cases 
        for w in test: # Loop through all strings in test case
            result = accept(w, i)
            print(f'Accepted String for Impa Dialog? {w}\n{result}\n')

    

if __name__ == "__main__":
    main()