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
board_X = 10                        # horizontal size of the BitMap
board_Y = 10                        # vertical size of the BitMap
realBoard_X = 8                     # Real size of the BitMap, horizontally, excluding the border (9's)
realBoard_Y = 8                     # Real size of the BitMap, vertically, excluding the border(9's)
CELL_X = board_XRES / realBoard_X   # Length of a single checker square
CELL_Y = board_YRES / realBoard_Y   # Height of a single checker square
## ====================================================================================================== ##

## ========= Piece constants based on BitMap ============= ##
PIECE_EMPTY = 0     # Nothing drawn onto board
PIECE_RED = 1       # Red Piece
PIECE_BLACK = 2     # Black Piece
PIECE_VOID = 9      # No piece drawn -- Border of BitMap
## ======================================================= ##

## =================================== Move Lists ============================================= ##
## Each tuple represents a move that the pieces are allowed to make. Up and down                ##
## is relative to looking at the board from the bottom, where the red pieces are, as down,      ##
## and the top of the board with black pieces being up.                                         ##
## ============================================================================================ ##
## (2, 2) = Jump up right;         (2, -2) = Jump down left;                                    ##
## (-2, -2) = Jump up left;        (-2, 2) = Jump up right;                                     ##
## (1, 1) = Down right;            (1, -1) = Down left;                                         ##
## (-1, -1) = Up left;             (-1, 1) = Up right;                                          ##
## ============================================================================================ ##
## The numbers represent the difference of the pieces initial coordinates on the BitMap         ##
## - as in a set of numbers such as 7, 4; 7 being the X coordinate and 3 being the Y coordinate ##
## - and the pieces new coordinates. Thus if the piece moves from 7, 4 to 6, 5                  ##
## - a perfectly legal move - it would return (-1, 1) which indicates Forward right.            ##
## ============================================================================================ ##
possibleMoves = [(2,2),(2,-2),(-2,-2),(-2,2),(1,1),(1,-1),(-1,1),(-1,-1)] # All possible moves
movesWithoutJumps = [(1,1),(1,-1),(-1,-1),(-1,1)]                         # Moves without jumps
## ============================================================================================ ##

## ===================================================== State Variables =============================================================== ##
gameOver = False            # Determines if game is over
gameStarted = False         # Determines if game is started
playerWon = "Winner"        # Keeps track of the winner
redTurn = False             # Turn feature
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
playSpeed = 1000
ALPHABETA = True
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

