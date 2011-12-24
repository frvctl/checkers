## Written by: Ben Vest and Philip Briley                           ##
## ==========================SUMARY===============================  ##
## -> Checker's Game with an AI opponent                            ##
## -> Still very much in production                                 ##
## -> Compare the effectivness of three heuristic search algorithms ##
## namely the Minimax, NegaScout, and Alpha-Beta                    ##
## ==========================DATES================================  ##
## -> Start: 11-5-11                                                ##
## -> Version 1: 11-6-11                                            ##
## -> Version 2: Pictures + Menu: 11-7-11                           ##
## -> Version 3: MiniMax added and refined 12-19-11 -->             ##
## ==========================TODO=================================  ##
## -> Need to write Minimax, NegaScout,and Alpha-Beta Algorithms.   ##
## -> Rewrite code so its better, more efficient, more OOP          ##
## -> Create a better GUI for the menu and in game playing          ##
## -> Make it play against itself                                   ##
## -> Have a way to record statistics from the game                 ##
## -> Compartmentalize the code into different files                ##
 
import pygame, sys
from pygame.locals import *

pygame.init()

mainClock = pygame.time.Clock()

INFINITY = 99999999

## Size of the window ##
boardOffSet_X = 400
board_XRES = 1000
board_YRES = 1000

windowSurface = pygame.display.set_mode((board_XRES + boardOffSet_X, board_YRES), 0, 32)
pygame.display.set_caption('Checkers!')

font1 = pygame.font.SysFont(None, 60, bold = True, italic = True)
font2 = pygame.font.SysFont(None, 36)

## Initializes Colors ##
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
ORANGE = (255, 128, 0)

## Board Variables ##
board_X = 10                        # horizontal size of the BitMap
board_Y = 10                        # vertical size of the BitMap
realBoard_X = 8                     # Real size of the BitMap, horizontally, excluding the border (9's)
realBoard_Y = 8                     # Real size of the BitMap, vertically, excluding the border(9's)
CELL_X = board_XRES / realBoard_X   # Length of a single checker square
CELL_Y = board_YRES / realBoard_Y   # Height of a single checker square

## Piece constants based on BitMap ##
PIECE_EMPTY = 0     # Nothing drawn onto board
PIECE_RED = 1       # Red Piece
PIECE_BLACK = 2     # Black Piece
PIECE_VOID = 9      # No piece drawn -- Border of BitMap

## =================================== Move Lists ============================================= ##
## Each tuple represents a move that the pieces are allowed to make. Up and down                ##
## is relative to looking at the board from the bottom, where the red pieces are, as up         ##
## and the top of the board with black pieces being forward.                                    ##
## ============================================================================================ ##
## (2, 2) = Jump back right;         (2, -2) = Jump back left;                                  ##
## (-2, -2) = Jump forward left;     (-2, 2) = Jump forward right;                              ##
## (1, 1) = back right;              (1, -1) = Back left;                                       ##
## (-1, -1) = forward left;          (-1, 1) = Forward right;                                   ##
## ============================================================================================ ##
## The numbers represent the difference of the pieces initial coordinates on the BitMap         ##
## - as in a set of numbers such as 7, 4; 7 being the Y coordinate and 3 being the X coordinate ##
## - and the pieces new coordinates. Thus if the piece moves from 7, 4 to 6, 5                  ##
## - a perfectly legal move - it would return (-1, 1) which indicates Forward right             ##
## ============================================================================================ ##
possibleMoves = [(2,2),(2,-2),(-2,-2),(-2,2),(1,1),(1,-1),(-1,1),(-1,-1)] # All possible moves
movesWithoutJumps = [(1,1),(1,-1),(-1,-1),(-1,1)]                         # Moves without jumps
## ============================================================================================ ##

