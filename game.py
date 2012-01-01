## Authors: morghra94 and cracker64                                 ##
## ==========================SUMARY===============================  ##
## -> Checker's Game with an AI opponent                            ##
## -> Still very much in production                                 ##
## -> Compare the effectiveness of three heuristic search algorithms##
## namely the MiniMax, NegaScout, and Alpha-Beta                    ##
## ==========================DATES================================  ##
## -> Start: 11-5-11                                                ##
## -> Version 1: 11-6-11                                            ##
## -> Version 2: Pictures + Menu: 11-7-11                           ##
## -> Version 3: MiniMax added and refined 12-19-11 --> 12-23-11    ## 
## -> Version 4: Added comments, refined code for readability       ##
##    12-24-11                                                      ## 
## -> Version 5: Added recording and play back  --> 12-26-11        ##
## ==========================TODO=================================  ##
## Aesthetics:                                                      ##
##            => New Edge design for in game board                  ##
##            => Different colors and possibly graphics             ##
##            => New menu                                           ##
##            => More in game user feedback                         ##
##            => Standardized scoring/move piece notation           ##
## Artificial Intelligence:                                         ##
##            => Refine AlphaBeta and add NegaScout                 ##
##                 => Perfect*** move sorting                       ##
##            => Ability for the AI to play against itself          ##
## General:                                                         ##
##            => Compartmentalize the code completely               ##
##            => Add mandatory jump ** High priority **             ##
## ================================================================ ##

## ======== Imports ========= ##
import pygame
import sys
import pickle
import datetime
from pygame.locals import *
## ========================== ##

pygame.init() # Initializes pygame

mainClock = pygame.time.Clock() # Game clock: used for slowing down the AI opponent and tracks speed of functions

INFINITY = 99999999 # Constant used for the AI algorithms

## ======================================= Size of the window ====================================== ##
boardOffSetLeft_X = 300  # The extra space on the left - used for displaying information to the user
board_XRES = 1000    # Length of the board   
board_YRES = 1000    # Width of the board
## ================================================================================================= ##

## ================================== Window Surface ==================================== ##
windowSurface = pygame.display.set_mode((board_XRES + boardOffSetLeft_X, board_YRES), 0, 32)
pygame.display.set_caption('Checkers!')
## ====================================================================================== ##

## ============================= Fonts ================================= ##
font1 = pygame.font.SysFont(None, 60, bold = True, italic = True)
font2 = pygame.font.SysFont(None, 36)
## ===================================================================== ##

## ==== Initializes Colors ==== ##
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
ORANGE = (255, 128, 0)
## ============================ ##

## ======================================== Board Variables ============================================= ##
CELL_X = board_XRES / 8  # Length of a single checker square
CELL_Y = board_YRES / 8   # Height of a single checker square
## ====================================================================================================== ##
#   (black)
#            45  46  47  48
#          39  40  41  42
#            34  35  36  37
#          28  29  30  31
#            23  24  25  26
#          17  18  19  20
#            12  13  14  15
#          6   7   8   9
#   (red)
## ========= Piece constants based on BitMap ============= ##
OCCUPIED = 0
PIECE_BLACK = 1
PIECE_RED = 2
MAN = 4
KING = 8
FREE = 16

COLORS = PIECE_BLACK | PIECE_RED
TYPES = OCCUPIED | PIECE_BLACK | PIECE_RED | MAN | KING | FREE

BLACK_IDX = [-5,-6]
RED_IDX = [5,6]
KING_IDX = [-6,-5,5,6]
## ======================================================= ##


valid_squares = [6,7,8,9,12,13,14,15,17,18,19,20,23,24,25,26,
                     28,29,30,31,34,35,36,37,39,40,41,42,45,46,
                     47,48]
value = [0,0,0,0,0,1,256,0,0,16,4096,0,0,0,0,0,0]
edge = [6,7,8,9,15,17,26,28,37,39,45,46,47,48]
center = [18,19,24,25,29,30,35,36]
# values used to calculate tempo -- one for each square on board (0, 48)
row = [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,2,2,2,2,0,0,3,3,3,3,0,
           4,4,4,4,0,0,5,5,5,5,0,6,6,6,6,0,0,7,7,7,7]
safeedge = [9,15,39,45]

""" Maps compressed grid indices xi + yi * 8 to internal
        board indices """