class piece:
    
    """ 
    
         Controls most aspects that have to do with the pieces on the          
         board. Including displaying pieces, determining if movement is legal, 
         aspects of the AI allowing it to do and undo moves, and the evaluate  
         function
         
    """
    
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
        
        """ 
            Determines if a piece can move. Kings can move forward and backward. 
            Red pieces can move forward only. Black pieces can move backward only.
            
        """
        
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
                if board[temp_Y - unit_Y][temp_X - unit_X] == self.otherColor:    # If diff_X is greater than one and is a black piece it is a valid jump
                    return True, move(self.x,self.y,temp_X,temp_Y) , True         # Returns True (it can move) - temp_X and temp_Y (the coordinates after the move) - and True (since it is a jump move)
                else:                                                             # Else the above falls through - returns False (it cannot move) 
                    return False,                                                 # returns False (it cannot move)  
            return True, move(self.x,self.y,temp_X,temp_Y) , False                # Applies the first if - assuming all else falls through - returns True (it can move) - temp_X and temp_Y (the coordinates after the move) - and False (it is not a jump)
        return False,                                                             # Assuming none of the above apply returns False (it cannot move) 
    
    def doMove(self, x, y, notReallyDead=False):
        
        """ Does a move no matter what, can be temporary for computer checks """
        
        board[self.y][self.x] = PIECE_EMPTY         # It just moved from here, so it's now empty
        diff_X = x - self.x                         # Where it is moving, for jump checking, X coordinate 
        diff_Y = y - self.y                         # Same as above, Y Coordinate
        self.x = x                                  # Set the piece location to the new x, y; X coordinate
        self.y = y                                  # Same as above, Y Coordinate
        board[y][x] = self.color                    # Set the new board location
        if abs(diff_X)==2:                          # If it jumped something
            jump_X = x - (diff_X / abs(diff_X))
            jump_Y = y - (diff_Y / abs(diff_Y))
            board[jump_Y][jump_X] = PIECE_EMPTY
            killedPiece = getPiece(jump_X, jump_Y, forceColor=self.otherColor)
            if killedPiece == None:
                print "WTF do",jump_X,jump_Y,self.otherColor
                return
            if notReallyDead:
                if self.king:
                    self.justJumped += 2
                else: 
                    self.justJumped += 1
                killedPiece.notReallyDead = True
                return
            
            killedPiece.killed = True
            
    def undoMove(self,x,y, notReallyDead = False, checkKilled = False):
        
        """ Same as doMove, except replaces any piece it jumped """
        
        board[self.y][self.x] = PIECE_EMPTY     # It just moved from here, so it's now empty
        diff_X = x - self.x                     # Where it is moving, for jump checking, X coordinate
        diff_Y = y - self.y                     # Same as above, Y coordinate
        self.x = x                              # Set the piece location to the new x, y; X coordinate
        self.y = y                              # Same as above, Y coordinate
        board[y][x] = self.color                # If it jumped something
        if abs(diff_X)==2: 
            jump_X = x - (diff_X/2)
            jump_Y = y - (diff_Y/2)
            board[jump_Y][jump_X] = self.otherColor
            killedPiece = getPiece(jump_X, jump_Y, notReallyDead, checkKilled, forceColor = self.otherColor)
            if notReallyDead:
                if self.king:
                    self.justJumped -= 2
                else:
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
        
        """ Creates a list of moves for the AI to use (through doMove and undoMove) """
        
        list_of_moves = []
        for check_X,check_Y in possibleMoves:
            if self.x + check_X > realBoard_X or self.x + check_X < 1 or self.y + check_Y > realBoard_Y or self.y + check_Y < 1:
                continue
            checkMove = self.canMove(check_X, check_Y)
            if checkMove[0]:
                others = []
                tempList = []
                flag = checkMove[2]
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
                        if checkMove[0] and checkMove[2]:
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
        
        """ 
            Evaluates the current piece's position and determines the best move for the AI to do. 
            Whichever move results in the highest returned value is determined to be the 
            'best move' and the AI proceeds to do that move. The evaluate functions relies 
            heavily on the doMove and undoMove functions to work properly. The AI gets the 
            values by doing all the moves available to it (determined by the depth of the minimax 
            function) then undoing all of those moves then it does the one move that is the best. 
            
        """
        
        numberValue = 0
        if self.canMoveAnywhere():  # If it can move anywhere if the move gains 1 point
            numberValue += 1
        else:                       # If not the move loses 5 points
            numberValue -= 5
            
        numberValue += 15*self.justJumped   # How many it jumped
        
        if not self.king:
            if self.red:
                if self.y == 1:
                    numberValue += 10   # If the Y coordinate of a red piece is 1 it gains 10 points because that means it will be getting a king
            else:
                if self.y == 8:         # Same as above except for black pieces
                    numberValue += 10
        if self.king:
            numberValue += 1
        for i in range(0,len(movesWithoutJumps)):                           # Going through the list of moves that can not jump ie (1, 1) ect
            near_X, near_Y = movesWithoutJumps[i]                           # near_X and near_Y are the respective coordinates of the proximity of moves without jumps to the piece
            if board[self.y + near_Y][self.x + near_X] == self.otherColor:  # If the pieces coordinate + the proximity coordinate equals the coordinates of a piece with a different color 
                next_X, next_Y = movesWithoutJumps[i-2]                     # next_X and next_Y are the X and Y coordinate of the first two items in the movesWithoutJumps list (Up right and Down right)
                if board[self.y + next_Y][self.x + next_X] == PIECE_EMPTY:  # If the coordinates + the next coordinates are equal to an empty space
                    numberValue -= 13                                       # The value goes down 13 because that means the piece has a high chance of being jumped
                 
        if not self.red:
            numberValue = -numberValue
        return numberValue

class move:
    
    """ 
    
        Basic move structure as applied to the checkers board. 
        Takes moves and then evaluates them by calling doMove and undoMove.  
        
    """
    
    def __init__(self, source_X, source_Y, dest_X, dest_Y, *others):
        
        """ Constructor for the move class""" 
        
        self.source_X = source_X    # The X coordinate before a move
        self.source_Y = source_Y    # Same as above; Y Coordinate
        self.dest_X = dest_X        # The X coordinate after a move
        self.dest_Y = dest_Y        # Same as above; Y Coordinate
        self.others = others        # A list of any extra jumps
        if len(others) > 0:
            self.others = others[0]
            
    def do(self, notReallyDead=False):
        
        """ For doing moves """
        
        p = getPiece(self.source_X, self.source_Y)
        p.doMove(self.dest_X,self.dest_Y, notReallyDead)
        for other in self.others:
            if len(other) > 1:
                p.doMove(other[0], other[1], notReallyDead)

        if not notReallyDead:
            record.add(self)
        
            
    def undo(self,fake=False,checkKilled = False):
        
        """ For undoing moves """
        
        p = None
        if len(self.others)>0:
            other = self.others[-1]
            if len(other) > 1:
                p = getPiece(other[0],other[1])
                for i in range(1,len(self.others)):
                    other = self.others[-i-1]
                    if len(other) > 1:
                        p.undoMove(other[0],other[1],fake,checkKilled)
                p.undoMove(self.dest_X,self.dest_Y,fake,checkKilled) 
        else:
            p = getPiece(self.dest_X,self.dest_Y)
        
        
        p.undoMove(self.source_X, self.source_Y,fake,checkKilled)

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