## ======================= State Variables ======================== ##
gameOver = False        # Determines if game is over
gameStarted = False     # Determines if game is started
playerWon = "Winner"    # Keeps track of the winner
redTurn = False         # Turn feature
selectedPiece = None    # Shows if there is a piece selected
computerPlayer = False  # Makes the computer play
computerstate = 0
computermove = None
computerTimer = 0
moveList = []           # Stores lists of moves that the AI uses
## ================================================================ ##

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

## ===================================================================== ##
## Controls most aspects that have to do with the pieces on the          ##
## board. Including displaying pieces, determining if movement is legal, ##
## aspects of the AI allowing it to do and undo moves, and the evaluate  ##
## function                                                              ##
## ===================================================================== ##
class piece:
    """ Everything to do with pieces is here in this class """
    def __init__(self, x, y, red, king=False):
        """ Constructor for the piece class. """
        self.x = x                  # X-Coordinates
        self.y = y                  # Y-Coordinates
        self.king = king            # King pieces
        self.red = red              # Red pieces    
        self.killed = False         # If a piece is killed it means that it has been jumped over
        self.notReallyDead = False  # If a piece is notReallyDead it is one which has been jumped by the computer but undone later in the game 
        self.justJumped = 0         # Pieces that have been jumped on the previous move
        if red:
            self.color = PIECE_RED
            self.otherColor = PIECE_BLACK
        else:
            self.color = PIECE_BLACK
            self.otherColor = PIECE_RED
        
        
    def getPiecePic(self):
        """ Handles the pictures of pieces """
        if self.red:
            if self.king:
                return redKingStretched
            return redpieceStretched
        else:
            if self.king:
                return blackKingStretched
            return blackpieceStretched
        
    def canMove(self, diff_X, diff_Y):
        """ Determines if a piece can move. Kings can move forward and backward. 
            Red pieces can move forward only. Black pieces can move backward only."""
        if abs(diff_X) != abs(diff_Y) or abs(diff_X) > 2 or abs(diff_Y) > 2:    
            return False,                                                   
        temp_X = self.x  # X Coordinate after a move
        temp_Y = self.y  # Y Coordinate after a move
        if diff_Y < 0 and not self.red and not self.king:    
            return False,
        if diff_Y > 0 and self.red and not self.king:    
            return False,
        temp_Y += diff_Y   
        temp_X += diff_X   
        if board[temp_Y][temp_X] == 0:      # If true the other pieces color is red
            unit_X = diff_X / abs(diff_X)   # Turns the X coordinate into a 1 or -1 
            unit_Y = diff_Y / abs(diff_Y)
            if abs(diff_X) > 1:
                if board[temp_Y - unit_Y][temp_X - unit_X] == self.otherColor:  # If diff_X is greater than one and is a black piece it is a valid jump
                    return True, temp_X, temp_Y, True                                       # Returns True (it can move) - temp_X and temp_Y (the coordinates after the move) - and True (since it is a jump move)
                else:                                                                       # Else the above falls through - returns False (it cannot move) 
                    return False,                                                           # returns False (it cannot move)  
            return True, temp_X, temp_Y, False                                              # Applies the first if - assuming all else falls through - returns True (it can move) - temp_X and temp_Y (the coordinates after the move) - and True (it is not a jump)
        return False,                                                                       # Assuming none of the above apply returns False (it cannot move) 
    
    def doMove(self, x, y, notReallyDead = False):
        """ Does a move no matter what, Can be temporary for computer checks """
        board[self.y][self.x] = PIECE_EMPTY         # It just moved from here, so it's now empty
        diff_X = x - self.x                         # Where it is moving, for jump checking
        diff_Y = y - self.y                         # ^
        self.x = x                                  # Set the piece location to the new x,y
        self.y = y                                  # ^
        board[y][x] = self.color                    # Set the new board location
        if abs(diff_X)==2:                          # If it jumped something
            jump_X = x - (diff_X / abs(diff_X))
            jump_Y = y - (diff_Y / abs(diff_Y))
            board[jump_Y][jump_X] = PIECE_EMPTY
            killedPiece = getPiece(jump_X, jump_Y, forceColor = self.otherColor)
            if killedPiece == None:
                print "WTF do",jump_X,jump_Y,self.otherColor
                return
            if notReallyDead:
                self.justJumped += 1
                killedPiece.notReallyDead = True
                return
            killedPiece.killed = True
            
    def undoMove(self,x,y, notReallyDead = False):
        """ Same as doMove, except replaces any piece it jumped """
        board[self.y][self.x] = PIECE_EMPTY
        diff_X = x - self.x
        diff_Y = y - self.y
        self.x = x
        self.y = y
        board[y][x] = self.color
        if abs(diff_X)==2: #did it jump something
            jump_X = x - (diff_X/2)
            jump_Y = y - (diff_Y/2)
            board[jump_Y][jump_X] = self.otherColor
            killedPiece = getPiece(jump_X, jump_Y, notReallyDead, forceColor = self.otherColor)
            if notReallyDead:
                self.justJumped -= 1
                if killedPiece == None:
                    temp = getPiece(jump_X, jump_Y, notReallyDead)
                    if temp!=None:
                        print temp.color
                    print "WTF undo",x,y,diff_X,diff_Y,self.otherColor
                else:
                    killedPiece.notReallyDead = False
                return
            killedPiece.killed = False
    
    def canMoveAnywhere(self):
        """ Checks all around the piece in every direction to determine if movement is possible """
        
        for check_X,check_Y in possibleMoves:
            if self.x + check_X > realBoard_X or self.x + check_X < 1 or self.y + check_Y > realBoard_Y or self.y + check_Y < 1:
                continue
            checkMove = self.canMove(check_X, check_Y)
            if checkMove[0]:
                return True
        return False
    
    def makeMoveList(self):
        """ Creates a list of moves for the AI through doMove and undoMove) to use """
        list_of_moves = []
        for check_X,check_Y in possibleMoves:
            if self.x + check_X > realBoard_X or self.x + check_X < 1 or self.y + check_Y > realBoard_Y or self.y + check_Y < 1:
                continue
            checkMove = self.canMove(check_X, check_Y)
            if checkMove[0]:
                others = []
                tempList = []
                flag = checkMove[3]
                last_X = check_X
                last_Y = check_Y
                count = 0
                while flag and count < 5:
                    count += 1
                    foundJump = False
                    tempList.append([self.x,self.y])  #store pieces current position
                    self.doMove(self.x + last_X, self.y + last_Y, True)  # move it to new position
                    for next_X,next_Y in possibleMoves:
                        if self.x + next_X > realBoard_X or self.x + next_X < 1 or self.y + next_Y > realBoard_Y or self.y + next_Y < 1:
                            continue
                        checkMove = self.canMove(next_X, next_Y)
                        if checkMove[0] and checkMove[3]:
                            last_X = next_X
                            last_Y = next_Y
                            others.append((self.x + next_X, self.y + next_Y))
                            foundJump = True
                    flag = foundJump
                    
                while len(tempList)>0: # go through stored positions and undo
                    undo_X, undo_Y = tempList.pop()
                    self.undoMove(undo_X,undo_Y,True)
                list_of_moves.append(move(self.x, self.y, self.x + check_X, self.y + check_Y, others))
        return list_of_moves
    
    def evaluate(self):
        """ Evaluates the current piece's position"""
        num = 0
        if self.canMoveAnywhere():
            num += 1
        else:
            num -= 5
            
        num += 15*self.justJumped
        
        if not self.king:
            num += vBoard[self.y][self.x]
            if self.y == 1:
                num += 10
        if self.king:
            num += 1
        for i in range(0,len(movesWithoutJumps)):
            near_X, near_Y = movesWithoutJumps[i]
            if board[self.y + near_Y][self.x + near_X] == self.otherColor:
                next_X, next_Y = movesWithoutJumps[i-2]
                if board[self.y + next_Y][self.x + next_X] == PIECE_EMPTY:
                    num -= 13
                 
        if not self.red:
            num = -num
        return num

