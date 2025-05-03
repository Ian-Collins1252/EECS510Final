# Names: Del Endecott, Ian Collins, Zeidan Abdelrahman
# KUIDs: , 3051520, 
# Date: 4/25/25
# Date last modified: 4/26/25
# Course: EECS 510
# Purpose: Run main simulation of Zelda character interactions

import regex as re

def accept(w, i):
    # Zelda Dialog Accept String = {E((TE)+(FS))*(YQ+N)B}
    # Impa Dialog Accept String = {E(TE)*(YQ+N)B}
    match i:
        case 0: # Impa's Dialog
            accept_str = '^E(TE)*(YQ|N)B$'
            x = re.search(accept_str, w)
            return True if len(w) == x+1 else False
        case 1: # Zelda's Dialog
            accept_str = '^E((TE)|(FS))*(YQ|N)B$'
            x = re.search(accept_str, w)
            return True if len(w) == x+1 else False
        

def main():
    impa_str = ['ETENB', 'EYQB', 'B', 'ETETEYQB', 'ETETETQ'] # True, True, False, True, False
    zelda_str = ['EFSTEYQB', 'EFSB', 'YQB', 'ETEFSNB', 'EFSNB'] # True, False, False, True, True
    test_case = [impa_str, zelda_str]
    for test, i in enumerate(test_case): # Loop through all test cases 
        for w in test: # Loop through all strings in test case
            result = accept(w, i)
            print(f'Accepted String for Impa Dialog? {w}\n{result}\n')

    

if __name__ == "__main__":
    main()