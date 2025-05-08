# Names: Del Endecott, Ian Collins, Zeidan Abdelrahman
# KUIDs: , 3051520, 
# Date: 4/25/25
# Date last modified: 4/26/25
# Course: EECS 510
# Purpose: Define each Zelda character interactions and vocabulary

class Link():
    def __init__(self):
        self.name = 'Link'
        self.states = ['Idle', 'Eat', 'Fight', 'Dialog']
        self.vocab = {'I':'idle', 
                      'H':'hi', 
                      'Y':'yes',
                      'N':'no', 
                      'T':'tell', 
                      'F':'fight', 
                      'W':'win', 
                      'R':'retreat', 
                      'E':'eat', 
                      'S':'backstory', 
                      'B':'bye'}
        self.cur_state = self.states[0]
        self.health = 5
        self.if_sheild = False
        self.if_potion = False

    def change_behavior(self, input):
        transitions = {(self.state[0], self.vocab[0]):self.state[0], #Idle to Idle
                       (self.state[0], self.vocab[1]):self.state[3], #Idle to Dialog
                       (self.state[0], self.vocab[8]):self.state[1], #Idle to Eat
                       (self.state[0], self.vocab[5]):self.state[2], #Idle to Fight
                       (self.state[1], self.vocab[0]):self.state[0], #Eat to Idle
                       (self.state[2], self.vocab[6]):self.state[0], #Fight to Idle
                       (self.state[2], self.vocab[7]):self.state[0], #Fight to Idle
                       (self.state[3], self.vocab[10]):self.state[0]} #Dialog to Idle
        
        if (self.cur_state, input) not in transitions.keys:
            return
        else:
            self.cur_state = transitions[(self.cur_state, input)]

    def speak(self, i: str):
        print(f'Link: "{self.vocab[i]}"')

    def print_state(self):
        print(f'Link\'s State: {self.cur_state}')

    def __eq__(self, other):
        return self.name == other.name

class NPC():
    def __init__(self):
        self.states = ['Idle', 'Dialog']
        self.vocab = {'I':'idle',
                      'H':'hi',
                      'E':'exposition',
                      'Q':'quest',
                      'B':'bye'}
        self.cur_state = self.states[0]
        self.name = 'Satori' #RIP

    def name(self):
        return self.name

    def speak(self, i: str):
        print(f'{self.name}: "{self.vocab[i]}"')

    def __str__(self):
        return f'{self.name}'
    
    def __eq__(self, other):
        return self.name == other.name
    
class Zelda(NPC):
    def __init__(self):
        self.vocab = {'I':'idle',
                      'H':'hi',
                      'E':'exposition',
                      'Q':'quest',
                      'F':'feed',
                      'B':'bye'}
        self.name = 'Zelda'

class Impa(NPC):
    def __init__(self):
        super().__init__()
        self.name = 'Impa'
            
class Enemy():
    def __init__(self):
        hp = 1