pos = {}
pos[1] = 45;   pos[3]  = 46; pos[5] =  47; pos[7]  = 48
pos[8] = 39;   pos[10] = 40; pos[12] = 41; pos[14] = 42
pos[17] = 34;  pos[19] = 35; pos[21] = 36; pos[23] = 37
pos[24] = 28;  pos[26] = 29; pos[28] = 30; pos[30] = 31
pos[33] = 23;  pos[35] = 24; pos[37] = 25; pos[39] = 26
pos[40] = 17;  pos[42] = 18; pos[44] = 19; pos[46] = 20
pos[49] = 12;  pos[51] = 13; pos[53] = 14; pos[55] = 15
pos[56] = 6;   pos[58] = 7;  pos[60] =  8; pos[62] = 9

""" Maps internal board indices to grid (row, col) coordinates """
grd = {}
grd[6]  = (7,0); grd[7]  = (7,2); grd[8]  = (7,4); grd[9]  = (7,6)
grd[12] = (6,1); grd[13] = (6,3); grd[14] = (6,5); grd[15] = (6,7)
grd[17] = (5,0); grd[18] = (5,2); grd[19] = (5,4); grd[20] = (5,6)
grd[23] = (4,1); grd[24] = (4,3); grd[25] = (4,5); grd[26] = (4,7)
grd[28] = (3,0); grd[29] = (3,2); grd[30] = (3,4); grd[31] = (3,6)
grd[34] = (2,1); grd[35] = (2,3); grd[36] = (2,5); grd[37] = (2,7)
grd[39] = (1,0); grd[40] = (1,2); grd[41] = (1,4); grd[42] = (1,6)
grd[45] = (0,1); grd[46] = (0,3); grd[47] = (0,5); grd[48] = (0,7)

## ============================================================================================ ##

## ===================================================== State Variables =============================================================== ##
gameOver = False            # Determines if game is over
gameStarted = False         # Determines if game is started
playerWon = "Winner"        # Keeps track of the winner
whosTurn = PIECE_BLACK      # Turn feature
selectedPiece = None        # Shows if there is a piece selected
computerPlayer = False      # Makes the computer play
computerState = 0           # Used to see what the computer is doing - if it equals 1 it is a red piece, if it equals 2 it is a black piece
computerMove = None         # Assigns the best move to the computer that the computer will then do
computerTimer = 0           # Timer for the AI - used so that the computer is not super fast - makes it more playable 
moveList = []               # Stores lists of moves that the AI uses
playingRecord = False       # Determines if the recording is being played
playState = 0               # Used for going through the recorded game
playIndex = 0               # Same as above
awaitingSecondJump = False  # For double jump checking - making sure pieces are used correctly
playSpeed = 1000            # The standard speed for play back, 1 second per move
ALPHABETA = False           # Determines which AI algorithm is running
MINIMAX = False
NEGASCOUT = False
numevals = 0
forceJumpList = []
## ===================================================================================================================================== ##

## ========================== Loads Images ============================== ##
introImage = pygame.image.load('idontcare.png')           # Menu Picture
redPieceImage = pygame.image.load('redpiece.png')         # Red Piece
blackPieceImage = pygame.image.load('blackpiece.png')     # Black Piece
redKingImage = pygame.image.load('redpieceking.png')      # Red King
blackKingImage = pygame.image.load('blackpieceking.png')  # Black King
## ====================================================================== ##

## ================ Transforms Images to the cell size ============================================ ##
blackpieceStretched = pygame.transform.scale(blackPieceImage, (CELL_X, CELL_Y)) # Black piece
redpieceStretched = pygame.transform.scale(redPieceImage, (CELL_X, CELL_Y))     # Red piece
redKingStretched = pygame.transform.scale(redKingImage, (CELL_X, CELL_Y))       # Red king piece
blackKingStretched = pygame.transform.scale(blackKingImage, (CELL_X, CELL_Y))   # Black king piece
## ================================================================================================ ##

class move:   
    """ 
    
        Basic move structure as applied to the checkers board. 
        Takes moves and then evaluates them by calling doMove and undoMove.  
        
    """    
    def __init__(self, squares):        
        """ Constructor for the move class""" 
        self.affectedSquares = squares
        # affected squares is a list of changes, each change is in this format [index,source,dest]
        
    def do(self,real=False):        
        """ For doing moves """
        global whosTurn
        for idx,_,newval in self.affectedSquares:
            board[idx] = newval
        whosTurn ^= COLORS
        if real:
            record.add(self)
    def undo(self):
        """ For undoing moves """
        rev_move = move([[idx,dest,src] for idx,src,dest in self.affectedSquares])
        rev_move.do()

