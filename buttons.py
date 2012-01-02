from constants import *
from game import pygame, sys, record, legal_moves, doComputer, resetBoard

def resetGame():  
    """ Allow's the game to be reset"""   
    global gameOver,redTurn,computerPlayer
    gameOver = False
    redTurn = False
    resetBoard()    
  
def startmulti():   
    """ Multiplayer game mode start button. In the menu."""    
    global gameStarted,players
    players = [HumanPlayer(PIECE_BLACK),HumanPlayer(PIECE_RED)]
    if gameOver or computerPlayer:
        resetGame()
    gameStarted = True
    
def exitbutton(): 
    """ Button used to exit the game. In the menu.""" 
    pygame.quit()
    sys.exit()
    
def miniMaxButton():
    global MINIMAX, gameStarted, computerPlayer,players
    players = [HumanPlayer(PIECE_BLACK),ComputerPlayer(PIECE_RED,False,True,False)]
    if gameOver or not computerPlayer:
        resetGame()
    computerPlayer = True
    gameStarted = True

def alphaBetaButton():  
    global ALPHABETA, gameStarted, computerPlayer,players
    players = [HumanPlayer(PIECE_BLACK),ComputerPlayer(PIECE_RED,True,False,False)]
    if gameOver or not computerPlayer:
        resetGame()
    computerPlayer = True
    gameStarted = True

def negaScoutButton():
    global gameStarted, computerPlayer, players
    players = [HumanPlayer(PIECE_BLACK),ComputerPlayer(PIECE_RED,False,False,True)]
    if gameOver or not computerPlayer:
        resetGame()
    computerPlayer = True
    gameStarted = True
    
def computerBattleButton():
    global gameStarted, computerPlayer, players
    players = [ComputerPlayer(PIECE_BLACK,True,False,False),ComputerPlayer(PIECE_RED,False,False,True)]
    if gameOver or not computerPlayer:
        resetGame()
    computerPlayer = True
    gameStarted = True
    
def undoButton():
    """ Undoes moves from both sides using undoMove """

    undo = record.deleteLast()
    if undo: undo.undo()


def mainMenuButton(): 
    global gameStarted
    gameStarted = False
     
def resetGameButton():  
    resetGame()

def playRecordButton():  
    global playingRecord,playState,playIndex,gameStarted
    record.load()
    gameStarted = True
    playingRecord = True
    playState = 1
    playIndex = 0
    resetGame()
    
def fastButton(): 
    global playSpeed 
    playSpeed -= (playSpeed/5)

def slowButton():  
    global playSpeed
    playSpeed += (playSpeed/5) + 1
     
def menuInRecordingButton():
    global playingRecord, gameStarted
    playingRecord = False
    gameStarted = False
    
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
        global playerIndexs
        self.started = True        
        moves = legal_moves()
        indexs = []
        for move in moves:
            changes = move.affectedSquares[:]
            firstindex = changes[0][0]
            secondindex = changes[1][0]
            try:
                secondindex = changes[2][0]
            except:
                pass
            indexs.append([firstindex,secondindex,move])
        playerIndexs = indexs
class ComputerPlayer(Player):
    def __init__(self,color,alpha,mini,nega):
        Player.__init__(self, color)
        self.alpha = alpha
        self.mini = mini
        self.nega = nega
    def startTurn(self):
        self.started = True
        doComputer(self.alpha,self.mini,self.nega)
        
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
        
    def draw(self):
        pygame.draw.rect(windowSurface, WHITE, (self.x , self.y , self.w, self.h))
        text = font2.render(self.text, True, RED)
        textRect = text.get_rect()
        textRect.centerx = self.x + (self.w/2)
        textRect.centery = self.y + (self.h/2)
        windowSurface.blit(text, textRect)
    
    def inside(self,x,y):
        """    """
        if x >= self.x and x < self.x+self.w and y >= self.y and y < self.y+self.h:
            return True
        return False

selectedIndex = None