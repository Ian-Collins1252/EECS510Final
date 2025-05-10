# class and methods to simulate tape/head interactions for a turing machine

class Tape():
    def __init__(self, str_in = ""):
        self.tape = [] # a list will act as a tape
        for i in str_in: # each char in input string will be its own entry on the list
            self.tape.append(i)
        self.head = 0 # integer tracking where the head is on the tape using list index
          
    def __str__(self): # when printing a Tape object, return the contents of the tape as one string
        return ''.join(str(elem) for elem in self.tape)      
    
    def get_head(self): # return the character the head is at
        return self.tape[self.head]
            
    def right(self): # move head right one space on the tape
        if self.head + 1 <= len(self.tape)-1: # only move if there's tape available
            self.head += 1
        else: # don't move if no tape available
            pass
    
    def left(self): # move head left one space on the tape
        if self.head - 1 >= 0: # only move if there's tape available
            self.head -= 1
        else:# don't move if no tape available
            pass
            
    def add(self,char): # add one char to the tape at the head's position
        self.tape.insert(self.head, char)
        
    def pop(self): #remove char at head's position. note that head technically moves right after pop by default
        self.tape.pop(self.head)
        
    def left_until(self, char): # move left until a specified character is found (or tape ends)
        if char != 'end': # look for a character
           try:
               self.head = self.tape.index(char, 0, self.head) # throws an error if char not found
           except:
               #print(f"char {char} not present, moving to end") # placeholder for troubleshooting
               self.head = 0
        else: # move to the leftmost end
            self.head = 0
            
    def right_until(self, char): # move right until a specified character is found (or tape ends)
        if char != 'end': # look for a character
           try:
               self.head = self.tape.index(char, self.head) # throws an error if char not found
           except:
               #print(f"char {char} not present, moving to end") # placeholder for troubleshooting
               self.head = len(self.tape)-1
        else: # move to the rightmost end
            self.head = len(self.tape)-1
    