## ========================================================================= ##        
## End of the piece class                                                    ##
## ========================================================================= ##   
    
class move:
    def __init__(self, source_X, source_Y, dest_X, dest_Y, *others):
        self.source_X = source_X
        self.source_Y = source_Y
        self.dest_X = dest_X
        self.dest_Y = dest_Y
        self.others = others
        if len(others) > 0:
            self.others = others[0]
    def do(self, notReallyDead = False):
        p = getPiece(self.source_X, self.source_Y)
        p.doMove(self.dest_X,self.dest_Y, notReallyDead)
        for other in self.others:
            #print self.others
            if len(other) > 1:
                p.doMove(other[0], other[1], notReallyDead)
            
    def undo(self,fake = False):
        p = None
        if len(self.others)>0:
            #print self.others
            other = self.others[-1]
            if len(other) > 1:
                p = getPiece(other[0],other[1])
                for i in range(1,len(self.others)):
                    other = self.others[-i-1]
                    if len(other) > 1:
                        p.undoMove(other[0],other[1],fake)
                p.undoMove(self.dest_X,self.dest_Y,fake) 
        else:
            p = getPiece(self.dest_X,self.dest_Y)
        
        
        p.undoMove(self.source_X, self.source_Y,fake)

## ========================================================================= ##        
## End of the move class                                                     ##
## ========================================================================= ##
    
