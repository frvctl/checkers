import pygame
import pickle
from pygame.locals import *

class button:
    """ Used for the menu """
    def __init__(self,x,y,w,h,text,f): 
        """ Constructor for button class """
        self.x = x       # X-coord for the button's box
        self.y = y       # Y=coord for the button's box
        self.w = w       # Width of the button's box
        self.h = h       # Height of the button's box
        self.text = text # The name of the button - text displayed on it
        self.f = f       # The function called
        
    def draw(self,windowSurface, font,rectColor = (255,255,255), textColor = (255,0,0)):
        pygame.draw.rect(windowSurface, rectColor, (self.x , self.y , self.w, self.h))
        text = font.render(self.text, True, textColor)
        textRect = text.get_rect()
        textRect.centerx = self.x + (self.w/2)
        textRect.centery = self.y + (self.h/2)
        windowSurface.blit(text, textRect)
    
    def inside(self,x,y):
        """    """
        if x >= self.x and x < self.x+self.w and y >= self.y and y < self.y+self.h:
            return True
        return False

class Player:
    def __init__(self,color):
        self.col = color
        self.started = False
    def getColor(self):
        return self.col
class HumanPlayer(Player):
    def __init__(self,color):
        Player.__init__(self, color)
    def startTurn(self):
        self.started = True
        return False,None
class ComputerPlayer(Player):
    def __init__(self,color,ai):
        Player.__init__(self, color)
        self.ai = ai
    def __repr__(self):
        if self.ai&1:
            return "Minimax"
        if self.ai&2:
            return "Alphabeta"
        if self.ai&4:
            return "Negascout"
        if self.ai&8:
            return "Random"
    def startTurn(self):
        self.started = True
        return True,self.ai

class recording:
    def __init__(self):
        self.moveList = []
    def add (self,move):
        self.moveList.append(move)
    def clear (self):
        self.moveList = []
    def deleteLast (self):
        if len(self.moveList) > 0:
            return self.moveList.pop()
        print "idiot, no moves"
    def save (self,name):
        with  open(name,'w') as f:
            pickle.dump(self.moveList,f)
    def load (self,name="record.txt"):
        with open(name, 'r') as f:
            self.moveList = pickle.load(f)
        


print "imported"