def handleWin(p,redWon):
    if redWon:
        if p.red:
            return INFINITY/2,
        else:
            return -INFINITY/2,
    else:
        if p.red:
            return -INFINITY/2,
        else:
            return INFINITY/2,

def miniMaxInit(depth):
    bestValue = -INFINITY
    bestMove = None
    mainClock.tick()
    for p in pieces:
        if not p.killed and p.red:
            if ALPHABETA:
                value = alphaBeta(p,depth,-INFINITY,INFINITY)
            else:
                value = miniMax(p,depth)
            if value[0] > bestValue:
                bestValue = value[0]
                bestMove = value[1]
    print mainClock.tick()
    return bestMove

def miniMax(p, depth):
    
    """ 
        
        The main miniMax algorithm, must enter the depth that you want 
        it to go to in the doComputer function, the depth entered 
        must be an odd number. 
        
    """
    winCheck = checkPieces(p.color)
    if winCheck[0]:
        return handleWin(p,winCheck[1])
    if depth == 0:
        return p.evaluate(),
    
    bestValue = INFINITY
    bestMove = None
    if p.red:
        bestValue = -INFINITY
    moves = p.makeMoveList()
    if len(moves)==0:   # No moves in the list
        if p.red:
            return -INFINITY,
        return INFINITY,
    
    for move in moves:
        move.do(True)
        if depth > 1:
            for p2 in pieces:
                if not p2.killed and not p2.notReallyDead and p2.red == (depth%2==0): # Starts with black
                    value = miniMax(p2,depth-1)[0]
        else:
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

def alphaBeta(p, depth, alpha, beta):
    
    """ 
        
        The main miniMax algorithm, must enter the depth that you want 
        it to go to in the doComputer function, the depth entered 
        must be an odd number. 
        
    """
    winCheck = checkPieces(p.color)
    if winCheck[0]:
        return handleWin(p,winCheck[1])
    if depth == 0:
        return p.evaluate(),
    
    localalpha = alpha
    bestValue = INFINITY
    bestMove = None
    if p.red:
        bestValue = -INFINITY
    moves = sort(p.makeMoveList())
    if len(moves)==0:   # No moves in the list
        if p.red:
            return -INFINITY,
        return INFINITY,
    
    for move in moves:
        move.do(True)
        if depth > 1:
            for p2 in pieces:
                if not p2.killed and not p2.notReallyDead and p2.red == (depth%2==0): # Starts with black
                    value = alphaBeta(p2,depth-1,-beta,-localalpha)[0]
        else:
            value = alphaBeta(p,depth-1,-beta,-localalpha)[0]
        move.undo(True)
        if p.red:
            if value > bestValue:
                bestValue = value
                bestMove = move
        else:
            if value < bestValue:
                bestValue = value
                bestMove = move
        if bestValue >= beta:
            break
        if bestValue > localalpha:
            localalpha = bestValue
    return bestValue, bestMove

def sort(moves):
    listToSort = []
    finalList = []
    for move in moves:
        p = getPiece(move.source_X,move.source_Y)
        move.do(True)
        listToSort.append((p.evaluate(),move))
        move.undo(True)
    newlist = sorted(listToSort,key=lambda blah:blah[0],reverse=True)
    for keymoves in newlist:
        finalList.append(keymoves[1])
    return finalList
    
    