def miniMax(p,depth):
    if depth == 0:
        return p.evaluate(),
    bestValue = INFINITY
    bestMove = None
    if p.red:
        bestValue = -INFINITY
    moves = p.makeMoveList()
    if len(moves)==0:
        if p.red:
            return -INFINITY,
        return INFINITY,
    
    for move in moves:
        move.do(True)
        value = miniMax(p,depth-1)[0]
        move.undo(True)
        if p.red:
            if value > bestValue:
                bestValue = value
                bestMove = move
        else:
            if value < bestValue:
                bestValue = value
                bestMove = move
    return bestValue, bestMove

def miniMax2(depth):
    allMoves = []
    realBestMove = None
    realBestValue = -INFINITY
    for p in pieces:
        if p.red and not p.killed:
            #do red moves
            moves = p.makeMoveList()
            movecounter = 0
            perMove = []
            perMoveValue = []
            for move in moves:
                tempDepth = depth
                otherMoves = []
                move.do(True)
                perMoveValue.append(0) 
                perMove.append(0)
                perMoveValue[movecounter] = miniMax(p,0)[0]
                #check depth moves...
                while tempDepth > 1:
                    perDepth = []
                    bestValue = -INFINITY
                    if tempDepth%2==1: #black
                        bestValue = INFINITY
                    bestMove = None
                    for p2 in pieces:
                        if not p2.killed and not p2.notReallyDead and p2.red == (tempDepth%2==0):#start with black
                            #print tempDepth
                            perDepth.append((miniMax(p2,1),p2.color))
                    #print bestvalues2
                    for blah in perDepth:
                        blah2 = blah[0]
                        if blah[1] == PIECE_RED and blah2[0] > bestValue:#red
                            bestValue = blah2[0]
                            bestMove = blah2[1]
                        elif blah[1] == PIECE_BLACK and blah2[0] < bestValue:#black
                            bestValue = blah2[0]
                            bestMove = blah2[1]
                            
                    perMove[movecounter] = (bestValue,move)
                    perMoveValue[movecounter] += bestValue
                    if bestMove != None:
                        bestMove.do(True)
                        otherMoves.append(bestMove)
                    tempDepth -= 1
                while len(otherMoves) > 0:
                    otherMoves.pop().undo(True)
                move.undo(True)
                movecounter += 1
            #end of moves
            bestValue = -INFINITY
            bestIndex = -1
            for i in range(movecounter):
                value = perMoveValue[i]
                if value > bestValue:#red
                    bestValue = value
                    bestIndex = i
            if bestIndex != -1:
                allMoves.append((bestValue,perMove[bestIndex][1]))
                
                
    #end of pieces
            
    #print realValues
    for value in allMoves:
        if value[0] > realBestValue:
            realBestValue = value[0]
            realBestMove = value[1]
            
    #print realBestValue
    return realBestMove
            #return best move back to doComputer()
            

        