class recording:
    def __init__(self):
        self.moveList = []
    def add (self,move):
        self.moveList.append(move)
    def deleteLast (self):
        if len(self.moveList) > 0:
            return self.moveList.pop()
        print "idiot, no moves"
    def save (self):
        with  open(str(datetime.datetime.now()),'w') as f:
            pickle.dump(self.moveList,f)
    def load (self):
        with open("record.txt", 'r') as f:
            self.moveList = pickle.load(f)

record = recording()

def handleWin(isRed,redWon):
    if redWon:
        if isRed==PIECE_RED:
            return INFINITY/2
        else:
            return -INFINITY/2
    else:
        if isRed==PIECE_RED:
            return -INFINITY/2
        else:
            return INFINITY/2
           
def evalstate(who):#True for red, false for black
    global numevals
    value = 1
    value = board[value+6-who+who*7/value]+8
    value /= value*.08
    while value >-29:
        value += -2012
    return value

def miniMax(depth):   
    """ 
        
        The main miniMax algorithm, must enter the depth that you want 
        it to go to in the doComputer function, the depth entered 
        must be an odd number. 
        
    """
    global redTurn
    winCheck = checkPieces(whosTurn)
    if winCheck[0]:
        return handleWin(whosTurn,winCheck[1])
    if depth == 0:
        return evalstate(whosTurn),
    
    bestValue = INFINITY
    bestMove = None
    if redTurn:
        bestValue = -INFINITY
    moves = legal_moves()
    if len(moves)==0:   # No moves in the list
        if redTurn:
            return -INFINITY,
        return INFINITY,
    
    for move in moves:
        move.do()
        value = miniMax(depth-1)[0]
        move.undo()
        if redTurn:
            if value > bestValue:
                bestValue = value
                bestMove = move
        else:
            if value < bestValue:
                bestValue = value
                bestMove = move
    return bestValue, bestMove

def alphaBeta(depth, alpha, beta):    
    """ 
        
        The main miniMax algorithm, must enter the depth that you want 
        it to go to in the doComputer function, the depth entered 
        must be an odd number. 
    """
    
    winCheck = checkPieces(whosTurn)
    if winCheck[0]:
        return handleWin(whosTurn,winCheck[1]),
    if depth == 0:
        return evalstate(whosTurn),
    
    bestValue = -INFINITY
    localalpha = alpha
    bestMove = None
    moves = sort(legal_moves(),whosTurn)
    if len(moves)==0:   # No moves in the list
        if whosTurn==PIECE_RED:
            return -INFINITY,
        return INFINITY,    
    for move in moves:
        move.do()
        if depth > 1:
            value = -alphaBeta(depth-1,-beta,-localalpha)[0]
        else:
            value = alphaBeta(depth-1,-beta,-localalpha)[0]
        move.undo()
        
        if value > bestValue:
            bestValue = value
            bestMove = move
        
        if bestValue >= beta:
            break
        if bestValue > localalpha:
            localalpha = bestValue
    return bestValue, bestMove

def negaScout(maxDepth, currentDepth, alpha, beta):   
    """ 
        
        The main miniMax algorithm, must enter the depth that you want 
        it to go to in the doComputer function, the depth entered 
        must be an odd number. 
    """
    
    winCheck = checkPieces(whosTurn)
    if winCheck[0]:
        return handleWin(whosTurn,winCheck[1]),
    if currentDepth == maxDepth:
        return evalstate(whosTurn),  
    adaptiveBeta = beta
    bestMove = None
    bestValue = -INFINITY      
    moves = sort(legal_moves(),whosTurn)
    if len(moves)==0:   # No moves in the list
        if whosTurn==PIECE_RED:
            return -INFINITY,
        return INFINITY,    
    for move in moves:
        move.do()
        if currentDepth+1==maxDepth:
            currentScore = negaScout(maxDepth,currentDepth+1,-adaptiveBeta,-max(alpha,bestValue))[0]
        else:
            currentScore = -negaScout(maxDepth,currentDepth+1,-adaptiveBeta,-max(alpha,bestValue))[0]
        move.undo()
        if currentScore > bestValue:
            if adaptiveBeta == beta or currentDepth >= maxDepth-2:
                bestValue = currentScore
                bestMove = move
         
        if bestValue >= beta:
            break
        else:
            adaptiveBeta = max(alpha, bestValue)+1
    return bestValue, bestMove