def depthMiniMax(depth):
    
    """ Allows the main miniMax function to reach a depth greater than 1 """
    
    allMoves = []                   # Every possible move made by the move list
    realBestMove = None             # The actual and real best move
    realBestValue = -sys.maxint     # The smallest number that Python can possibly display
    for p in pieces:                # Looping through all the pieces
        if p.red and not p.killed:
            moves = p.makeMoveList()
            moveCounter = 0     # The number of moves made
            perMove = []        # A list moves and the best evaluated value associated with them
            perMoveValue = []   # A list of values, no moves included
            for move in moves:
                tempDepth = depth
                otherMoves = [] 
                move.do(True)
                perMoveValue.append(0) # Adds a 0 to the list so that it is not empty
                perMove.append(0)      # Same as above
                perMoveValue[moveCounter] = miniMax(p,0)[0] # The list perMoveCounter[0 -> it has not changed from its inital value] = miniMax(p, 0)[0] -> which means it equals 0
                while tempDepth > 1:
                    perDepth = []   # A list of the depths of the miniMax function ie [7, 6, 5, 4, 3, 2, 1, 0]
                    bestValue = -INFINITY
                    if tempDepth%2==1: # If it is a black piece (even depths are black)
                        bestValue = INFINITY
                    bestMove = None    # No bestMove if it is black 
                    for p2 in pieces:
                        if not p2.killed and not p2.notReallyDead and p2.red == (tempDepth%2==0): # Starts with black
                            perDepth.append((miniMax(p2,1), p2.color)) 
                    for depthList in perDepth:
                        theMove = depthList[0]
                        if depthList[1] == PIECE_RED and theMove[0] > bestValue: # Red piece
                            bestValue = theMove[0]
                            bestMove = theMove[1]
                        elif depthList[1] == PIECE_BLACK and theMove[0] < bestValue: # Black piece
                            bestValue = theMove[0]
                            bestMove = theMove[1]      
                    perMove[moveCounter] = (bestValue,move) # Adds the bestValue and the move associated with it to a list
                    perMoveValue[moveCounter] += bestValue  # Adds just the bestValue to a list
                    if bestMove != None:
                        bestMove.do(True)
                        otherMoves.append(bestMove) # Puts the bestMoves found in a new list
                    tempDepth -= 1  # Subtract the depth by one every iteration
                while len(otherMoves) > 0:      # Until the list of otherMoves has nothing in it the moves are undone from the list and in the game
                    otherMoves.pop().undo(True)
                move.undo(True)
                moveCounter += 1  # End of the master move and depth loop
            bestValue = -sys.maxint
            bestIndex = -1
            for i in range(moveCounter):
                value = perMoveValue[i]
                if value > bestValue:   # Red Piece
                    bestValue = value
                    bestIndex = i
            if bestIndex != -1:
                allMoves.append((bestValue,perMove[bestIndex][1]))
    for value in allMoves: 
        if value[0] > realBestValue:
            realBestValue = value[0]
            realBestMove = value[1]
    return realBestMove  # Return best move back to doComputer()
        

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
    resetBoard()
    resetPieces()      
          
def getPiece(x, y, checkfake=False , checkKilled=False, forceColor=None):
    
    """ Determines which pieces are on the board and where they are """
    
    for p in pieces:
        if p.x == x and p.y == y:      
            if p.killed == checkKilled and (not p.notReallyDead or checkfake):  
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
    
def undoButton():
    
    """ Undoes moves from both sides using undoMove """
    
    record.deleteLast().undo(checkKilled=True)

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
              button(286,355,173,103, "Solo", startsolo),
              button(527,353,171,105,"Multi-Player",startmulti),
              button(527,500,171,105,"Exit",exitbutton),
              button(286,500,173,103,"Play",playRecordButton)
              ]

inGameButtons = [
                 button(25, 550, 150,100,"Undo",undoButton),
                 button(25, 700, 150,100, "Main Menu", mainMenuButton),
                 button(25, 850, 150,100, "Reset Game", resetGameButton),
                 ]

playBackButtons = [
                   button(25, 300, 30, 30, ">>", fastButton),
                   button(150, 300, 30, 30, "<<", slowButton),
                   button(150, 600, 100, 100, "Menu", menuInRecordingButton),
                   ]


   