def resetBoard():
    """ Redraw's the board, using the BitMap """
    global board
    board = [                        ## 1 is red piece, 2 is black piece, 9 is the border, this is the BitMap 
            [9,9,9,9,9,9,9,9,9,9],
            [9,0,2,0,2,0,2,0,2,9],
            [9,2,0,2,0,2,0,2,0,9],
            [9,0,2,0,2,0,2,0,2,9],
            [9,0,0,0,0,0,0,0,0,9],
            [9,0,0,0,0,0,0,0,0,9],
            [9,1,0,1,0,1,0,1,0,9],
            [9,0,1,0,1,0,1,0,1,9],
            [9,1,0,1,0,1,0,1,0,9],
            [9,9,9,9,9,9,9,9,9,9]
            ]
resetBoard()

def valueAssign():
    """ Value assignments for the various board positions """
    global vBoard
    vBoard =  [
              [9,9,9,9,9,9,9,9,9,9],
              [9,0,2,0,2,0,2,0,2,9],
              [9,2,0,2,0,2,0,2,0,9],
              [9,0,1,0,1,0,1,0,2,9],
              [9,2,0,1,0,1,0,1,0,9],
              [9,0,1,0,1,0,1,0,2,9],
              [9,2,0,1,0,1,0,1,0,9],
              [9,0,0,0,0,0,0,0,1,9],
              [9,2,0,2,0,2,0,2,0,9],
              [9,9,9,9,9,9,9,9,9,9]
              ]
valueAssign()

def resetPieces():
    """ Resets the piece array to the board """
    global pieces, selectedPiece
    selectedPiece = None
    pieces = []
    for x in range(0, board_X):
        for y in range(0, board_Y):
            boardcheck = board[y][x]
            if boardcheck == PIECE_BLACK:
                pieces.append(piece(x, y, False))
            elif boardcheck == PIECE_RED:
                pieces.append(piece(x, y, True))
resetPieces() 
def resetGame():
    """ Allow's the game to be reset"""
    global gameOver,redTurn,computerPlayer
    gameOver = False
    redTurn = False
    computerPlayer = False
    resetBoard()
    resetPieces()      
          
def getPiece(x, y, checkfake = False , forceColor = None):
    """ Determines which pieces are on the board and where they are """
    for p in pieces:
        if p.x == x and p.y == y:      
            if not p.killed and (not p.notReallyDead or checkfake):  
                if forceColor == None or forceColor == p.color:  
                    return p
    return None

def startsolo():
    """ Solo game start button, against an AI Opponent. In the menu. """
    global computerPlayer, gameStarted
    if gameOver or not computerPlayer:
        resetGame()
    computerPlayer = True
    gameStarted = True
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
def undobutton():
    global moveList
    if len(moveList) <= 0:
        print "idiot"
        return
    lastmove = moveList.pop()
    lastmove.undo()

class button:
    """ Used for the menu """
    def __init__(self,x,y,w,h,f):
        """ Constructor for button class """
        self.x = x  # X-coord for the button's box
        self.y = y  # Y=coord for the button's box
        self.w = w  # Width of the button's box
        self.h = h  # Height of the button's box
        self.f = f  # Name on the button
    def inside(self,x,y):
        """    """
        if x >= self.x and x < self.x+self.w and y >= self.y and y < self.y+self.h:
            return True
        return False
    
buttonlist = [button(286,355,173,103,startsolo),button(527,353,171,105,startmulti),button(405,695,181,82,exitbutton)]
undobutton = button(0,0,boardOffSet_X,board_YRES,undobutton)
   