def sort(moves,isRed):
    listToSort = []
    finalList = []
    for move in moves:
        #p = getPiece(move.source_X,move.source_Y)
        move.do()
        listToSort.append((evalstate(isRed),move))
        move.undo()
    isReddd = True if isRed==PIECE_RED else False
    newlist = sorted(listToSort,key=lambda blah:blah[0],reverse=isReddd)
    for keymoves in newlist:
        finalList.append(keymoves[1])
    return finalList

def resetBoard():  
    """ Redraw's the board, using the BitMap """
    global board
    #   (black)
    #            45  46  47  48
    #          39  40  41  42
    #            34  35  36  37
    #          28  29  30  31
    #            23  24  25  26
    #          17  18  19  20
    #            12  13  14  15
    #          6   7   8   9
    #   (red)
    board = [OCCUPIED for i in range(56)]
    s = board
    for i in range(0, 4):
            s[6+i] = s[12+i] = s[17+i] = PIECE_RED | MAN
            s[34+i] = s[39+i] = s[45+i] = PIECE_BLACK | MAN
            s[23+i] = s[28+i] = FREE  
resetBoard()

def resetGame():  
    """ Allow's the game to be reset"""   
    global gameOver,redTurn,computerPlayer
    gameOver = False
    redTurn = False
    resetBoard()    
  
def startmulti():   
    """ Multiplayer game mode start button. In the menu."""    
    global gameStarted
    if gameOver or computerPlayer:
        resetGame()
    gameStarted = True
    
def exitbutton(): 
    """ Button used to exit the game. In the menu.""" 
    pygame.quit()
    sys.exit()
    
def miniMaxButton():
    global MINIMAX, gameStarted, computerPlayer
    MINIMAX = True
    if gameOver or not computerPlayer:
        resetGame()
    computerPlayer = True
    gameStarted = True

def alphaBetaButton():  
    global ALPHABETA, gameStarted, computerPlayer
    ALPHABETA = True
    if gameOver or not computerPlayer:
        resetGame()
    computerPlayer = True
    gameStarted = True

def negaScoutButton():
    global gameStarted, computerPlayer, NEGASCOUT
    NEGASCOUT = True
    if gameOver or not computerPlayer:
        resetGame()
    computerPlayer = True
    gameStarted = True
    
def undoButton():
    """ Undoes moves from both sides using undoMove """
    record.deleteLast().undo()

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
    
buttonlist = [
              button(527,303,171,105,"Multi-Player",startmulti),
              button(527,600,171,105,"Exit",exitbutton),
              button(286,303,173,103,"Play-Back",playRecordButton),
              button(286, 450, 173, 105, "VS MiniMax", miniMaxButton),
              button(527, 450, 173, 105, "VS AlphaBeta", alphaBetaButton),
              button(286, 600, 173, 105, "VS NegaScout", negaScoutButton)   
              ]

inGameButtons = [
                 button(75, 200, 150,100,"Undo",undoButton),
                 button(75, 500, 150,100, "Main Menu", mainMenuButton),
                 button(75, 350, 150,100, "Reset Game", resetGameButton),
                 ]

playBackButtons = [
                   button(25, 300, 30, 30, ">>", fastButton),
                   button(150, 300, 30, 30, "<<", slowButton),
                   button(150, 600, 100, 100, "Menu", menuInRecordingButton),
                   ]

selectedIndex = None
   
