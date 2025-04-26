# Names: Del Endecott, Ian Collins, Zeidan Abdelrahman
# KUIDs: , 3051520, 
# Date: 4/25/25
# Date last modified: 4/26/25
# Course: EECS 510
# Purpose: Define each Zelda character interactions and vocabulary

class Link():
    def __init__(self):
        state = ['Idle', 'Eat', 'Fight', 'Dialog']
        vocab = ['idle', 'hi', 'yes', 'no', 'tell', 'fight', 'win', 'retreat', 'eat', 'backstory', 'bye']
        cur_state = state[0]
        health = 5
        if_sheild = False
        if_potion = False

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

    def dialog(self, item, string):
        #Consumes stack item and pushes
        items = ['E', 'R', 'Q', 'F', 'B', '']
        responce = {items[1]:(self.vocab[4], items[0]), #Asking for more info
                    items[1]:(self.vocab[2], items[2]), #Accepting quest
                    items[1]:(self.vocab[3], items[4]), #Declining quest
                    items[3]:(self.vocab[9], items[5]), #Give backstory after fed
                    items[4]:(self.vocab[10], items[5])} #Leave interaction
        
        if item not in responce.keys:
            return None
        else:
            return 