def processClick(pos):
    """ Overall click procesing function, makes sure every move is legal
        === Utilizes getpiece and canmove functions """
    global selectedPiece, redTurn, moveList
    x, y = pos
    if not gameStarted:
        for button in buttonlist:
            if button.inside(x,y):
                button.f()
        return
    if undobutton.inside(x,y):
        undobutton.f()
    if gameOver:
        return

    gridx = ((x-boardOffSet_X) / CELL_X) + 1
    gridy = (y / CELL_Y) + 1
    realPiece = getPiece(gridx, gridy) # The coordinates of the piece is equal to realPiece
    #print board[gridy][gridx]
    #for p in pieces:
    #    if p.x == gridx and p.y == gridy:
    #        print p.color,"killed:",p.killed,"fakedead:",p.notReallyDead
    if selectedPiece != None:
            if selectedPiece.x == gridx and selectedPiece.y == gridy:
                selectedPiece = None
                return
            elif realPiece != None:
                if redTurn == realPiece.red:
                    selectedPiece = realPiece # The selected piece is now equal to realPiece 
            canmove = selectedPiece.canMove((gridx) - (selectedPiece.x), (gridy) - (selectedPiece.y))
            if canmove[0]:
                cx = canmove[1]
                cy = canmove[2]
                #moveList.append(move(selectedPiece.x,selectedPiece.y,cx,cy))
                selectedPiece.doMove(cx,cy)
                
                if canmove[3]:
                    #check if it can jump again... four directions to check...
                    for checkx in [2, -2]:
                        for checky in [2, -2]:
                            if cx + checkx > realBoard_X or cx + checkx < 1 or cy + checky > realBoard_Y or cy + checky < 1:
                                continue
                            canmove = selectedPiece.canMove(checkx, checky)
                            if canmove[0] and canmove[3]:
                                return
                            
                selectedPiece = None
                checkPieces()
                if computerPlayer:
                    #doComputer()
                    doComputer2()
                    return
                redTurn = not redTurn                         
                
            return
    if realPiece != None:
        if redTurn == realPiece.red:
            selectedPiece = realPiece
       
def doComputer():
    bestvalues = []
    bestvalue = -INFINITY
    realbestmove = None
    for p in pieces:
        if not p.killed and p.red:
            bestvalues.append(miniMax(p,1))
    for blah in bestvalues:
        if blah[0] > bestvalue:
            bestvalue = blah[0]
            realbestmove = blah[1]
    if realbestmove != None:
        realbestmove.do()
    checkPieces()
    
def doComputer2():
    global selectedPiece, computerstate,computermove, redTurn
    bestmove = miniMax2(5)
    #bestmove.do()
    bestPiece = getPiece(bestmove.source_X,bestmove.source_Y)
    computermove = bestmove
    selectedPiece = bestPiece
    computerstate = 1
    redTurn = True
                 
def drawBoard():
    """ Draw's the checker board and the indicator for selection over a selected piece """
    color = RED
    for y in range(0, 8):
        for x in range(0, 8):
            if x % 2 == y % 2:
                color = RED
            else:
                color = BLACK
                if selectedPiece != None and selectedPiece.x - 1 == x and selectedPiece.y - 1 == y:
                    color = ORANGE
            pygame.draw.rect(windowSurface, color, ((x * CELL_X)+boardOffSet_X, y * CELL_Y, x + CELL_X, y + CELL_Y)) 
       
def drawPieces():
    """ Draw's the pieces onto the board """ 
    for p in pieces:
        if p.killed:
            continue
        screenx = ((p.x - 1) * CELL_X) + boardOffSet_X
        screeny = (p.y - 1) * CELL_Y
        windowSurface.blit(p.getPiecePic(), (screenx, screeny, screenx + CELL_X, screeny + CELL_Y))
        
def drawMenu():
    """ Draw's a menu picture """
    windowSurface.blit(introImage,(0, 0, board_XRES + boardOffSet_X, board_YRES))
    