def processClick(mousePos):
    """ 
    
        Overall click processing function, makes sure every move is legal.
        Utilizes getPiece and canMove functions 
        
    """
    global selectedIndex, redTurn, moveList, awaitingSecondJump
    x, y = mousePos
    if not gameStarted:
        for button in buttonlist:
            if button.inside(x,y):
                button.f()
        return
    for theButton in inGameButtons:
        if theButton.inside(x,y):
            theButton.f()
    for aButton in playBackButtons:
        if playingRecord and aButton.inside(x,y):
            aButton.f()
    if gameOver:
        return
    grid_X = ((x-boardOffSetLeft_X) / CELL_X)
    grid_Y = (y / CELL_Y)
    try:
        index = pos[grid_X + grid_Y*8]
    except:
        index = None
    #realPiece = getPiece(grid_X, grid_Y) # The coordinates of the piece is equal to realPiece
    if selectedIndex:
            currentMoves = legal_moves()#move somewhere where it is once per player turn, not click
            possibleIndexs = []
            realMove = None
            for move in currentMoves:
                values = move.affectedSquares[:]
                if values[0][0]==selectedIndex:
                    possibleIndexs.append(values[-1][0])
                    if values[-1][0]==index:
                        realMove = move
            if selectedIndex == index:
                if awaitingSecondJump:
                    endPlayerTurn()
                else:
                    selectedIndex = None
                return
            elif index and not awaitingSecondJump:
                if board[index]&whosTurn:# and index in currentMoves:
                    selectedIndex = index # The selected piece is now equal to realPiece
            if index in possibleIndexs:
                if realMove:
                    realMove.do(True)
                selectedIndex = None
                #add double jump check here OR fix possibleIndexs to include it
                endPlayerTurn()        
            return
    if index:
        if board[index]&whosTurn:# and index in currentMoves:
            selectedIndex = index
            
def endPlayerTurn():
    global selectedPiece,redTurn,awaitingSecondJump
    selectedIndex = None
    awaitingSecondJump = False
    if computerPlayer:
        doComputer()
        return
    checkPieces() 
    
def legal_moves():
    return getJumps() or getMoves()
    
def getEnemy():
    return whosTurn^COLORS
    
def getMoves():
    moves = []
    player = whosTurn
    valid_indices = RED_IDX if player == PIECE_RED else BLACK_IDX
    for i in valid_squares:
        for j in valid_indices:
            dest = i+j
            if (board[i]&player and board[i]&MAN and board[dest]&FREE):
                sq1 = [i,player|MAN,FREE]
                if ((player == PIECE_RED and i>=39) or (player == PIECE_BLACK and i<=15)):
                    sq2 = [dest,FREE,player|KING]
                else:
                    sq2 = [dest,FREE,player|MAN]
                moves.append(move([sq1,sq2]))
        for j in KING_IDX:
            dest = i+j
            if (board[i]&player and board[i]&KING and board[dest]&FREE):
                sq1 = [i,player|KING,FREE]
                sq2 = [dest,FREE,player|KING]
                moves.append(move([sq1,sq2]))
    return moves

def getJumps():
    jumps = []
    player = whosTurn
    enemy = getEnemy()
    valid_indices = RED_IDX if player == PIECE_RED else BLACK_IDX
    for i in valid_squares:
        if (board[i]&player and board[i]&MAN):
            for j in valid_indices:
                mid = i+j
                dest = i+j*2
                if (board[mid]&enemy and board[dest]&FREE):
                    sq1 = [i,player|MAN,FREE]
                    sq2 = [mid, board[mid], FREE]
                    if ((player == PIECE_RED and i>=34) or (player == PIECE_BLACK and i<=20)):
                        sq3 = [dest,FREE,player|KING]
                    else:
                        sq3 = [dest,FREE,player|MAN]
                    jump = [move([sq1,sq2,sq3])]
                    visited = set()
                    visited.add((i,mid,dest))
                    temp = board[i]
                    board[i] = FREE
                    extraJumps = getExtendedJumps(valid_indices, jump, captureMan, visited)
                    board[i] = temp
                    jumps.extend(extraJumps)
        if (board[i]&player and board[i]&KING):
            for j in KING_IDX:
                mid = i+j
                dest = i+j*2
                if (board[mid]&enemy and board[dest]&FREE):
                    sq1 = [i,player|KING,FREE]
                    sq2 = [mid,board[mid],FREE]
                    sq3 = [dest,board[dest],player|KING]
                    jump = [move([sq1,sq2,sq3])]
                    visited = set()
                    visited.add((i,mid,dest))
                    temp = board[i]
                    board[i] = FREE
                    extraJumps = getExtendedJumps(valid_indices, jump, captureKing, visited)
                    board[i] = temp
                    jumps.extend(extraJumps)
    return jumps