def processClick(pos):
    
    """ 
    
        Overall click processing function, makes sure every move is legal.
        Utilizes getPiece and canMove functions 
        
    """
    global selectedPiece, redTurn, moveList, awaitingSecondJump
    x, y = pos
    if not gameStarted:
        for button in buttonlist:
            if button.inside(x,y):
                button.f()
        return
    for blah in inGameButtons:
        if blah.inside(x,y):
            blah.f()
    for derp in playBackButtons:
        if derp.inside(x,y):
            derp.f()
    if gameOver:
        return
    grid_X = ((x-boardOffSetLeft_X) / CELL_X) + 1
    grid_Y = (y / CELL_Y) + 1
    realPiece = getPiece(grid_X, grid_Y) # The coordinates of the piece is equal to realPiece
    if selectedPiece != None:
            if selectedPiece.x == grid_X and selectedPiece.y == grid_Y:
                selectedPiece = None
                if awaitingSecondJump:
                    endPlayerTurn()
                return
            elif realPiece != None and not awaitingSecondJump:
                if redTurn == realPiece.red and realPiece.canMoveAnywhere():
                    selectedPiece = realPiece # The selected piece is now equal to realPiece 
            canMove = selectedPiece.canMove(grid_X - selectedPiece.x, grid_Y - selectedPiece.y)
            if canMove[0]:
                move = canMove[1]
                move.do()
                if canMove[2]: # Checks to see if it can jump again - four directions to check.
                    for check_X in [2, -2]:
                        for check_Y in [2, -2]:
                            if grid_X + check_X > realBoard_X or grid_X + check_X < 1 or grid_Y + check_Y > realBoard_Y or grid_Y + check_Y < 1:
                                continue
                            canMove = selectedPiece.canMove(check_X, check_Y)
                            if canMove[0] and canMove[2]:
                                awaitingSecondJump = True
                                return
                endPlayerTurn()        
            return
    if realPiece != None:
        if redTurn == realPiece.red and realPiece.canMoveAnywhere():
            selectedPiece = realPiece
            
def endPlayerTurn():
    global selectedPiece,redTurn,awaitingSecondJump
    selectedPiece = None
    awaitingSecondJump = False
    if computerPlayer:
        doComputer()
        return
    redTurn = not redTurn 
    checkPieces() 
    
    
def legal_moves():
    moves = []
    for p in pieces:
        if not p.killed and not p.notReallyDead:
            piecemoves = p.makeMoveList()
            for move in piecemoves:
                moves.append(move)
    return moves
            
    
def perft(depth):
    global redTurn
    if depth == 0:
        return 1

    #state = curr_state or self.curr_state
    nodes = 0
    for move in legal_moves():
        move.do(True)
        nodes += perft(depth-1)
        move.undo(True)
    return nodes

def perftest():
    mainClock.tick()
    for depth in range (1,11):
        print "Depth:",depth,"count:",perft(depth),"Time:",mainClock.tick()

#perftest()
    
       
def doComputer():
    
    """ Activates the computer Player """
    
    global selectedPiece, computerState,computerMove, redTurn
    #mainClock.tick()
    
    #for depth in range(1,11):
        #depthMiniMax(depth)
        #miniMaxInit(depth)
        #print "Depth: ",depth,"Time: ",mainClock.tick()
    #bestMove = depthMiniMax(7)  # The depth which the miniMax function will search to - *must be an odd number*
    
    bestMove = miniMaxInit(5)
    if bestMove != None:
        bestPiece = getPiece(bestMove.source_X,bestMove.source_Y)
        computerMove = bestMove
        selectedPiece = bestPiece
        computerState = 1
        redTurn = True
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
                if selectedPiece != None and selectedPiece.x - 1 == x and selectedPiece.y - 1 == y:
                    color = ORANGE
            pygame.draw.rect(windowSurface, color, ((x * CELL_X)+boardOffSetLeft_X, y * CELL_Y, x + CELL_X, y + CELL_Y)) 
       
def drawPieces():
    
    """ Draw's the pieces onto the board """ 
    
    for p in pieces:
        if p.killed:
            continue
        screen_X = ((p.x - 1) * CELL_X) + boardOffSetLeft_X
        screen_Y = (p.y - 1) * CELL_Y
        windowSurface.blit(p.getPiecePic(), (screen_X, screen_Y, screen_X + CELL_X, screen_Y + CELL_Y))
        
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
    
    global pieces, gameOver, playerWon, selectedPiece
    redCanMove = False
    blackCanMove = False
    for p in pieces:
        if p.killed:
            continue
        if p.red:
            if color == None and p.y == 1:
                p.king = True
            if not redCanMove:
                redCanMove = p.canMoveAnywhere()
        else:
            if color == None and p.y == 8:
                p.king = True
            if not blackCanMove:
                blackCanMove = p.canMoveAnywhere()
    if redCanMove and not blackCanMove and not redTurn:
        gameOver = True
        playerWon = "Red"
    elif blackCanMove and not redCanMove and (redTurn or computerPlayer):
        gameOver = True
        playerWon = "Black"
    elif not blackCanMove and not redCanMove:
        gameOver = True
        playerWon = "Tie"
    if color != None:
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
    textRect.centery = board_YRES/2
    windowSurface.blit(text, textRect)

def updateComp():
    
    """ Slows the computer down so that is not super fast - increases playability """
    
    global selectedPiece, computerMove, computerTimer, redTurn, computerState
    if computerState > 0 and not gameOver:
        computerTimer += mainClock.get_time()
        if computerState == 1:
            if computerTimer >= 1000:
                computerMove.do()
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
            
            
            
            