def eventCheck(event):
    """ Checks for input from user.
        === If mousebutton is clicked utilizes processClick function
        === If r is pressed resets the game
        === If escape is pressed exits the game and returns user to menu """
    global gameOver,gameStarted
    if event.type == MOUSEBUTTONDOWN:
        processClick(event.pos)
    if event.type == KEYDOWN:
        if event.key == 114:
            resetGame()
        if event.key == 27:
            gameStarted = False

def checkPieces():
    """ Checks for various attributes of pieces after each move 
        Also Checks for winners and determines the winner or if there is a tie."""
    global pieces, gameOver, playerWon
    redcanmove = False
    blackcanmove = False
    for p in pieces:
        if p.killed:
            continue
        if p.red:
            if p.y == 1:
                p.king = True
            if not redcanmove:
                redcanmove = p.canMoveAnywhere()
        else:
            if p.y == 8:
                p.king = True
            if not blackcanmove:
                blackcanmove = p.canMoveAnywhere()
    if redcanmove and not blackcanmove and not redTurn:
        gameOver = True
        playerWon = "Red"
    elif blackcanmove and not redcanmove and (redTurn or computerPlayer):
        gameOver = True
        playerWon = "Black"
    elif not blackcanmove and not redcanmove:
        gameOver = True
        playerWon = "Tie"
                        
def drawtext():
    """ Draw's the text for who's turn it is and display's the winner of the game """
    if gameOver:
        text = font1.render(playerWon + " has won the game", True, WHITE)
        textRect = text.get_rect()
        textRect.centerx = windowSurface.get_rect().centerx
        textRect.centery = windowSurface.get_rect().centery
        windowSurface.blit(text, textRect)
        return
    player = "Red"
    textx = boardOffSet_X/2
    texty = board_YRES - 40
    if not redTurn:
        player = "Black"
        texty = 40
    text = font2.render("It is " + player + "'s turn", True, WHITE)
    textRect = text.get_rect()
    textRect.centerx = textx
    textRect.centery = texty
    windowSurface.blit(text, textRect)
    
    text = font2.render("FPS: " + repr(int(mainClock.get_fps())),True,WHITE)
    textRect = text.get_rect()
    textRect.centerx = boardOffSet_X/2
    textRect.centery = board_YRES/2
    windowSurface.blit(text, textRect)
def tests():
    global board
    board = [ 
                 [0,0,0,0],
                 [0,1,0,0],
                 [0,0,2,0],
                 [0,0,0,0],
                 ]
    resetPieces()
    blackpiece = pieces[0]
    redpiece = pieces[1]
    print "black piece is at:",blackpiece.x,blackpiece.y,blackpiece.killed
    print "red piece is at:",redpiece.x,redpiece.y
    redpiece.doMove(0,0,True)
    print "black piece is at:",blackpiece.x,blackpiece.y,blackpiece.killed,blackpiece.notReallyDead
    print "red piece is at:",redpiece.x,redpiece.y
    if board[0][0] == 2 and board[1][1] == 0:
        print "yay"
    else:
        print "fail",board[0][0],board[1][1]

def updateComp():
    global selectedPiece, computermove, computerTimer, redTurn, computerstate
    if computerstate > 0 and not gameOver:
        computerTimer += mainClock.get_time()
        if computerstate == 1:
            if computerTimer >= 1000:
                computermove.do()
                computerstate = 2
                computerTimer = 0
        if computerstate == 2:
            if computerTimer >= 500:
                selectedPiece = None
                computerTimer = 0
                computermove = None
                computerstate = 0
                redTurn = False
                checkPieces()
                
                

def updateGame():
    """ All functions that update the game are encapuslated here. 
        Starts updated when game starts or show's the menu on startup"""
    mainClock.tick()
    if gameStarted:
        updateComp()
        drawBoard()
        drawPieces()
        drawtext()
    else:
        drawMenu()

testing = False
if testing:
    tests()
    sys.exit()
## Main Game Loop ##
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        eventCheck(event)
    windowSurface.fill(BLACK)
    updateGame()
    pygame.display.update()
            
            