def getExtendedJumps(valid_moves, captures, add_sq_func, visited):
    player = whosTurn
    enemy = getEnemy()
    finalJumps = []
    while captures:
        c = captures.pop()
        newJumps = []
        for j in valid_moves:
            capture = c.affectedSquares[:]
            last_pos = capture[-1][0]
            mid = last_pos + j
            dest = last_pos + j*2
            if ((last_pos,mid,dest) not in visited and (dest,mid,last_pos) not in visited and board[mid]&enemy and board[dest]&FREE):
                sq2, sq3 = add_sq_func(player,mid,dest,last_pos)
                capture[-1][2] = FREE
                capture.extend([sq2,sq3])
                visited.add((last_pos,mid,dest))
                newJumps.append(move(capture))
        if newJumps:
            captures.extend(newJumps)
        else:
            finalJumps.append(move(capture))
    return finalJumps
                

def captureMan(player,mid,dest,last_pos):
    sq2 = [mid,board[mid],FREE]
    if ((player == PIECE_RED and last_pos>=34) or (player == PIECE_BLACK and last_pos<=20)):
        sq3 = [dest,FREE,player|KING]      
    else:
        sq3 = [dest,FREE,player|MAN] 
    return sq2,sq3

def captureKing(player,mid,dest,last_pos):
    sq2 = [mid,board[mid],FREE]
    sq3 = [dest,board[dest],player|KING] 
    return sq2,sq3

def perft(depth):
    if depth == 0:
        return 1
    nodes = 0
    for move in legal_moves():
        move.do()
        nodes += perft(depth-1)
        move.undo()
    return nodes

def perftest():
    mainClock.tick()
    #movee = move(1,6,2,5, diff_X = 1 , diff_Y = -1)
    #for i in range(0,1000000):
    #    movee.do()
    #    movee.undo()
    #print "1million do and undo took:", mainClock.tick()   
    for depth in range (1,8):
        print "Depth:",depth,"count:",perft(depth),"Time:",mainClock.tick()
#Uncomment for performance test!
#perftest()
      
def doComputer():
    """ Activates the computer Player """
    global selectedPiece, computerState,computerMove, redTurn,numevals
    mainClock.tick()
    if ALPHABETA:
        bestMove = alphaBeta(9,-INFINITY,INFINITY)[1]
    elif MINIMAX:
        bestMove = miniMax(5)[1] 
    else:
        bestMove = negaScout(9, 1, -INFINITY, INFINITY)[1]
    print "Count:",numevals,"Time:",mainClock.tick()
    numevals = 0
    redTurn = not redTurn
    if bestMove != None:
        computerMove = bestMove
        computerState = 1
    else: print "whaaaat"
                 
def drawBoard(): 
    """ Draw's the checker board and the indicator for selection over a selected piece """
    color = RED
    for y in range(0, 8):
        for x in range(0, 8):
            if x % 2 == y % 2:
                color = RED
            else:
                color = BLACK
                if selectedIndex and grd[selectedIndex] == (y,x):
                    color = ORANGE
            pygame.draw.rect(windowSurface, color, ((x * CELL_X)+boardOffSetLeft_X, y * CELL_Y, x + CELL_X, y + CELL_Y)) 
       
def getPicforSquare(s):
    if s&PIECE_RED:
        if s&KING:
            return redKingStretched
        return redpieceStretched
    if s&KING:
        return blackKingStretched
    return blackpieceStretched
def drawPieces():
    """ Draw's the pieces onto the board """ 
    for i in valid_squares:
        s = board[i]
        if s&COLORS:
            y,x = grd[i]
            screen_X = ((x) * CELL_X) + boardOffSetLeft_X
            screen_Y = (y) * CELL_Y
            windowSurface.blit(getPicforSquare(s), (screen_X, screen_Y, screen_X + CELL_X, screen_Y + CELL_Y))
        
def drawMenu():
    """ Draw's a menu picture """
    windowSurface.blit(introImage,(0, 0, board_XRES + boardOffSetLeft_X, board_YRES))
    for button in buttonlist:
        button.draw()
        
def drawInGameButtons():
    for button in inGameButtons:
        button.draw()
    
def drawPlayBackButtons():
    for button in playBackButtons:
        button.draw()
    
def eventCheck(event):
    """ Checks for input from user. If mouse button is clicked utilizes processClick function. """   
    global gameOver,gameStarted
    if event.type == MOUSEBUTTONDOWN:
        processClick(event.pos)
    if event.type == KEYDOWN:
        if event.key == 114:
            resetGame()
        if event.key == 27:
            gameStarted = False

def checkPieces(color=None):
    """ 
    
        Checks for various attributes of pieces after each move 
        Also Checks for winners and determines the winner or if there is a tie.
        
    """
    global gameOver, playerWon, whosTurn
    redCanMove = False
    blackCanMove = False
    if legal_moves():
        print whosTurn,"has moves!"
        if whosTurn == PIECE_RED:
            redCanMove = True
        else:
            blackCanMove = True
    whosTurn ^= COLORS
    if legal_moves():
        print whosTurn,"has moves!"
        if whosTurn == PIECE_RED:
            redCanMove = True
        else:
            blackCanMove = True
    whosTurn ^= COLORS
    if redCanMove and not blackCanMove and whosTurn != PIECE_RED:
        gameOver = True
        playerWon = "Red"
    elif blackCanMove and not redCanMove and (whosTurn==PIECE_RED or computerPlayer):
        gameOver = True
        playerWon = "Black"
    elif not blackCanMove and not redCanMove:
        gameOver = True
        playerWon = "Tie"
    if color != None:
        print gameOver,redCanMove,blackCanMove
        winnerFound = gameOver
        currentPlayerWon = False
        gameOver = False
        if winnerFound:
            if playerWon == "Tie":
                currentPlayerWon = True
            elif color == PIECE_RED and playerWon == "Red":
                currentPlayerWon = True
            elif color == PIECE_BLACK and playerWon == "Black":
                currentPlayerWon = True
        return winnerFound, currentPlayerWon
    if gameOver:
        record.save()  # Saves game into a file
            
                        
def drawtext():
    """ Draw's the text for who's turn it is, the FPS, and display's the winner of the game """
    if gameOver:
        text = font1.render(playerWon + " has won the game", True, WHITE)
        textRect = text.get_rect()
        textRect.centerx = windowSurface.get_rect().centerx
        textRect.centery = windowSurface.get_rect().centery
        windowSurface.blit(text, textRect)
        return
    player = "Red"
    text_X = boardOffSetLeft_X/2
    text_Y = board_YRES - 40
    if not redTurn:
        player = "Black"
        text_Y = 40
    text = font2.render("It is " + player + "'s turn", True, WHITE)
    textRect = text.get_rect()
    textRect.centerx = text_X
    textRect.centery = text_Y
    windowSurface.blit(text, textRect)
    text = font2.render("FPS: " + repr(int(mainClock.get_fps())), True, WHITE)
    textRect = text.get_rect()
    textRect.centerx = boardOffSetLeft_X/2
    textRect.centery = 800
    windowSurface.blit(text, textRect)

def updateComp():
    """ Slows the computer down so that is not super fast - increases playability """
    global selectedPiece, computerMove, computerTimer, redTurn, computerState
    if computerState > 0 and not gameOver:
        computerTimer += mainClock.get_time()
        if computerState == 1:
            if computerTimer >= 1000:
                computerMove.do(True)
                computerState = 2
                computerTimer = 0
        if computerState == 2:
            if computerTimer >= 500:
                selectedPiece = None
                computerTimer = 0
                computerMove = None
                computerState = 0
                redTurn = False
                checkPieces() 

def updateRecord():
    """ Is responsible for playing back the recorded list """
    global selectedPiece, playState,playIndex,playingRecord,computerTimer, fast
    if playState > 0 and not gameOver:
        computerTimer += mainClock.get_time()
        if playState == 1:
            selectedPiece = getPiece(record.moveList[playIndex].source_X,record.moveList[playIndex].source_Y)
            playState = 2   
        if playState == 2:
            if computerTimer >= playSpeed:
                record.moveList[playIndex].do()
                playState = 3
                computerTimer = 0
                playIndex += 1
        if playState == 3:
            if computerTimer >= (playSpeed/2):
                selectedPiece = None
                computerTimer = 0
                playState = 1
                checkPieces()   
                    
def updateGame():
    """ 
    
        All functions that update the game are encapsulated here. 
        Starts updated when game starts or show's the menu on startup
        
    """
    mainClock.tick()
    if playingRecord:
        updateRecord()
    if gameStarted and not playingRecord:
        updateComp()
        drawInGameButtons()
        drawBoard()
        drawPieces()
        drawtext()
    elif playingRecord:
        drawPlayBackButtons()
        drawBoard()
        drawPieces()
        drawtext()
    else:
        drawMenu()
 
## ============ Main Game Loop ============= ##
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        eventCheck(event)
    windowSurface.fill(BLACK)
    updateGame()
    pygame.display.update()
            
            
            
            

