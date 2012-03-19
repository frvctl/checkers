## Created By: Benjamin Vest                                        ##
## ==========================SUMARY===============================  ##
## -> Checker's Game with an AI opponent                            ##
## -> Compare the effectiveness of three heuristic search algorithms##
##    namely the MiniMax, NegaScout, and Alpha-Beta                 ##
## ==========================DATES================================  ##
## -> Start: 11-5-11                                                ##
## -> Version 1: 11-6-11                                            ##
## -> Version 2: Pictures + Menu: 11-7-11                           ##
## -> Version 3: MiniMax added and refined 12-19-11 --> 12-23-11    ## 
## -> Version 4: Added comments, refined code for readability       ##
##               12-24-11                                           ## 
## -> Version 5: Added recording and play back  --> 12-26-11        ##
## -> Version 6: Complete revision of board system --> 12-31-11     ##
## -> Version 7: Added time limited cut-off --> 1-9-12              ##
## ==========================TODO=================================  ##
## -> Fix FPS bug                                                   ##
 

## ======== Imports ========= ##
import random
import sys
from classes import *
from constants import *
## ========================== ##

STATS = True #If true the GUI will be suppressed -- for algorithm testing purposes

pygame.init() # Initializes pygame
mainClock = pygame.time.Clock() # Game clock: used for slowing down the AI opponent and tracks speed of functions
if not STATS:
    ## ================================== Window Surface ======================================= ##
    windowSurface = pygame.display.set_mode((board_XRES + boardOffSetLeft_X, board_YRES), 0, 32)
    pygame.display.set_caption('Checkers!')
    ## ========================================================================================= ##

    ## ============================= Fonts ================================= ##
    font1 = pygame.font.SysFont(None, 60, bold = True, italic = True)
    font2 = pygame.font.SysFont(None, 36)
    ## ===================================================================== ##

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

## Visual Representation of the board and numbers assigned to it ##
        ## ==== Black Pieces ==== ##
        ##      45  46  47  48    ##
        ##    39  40  41  42      ##
        ##      34  35  36  37    ##
        ##    28  29  30  31      ##
        ##      23  24  25  26    ##
        ##    17  18  19  20      ##  
        ##      12  13  14  15    ##
        ##    6   7   8   9       ##
        ## ===== Red Pieces ===== ##
## ============================================================== ##

## ===================================================== State Variables =============================================================== ##
gameOver = False            # Determines if game is over
gameStarted = False         # Determines if game is started
playerWon = "Winner"        # Keeps track of the winner
whosTurn = PIECE_RED        # Starting turn
selectedPiece = None        # Shows if there is a piece selected
computerPlayer = False      # Makes the computer play
computerState = 0           # Used to see what the computer is doing - if it equals 1 it is a red piece, if it equals 2 it is a black piece
computerMove = None         # Assigns the best move to the computer that the computer will then do
computerTimer = 0           # Timer for the AI - used so that the computer is not super fast - makes it more playable 
moveList = []               # Stores lists of moves that the AI uses
record = recording()        # Make a new recording instance
playingRecord = False       # Determines if the recording is being played
playState = 0               # Used for going through the recorded game
playIndex = 0               # Same as above
awaitingSecondJump = False  # For double jump checking - making sure pieces are used correctly
playSpeed = 1000            # The standard speed for play back, 1 second per move
players = []                # Used to determine who or what plays who or what
playerIndexs = []           # Index's of piece positions
selectedIndex = None        # The selected index of the board   
board = []                  # List representing the checkers board   
numEvals = 0                # Keeps track of the number of evaluations for a given move
soloGame = False            # True when soloButton is pressed, activates the solo menu
aiGame = False              # True when the AIButton is pressed, activates the AI menu
options = False             # True when the optionsButton is pressed, activates the options menu
moveCount = 0               # Keeps track of the number of moves
numberOfGames = 20          # The number of games stat loop goes through
statCounter = 0             
currentTime = 0
maxTime = 4000
## ===================================================================================================================================== ##

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

def handleWin(isRed, redWon):
    if redWon:
        if isRed == PIECE_RED:
            return INFINITY / 2
        else:
            return -INFINITY / 2
    else:
        if isRed == PIECE_RED:
            return -INFINITY / 2
        else:
            return INFINITY / 2
        
        
def evaluateTheCramp(sq):
    evalNum = 0
    if sq[28] == PIECE_BLACK | MAN and sq[34] == PIECE_RED | MAN:
        evalNum += CRAMP
    if sq[26] == PIECE_RED | MAN and sq[20] == PIECE_BLACK | MAN:
        evalNum -= CRAMP
    return evalNum

def evaluateTheBackRankGuard(sq):
    evalNum = 0
    code = 0
    if sq[6] & MAN: code += 1
    if sq[7] & MAN: code += 2
    if sq[8] & MAN: code += 4
    if sq[9] & MAN: code += 8
    backrank = rank[code]

    code = 0
    if sq[45] & MAN: code += 8
    if sq[46] & MAN: code += 4
    if sq[47] & MAN: code += 2
    if sq[48] & MAN: code += 1
    backrank = backrank - rank[code]
    evalNum *= BRV * backrank
    return evalNum

def evaluateTheDoubleCorner(sq):
    evalNum = 0
    if sq[9] == PIECE_BLACK | MAN:
        if sq[14] == PIECE_BLACK | MAN or sq[15] == PIECE_BLACK | MAN:
            evalNum += DOUBLECORNERSCALAR

    if sq[45] == PIECE_RED | MAN:
        if sq[39] == PIECE_RED | MAN or sq[40] == PIECE_RED | MAN:
            evalNum -= DOUBLECORNERSCALAR
    return evalNum

def evaluateTheCenter(sq):
    evalNum = 0
    nbmc = nbkc = nwmc = nwkc = 0
    for c in center:
        if sq[c] != FREE:
            if sq[c] == PIECE_BLACK | MAN:
                nbmc += 1
            if sq[c] == PIECE_BLACK | KING:
                nbkc += 1
            if sq[c] == PIECE_RED | MAN:
                nwmc += 1
            if sq[c] == PIECE_RED | KING:
                nwkc += 1
    evalNum += (nbmc - nwmc) * MCV
    evalNum += (nbkc - nwkc) * KCV
    return evalNum

def evaluateTheEdge(sq):
    evalNum = 0
    nbme = nbke = nwme = nwke = 0
    for e in edge:
        if sq[e] != FREE:
            if sq[e] == PIECE_BLACK | MAN:
                nbme += 1
            if sq[e] == PIECE_BLACK | KING:
                nbke += 1
            if sq[e] == PIECE_RED | MAN:
                nwme += 1
            if sq[e] == PIECE_RED | KING:
                nwke += 1
    evalNum -= (nbme - nwme) * MEV
    evalNum -= (nbke - nwke) * KEV
    return evalNum

def evaluateTheTempo(sq, nm, nbk, nbm, nwk, nwm):
    evalNum = tempo = 0
    for i in range(6, 49):
        if sq[i] == PIECE_BLACK | MAN:
            tempo += row[i]
        if sq[i] == PIECE_RED | MAN:
            tempo -= 7 - row[i]

    if nm >= 16:
        evalNum += OPENING * tempo
    if nm <= 15 and nm >= 12:
        evalNum += MIDGAME * tempo
    if nm < 9:
        evalNum += ENDGAME * tempo

    for s in safeedge:
        if nbk + nbm > nwk + nwm and nwk < 3:
            if sq[s] == PIECE_RED | KING:
                evalNum -= 15
        if nwk + nwm > nbk + nbm and nbk < 3:
            if sq[s] == PIECE_BLACK | KING:
                evalNum += 15
    return evalNum

def evaluateThePlayerOpposition(sq, nwm, nwk, nbk, nbm, nm, nk):
    evalNum = 0
    pieces_in_system = 0
    tn = nm + nk
    if nwm + nwk - nbk - nbm == 0:
        if whosTurn == PIECE_BLACK:
            for i in range(6, 10):
                for j in range(4):
                    if sq[i + 11 * j] != FREE:
                        pieces_in_system += 1
            if pieces_in_system % 2:
                if tn <= 12: evalNum += 1
                if tn <= 10: evalNum += 1
                if tn <= 8: evalNum += 2
                if tn <= 6: evalNum += 2
            else:
                if tn <= 12: evalNum -= 1
                if tn <= 10: evalNum -= 1
                if tn <= 8: evalNum -= 2
                if tn <= 6: evalNum -= 2
        else:
            for i in range(12, 16):
                for j in range(4):
                    if sq[i + 11 * j] != FREE:
                        pieces_in_system += 1
            if pieces_in_system % 2 == 0:
                if tn <= 12: evalNum += 1
                if tn <= 10: evalNum += 1
                if tn <= 8: evalNum += 2
                if tn <= 6: evalNum += 2
            else:
                if tn <= 12: evalNum -= 1
                if tn <= 10: evalNum -= 1
                if tn <= 8: evalNum -= 2
                if tn <= 6: evalNum -= 2
    return evalNum
       
def evaluationUtility():
    """ Player evaluation function """
    global numEvals
    sq = board
    code = sum(value[s] for s in sq)
    nbm = code % 16
    nbk = (code >> 4) % 16
    nwm = (code >> 8) % 16
    nwk = (code >> 12) % 16

    v1 = 100 * nbm + 130 * nbk
    v2 = 100 * nwm + 130 * nwk

    evalNum = v1 - v2 # material values
    # favor exchanges if in material plus
    evalNum += (250 * (v1 - v2))/(v1 + v2)

    nm = nbm + nwm
    nk = nbk + nwk

    # final evaluation below
    if whosTurn == PIECE_BLACK:
        evalNum += TURN
        mult = -1
    else:
        evalNum -= TURN
        mult = 1
    
    numEvals += 1
    
    blah = mult * \
            (evalNum +evaluateTheCramp(sq) + evaluateTheBackRankGuard(sq) +
            evaluateTheDoubleCorner(sq) + evaluateTheCenter(sq) +
            evaluateTheEdge(sq) +
            evaluateTheTempo(sq, nm, nbk, nbm, nwk, nwm) +
            evaluateThePlayerOpposition(sq, nwm, nwk, nbk, nbm, nm, nk))
    return blah

def evalstate(who):
    return evaluationUtility()

def randomMove():
    possibleMoves = legal_moves()
    bestMove = None
    try:
        randomIndex = random.randint(0, len(possibleMoves)-1)
        bestMove = possibleMoves[randomIndex]
    except:
        pass
    return bestMove
               
def miniMax(depth):   

    winCheck = checkPieces(whosTurn)
    if winCheck[0]:
        return handleWin(whosTurn,winCheck[1]),None
    if depth == 0:
        return evalstate(whosTurn),None
    
    bestValue = INFINITY 
    bestMove = None
    if whosTurn == PIECE_RED:
        bestValue = -INFINITY
    moves = legal_moves()
    if len(moves)==0:   # No moves in the list
        if whosTurn == PIECE_RED:
            return -INFINITY,None
        return INFINITY,None
    
    for move in moves:
        move.do()
        value = miniMax(depth-1)[0]
        move.undo()
        if whosTurn == PIECE_RED:
            if value > bestValue:
                bestValue = value
                bestMove = move
        else:
            if value < bestValue:
                bestValue = value
                bestMove = move
    return bestValue, bestMove


def alphaBeta(maxDepth, currentDepth, alpha, beta):    
    
    global currentTime
    winCheck = checkPieces(whosTurn)
    if winCheck[0]:
        return handleWin(whosTurn,winCheck[1]),None
    if currentDepth == maxDepth:
        return evalstate(whosTurn),None
    
    bestValue = -INFINITY
    localalpha = alpha
    bestMove = None
    moves = sort(legal_moves())
    if len(moves)==0:   # No moves in the list
        return -INFINITY,None
    for move in moves:
        currentTime += mainClock.tick()
        if currentTime >= maxTime:
            return -INFINITY,None
        move.do()
        value = -alphaBeta(maxDepth, currentDepth+1,-beta,-localalpha)[0]
        move.undo()
        if value > bestValue:
            bestValue = value
            bestMove = move
        
        if bestValue >= beta:
            break
        if bestValue > localalpha:
            localalpha = bestValue
    return bestValue, bestMove


def negaMax(maxDepth, currentDepth, alpha, beta):    

    global currentTime
    winCheck = checkPieces(whosTurn)
    if winCheck[0]:
        return handleWin(whosTurn,winCheck[1]),None
    if currentDepth == maxDepth:
        return evalstate(whosTurn),None
    
    bestValue = -INFINITY
    bestMove = None
    moves = sort(legal_moves())
    if len(moves)==0:   # No moves in the list
        return -INFINITY,None   
    for move in moves:
        currentTime += mainClock.tick()
        if currentTime >= maxTime:
            return -INFINITY,None
        move.do()
        #if depth > 1:
        value = -negaMax(maxDepth, currentDepth+1,-beta,-max(alpha,bestValue))[0]
        #else:
        #    value = alphaBeta(depth-1,-beta,-localalpha)[0]
        move.undo()
        
        if value > bestValue:
            bestValue = value
            bestMove = move
        
        if bestValue >= beta:
            break
    return bestValue, bestMove

def negaScout(maxDepth, currentDepth, alpha, beta):   
    
    global currentTime
    winCheck = checkPieces(whosTurn)
    if winCheck[0]:
        return handleWin(whosTurn,winCheck[1]),None
    if currentDepth == maxDepth:
        return evalstate(whosTurn),None
    adaptiveBeta = beta
    bestMove = None
    bestValue = -INFINITY      
    moves = sort(legal_moves())
    if len(moves)==0:   # No moves in the list
        return -INFINITY,None
    for move in moves:
        currentTime += mainClock.tick()
        if currentTime >= maxTime:
            return -INFINITY,None
        move.do()       
        currentScore = -negaMax(maxDepth,currentDepth+1,-adaptiveBeta,-max(alpha,bestValue))[0]
        move.undo()
        if currentScore > bestValue:
            if adaptiveBeta == beta or currentDepth >= (maxDepth-2):
                bestValue = currentScore
                bestMove = move
            else:
                negativeBestScore , bestMove = negaScout(maxDepth,currentDepth+1,-beta,-currentScore)
                bestValue = -negativeBestScore
        if bestValue >= beta:
            break
        adaptiveBeta = max(alpha, bestValue)+1
    return bestValue, bestMove

def sort(moves):
    listToSort = []
    finalList = []
    for move in moves:
        move.do()
        listToSort.append((evalstate(whosTurn),move))
        move.undo()
    isReddd = True if whosTurn==PIECE_RED else False
    newlist = sorted(listToSort,key=lambda blah:blah[0],reverse=isReddd)
    for keymoves in newlist:
        finalList.append(keymoves[1])
    return finalList

def processClick(mousePos):
    """ 
        Overall click processing function, makes sure every move is legal.
        Utilizes getPiece and canMove functions 
    """
    global selectedIndex, redTurn, moveList, awaitingSecondJump, soloGame
    x, y = mousePos
    
    if not soloGame and not aiGame and not options:
        if not gameStarted:
            for button in buttonlist:
                if button.inside(x,y):
                    button.f()
            return
        for theButton in inGameButtons:
            if theButton.inside(x,y):
                theButton.f()
        if playingRecord:
            for aButton in playBackButtons:
                if aButton.inside(x,y):
                    aButton.f() 
    elif not gameStarted:                   
        if soloGame:
            for soloingButton in soloButtons:
                if soloingButton.inside(x,y):
                    soloingButton.f()
        elif options:
            for optionButton in optionButtons:
                if optionButton.inside(x,y):
                    optionButton.f()
        else:
            for aiTimeButton in AIButtons:
                if aiTimeButton.inside(x,y):
                    aiTimeButton.f()
                
    if gameOver:
        return
    grid_X = ((x-boardOffSetLeft_X) / CELL_X)
    grid_Y = (y / CELL_Y)
    try:
        index = pos[grid_X + grid_Y*8]
    except:
        index = None
    if selectedIndex:
            if selectedIndex == index:
                selectedIndex = None
                return
            elif index:
                for checkIdx in playerIndexs:
                    start = checkIdx[0]
                    if index == start:
                        selectedIndex = index 
                        
                
            for checkIdx in playerIndexs:
                start,dest = checkIdx[:2]
                if (selectedIndex, index) == (start,dest):
                    checkIdx[2].do()
                    endPlayerTurn()
                    selectedIndex = None     
            return
    elif index:
        for checkIdx in playerIndexs:
            start = checkIdx[0]
            if index == start:
                selectedIndex = index 
            
def endPlayerTurn():
    for player in players:
        player.started = False
    checkPieces()

def setPlayerMoves():
    global playerIndexs
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
    playerIndexs =  indexs
    
def legal_moves():
    return getJumps() or getMoves()
    
def getEnemy():
    return whosTurn^COLORS
    
def getMoves():
    moves = []
    player = whosTurn
    valid_indices = RED_INDEX if player == PIECE_RED else BLACK_INDEX
    for i in validSquares:
        if (board[i]&player):
            if(board[i]&MAN):
                for j in valid_indices:
                    dest = i+j
                    if (board[dest]&FREE):
                        sq1 = [i,player|MAN,FREE]
                        if ((player == PIECE_RED and i>=39) or (player == PIECE_BLACK and i<=15)):
                            sq2 = [dest,FREE,player|KING]
                        else:
                            sq2 = [dest,FREE,player|MAN]
                        moves.append(move([sq1,sq2]))
            if (board[i]&KING):                
                for j in KING_INDEX:
                    dest = i+j
                    if (board[dest]&FREE):
                        sq1 = [i,player|KING,FREE]
                        sq2 = [dest,FREE,player|KING]
                        moves.append(move([sq1,sq2]))
    return moves

def getJumps():
    jumps = []
    player = whosTurn
    enemy = getEnemy()
    valid_indices = RED_INDEX if player == PIECE_RED else BLACK_INDEX
    for i in validSquares:
        if (board[i]&player):
            if (board[i]&MAN):
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
            if (board[i]&KING):
                for j in KING_INDEX:
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
                        extraJumps = getExtendedJumps(KING_INDEX, jump, captureKing, visited)
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
            if (board[mid]&enemy and board[dest]&FREE and (last_pos,mid,dest) not in visited and (dest,mid,last_pos) not in visited):
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

def resetBoard():  
    
    """ 
        Redraw's the board, numbers based on the board below 
    
        ## ==== Black Pieces ==== ##
        ##      45  46  47  48    ##
        ##    39  40  41  42      ##
        ##      34  35  36  37    ##
        ##    28  29  30  31      ##
        ##      23  24  25  26    ##
        ##    17  18  19  20      ##  
        ##      12  13  14  15    ##
        ##    6   7   8   9       ##
        ## ===== Red Pieces ===== ##
        
    """
    global board

    board = [OCCUPIED for i in range(56)]
    s = board
    for i in range(0, 4):
            s[6+i] = s[12+i] = s[17+i] = PIECE_RED | MAN
            s[34+i] = s[39+i] = s[45+i] = PIECE_BLACK | MAN
            s[23+i] = s[28+i] = FREE  
            
resetBoard()

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
#\/Uncomment for performance test!\/
#perftest()
      
def doComputer(ai = AI_NEGA):
    """ Activates the computer Player """
    global selectedIndex, computerState,computerMove, numEvals, moveCount, gameOver, currentTime
    mainClock.tick()
    currentTime = 0
    depth = 1
    bestMove = None
    if ai & AI_ALPHA:
        while depth < 12:
            tempMove = alphaBeta(depth, 0,-INFINITY,INFINITY)[1]
            if tempMove:
                bestMove = tempMove
            else: break
            depth += 1
        plrstring = "Alphabeta"
    elif ai & AI_MINI:
        bestMove = miniMax(5)[1] 
        plrstring = "Minimax"
    elif ai & AI_NEGA:
        while depth < 12:
            tempMove = negaScout(depth, 0, -INFINITY, INFINITY)[1]
            if tempMove:
                bestMove = tempMove
            else: break
            depth += 1
        plrstring = "NegaScout"
    elif ai & AI_RANDOM:
        bestMove = randomMove()
        plrstring = "Random"

    print plrstring ,",", numEvals, ",",currentTime, ",", depth
    numEvals = 0
    if bestMove:
        computerMove = bestMove
        selectedIndex = bestMove.affectedSquares[0][0]
        computerState = 1
        moveCount += 1
    
    else: print "whaaaat"
                 
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
    global playerWon, whosTurn, gameOver
    redCanMove = False
    blackCanMove = False
    if legal_moves():
        if whosTurn == PIECE_RED:
            redCanMove = True
        else:
            blackCanMove = True
    whosTurn ^= COLORS
    if legal_moves():
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
        print playerWon , "WON"
        record.save("Game #" + str(statCounter))  # Saves game into a file
        
def resetGame():  
    """ Allow's the game to be reset"""   
    global gameOver,whosTurn
    gameOver = False
    whosTurn = PIECE_RED
    resetBoard()  
    
def optionButton():
    global options
    options = True

def blackStart():
    global whosTurn
    whosTurn = PIECE_BLACK

def redStart():
    global whosTurn
    whosTurn = PIECE_RED
      
def startmulti():   
    """ Multiplayer game mode start button. In the menu."""    
    global gameStarted,players
    players = [HumanPlayer(PIECE_BLACK),HumanPlayer(PIECE_RED)]
    if gameOver or computerPlayer:
        resetGame()
    gameStarted = True
    
def soloButton():
    global soloGame
    soloGame = True
    
def battleModeButton():
    global aiGame
    aiGame = True
    
def exitbutton(): 
    """ Button used to exit the game. In the menu.""" 
    pygame.quit()
    sys.exit()
    
def miniMaxButton():
    global gameStarted, computerPlayer,players, soloGame
    players = [HumanPlayer(PIECE_BLACK),ComputerPlayer(PIECE_RED, AI_MINI)]
    if gameOver or not computerPlayer:
        resetGame()
    computerPlayer = True
    gameStarted = True
    soloGame = False
    
def alphaBetaButton():  
    global gameStarted, computerPlayer,players, soloGame
    players = [HumanPlayer(PIECE_BLACK),ComputerPlayer(PIECE_RED, AI_ALPHA)]
    if gameOver or not computerPlayer:
        resetGame()
    computerPlayer = True
    gameStarted = True
    soloGame = False

def negaScoutButton():
    global gameStarted, computerPlayer, players, soloGame
    players = [HumanPlayer(PIECE_BLACK),ComputerPlayer(PIECE_RED, AI_NEGA)]
    if gameOver or not computerPlayer:
        resetGame()
    computerPlayer = True
    gameStarted = True
    soloGame = False
    
def negaA_vs_alphaB():
    global gameStarted, computerPlayer, players
    players = [ComputerPlayer(PIECE_RED, AI_NEGA),ComputerPlayer(PIECE_BLACK, AI_ALPHA)]
    if gameOver or not computerPlayer:
        resetGame()
    computerPlayer = True
    gameStarted = True

def negaA_vs_miniB():
    global gameStarted, computerPlayer, players
    players = [ComputerPlayer(PIECE_RED, AI_NEGA),ComputerPlayer(PIECE_BLACK, AI_MINI)]
    if gameOver or not computerPlayer:
        resetGame()
    computerPlayer = True
    gameStarted = True
    
def negaA_vs_randoB():
    global gameStarted, computerPlayer, players
    players = [ComputerPlayer(PIECE_RED, AI_NEGA),ComputerPlayer(PIECE_BLACK, AI_RANDOM)]
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
    
def menuReturn():
    global gameStarted, aiGame, soloGame, options
    gameStarted = False
    aiGame = False
    soloGame = False
    options = False
    
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
        
def drawMenu():
    """ Draw's a menu picture """
    windowSurface.blit(introImage,(0, 0, board_XRES + boardOffSetLeft_X, board_YRES))
    for button in buttonlist:
        button.draw(windowSurface,font2)
        
def drawSoloMenu():    
    windowSurface.blit(introImage,(0, 0, board_XRES + boardOffSetLeft_X, board_YRES))
    for button in soloButtons:
        button.draw(windowSurface,font2)
        
def drawAIMenu():
    windowSurface.blit(introImage,(0, 0, board_XRES + boardOffSetLeft_X, board_YRES))
    for button in AIButtons:
        button.draw(windowSurface,font2)
        
def drawOptionsMenu():
    windowSurface.blit(introImage,(0, 0, board_XRES + boardOffSetLeft_X, board_YRES))
    for button in optionButtons:
        button.draw(windowSurface,font2)
        
def drawInGameButtons():
    if soloGame == False:
        for button in inGameButtons:
            button.draw(windowSurface,font2)
    
def drawPlayBackButtons():
    if soloGame == False:
        for button in playBackButtons:
            button.draw(windowSurface,font2)
    

buttonlist = [
              button(200, 300, 300, 100, "Local Multi-Player Game", startmulti),
              button(500, 750, 200, 100, "Exit", exitbutton),
              button(400, 600, 500, 100, "Playback: Watch the Previous Game", playRecordButton),
              button(300, 450, 300, 100, "Solo Game Modes", soloButton),
              button(600, 300, 400, 100, "Computer Battle Variations", battleModeButton),
              button(700, 450, 200, 100, "Options", optionButton)   
              ]

inGameButtons = [
                 button(75, 200, 150, 100, "Undo", undoButton),
                 button(75, 500, 150, 100, "Main Menu", menuReturn),
                 button(75, 350, 150, 100, "Reset Game", resetGameButton),
                 ]

playBackButtons = [
                   button(25, 300, 50, 30, ">>", fastButton),
                   button(150, 300, 50, 30, "<<", slowButton),
                   button(150, 600, 100, 100, "Menu", menuInRecordingButton),
                   ]

soloButtons = [
                button(200, 300, 500, 100, "Play against the MiniMax Algorithm", miniMaxButton),
                button(300, 450, 500, 100, "Play against the AlphaBeta Algorithm", alphaBetaButton),
                button(400, 600, 500, 100, "Play against the NegaScout Algorithm", negaScoutButton),
                button(500, 750, 200, 100, "Exit", exitbutton),
                button(750, 750, 300, 100, "Return to Main Menu", menuReturn) 
                ]

AIButtons = [
              button(200, 300, 650, 100, "NegaScout Algorithm versus the MiniMax Algorithm", negaA_vs_miniB),
              button(300, 450, 650, 100, "NegaScout Algorithm versus the AlphaBeta Algorithm", negaA_vs_alphaB),
              button(400, 600, 650, 100, "NegaScout Algorithm versus the Random Player", negaA_vs_randoB),
              button(500, 750, 200, 100, "Exit", exitbutton),
              button(750, 750, 300, 100, "Return to Main Menu", menuReturn) 
              ]

optionButtons = [
                 button(200, 300, 200, 100, "Black goes first", blackStart),
                 button(500, 300, 200, 100, "Red goes first", redStart),
                 button(500, 750, 200, 100, "Exit", exitbutton),
                 button(750, 750, 300, 100, "Return to Main Menu", menuReturn)
                 ]

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
    for i in validSquares:
        s = board[i]
        if s&COLORS:
            y,x = grd[i]
            screen_X = ((x) * CELL_X) + boardOffSetLeft_X
            screen_Y = (y) * CELL_Y
            windowSurface.blit(getPicforSquare(s), (screen_X, screen_Y, screen_X + CELL_X, screen_Y + CELL_Y))
                        
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
    if whosTurn == PIECE_BLACK:
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
    global computerMove, computerTimer, computerState, selectedIndex, moveCount
    if computerState > 0 and not gameOver:
        computerTimer += mainClock.get_time()
        if computerState == 1:
            if computerTimer >= 1000:
                computerMove.do(True)
                selectedIndex = computerMove.affectedSquares[-1][0]
                computerState = 2
                computerTimer = 0
        if computerState == 2:
            if computerTimer >= 500:
                computerTimer = 0
                selectedIndex = None
                computerMove = None
                computerState = 0
                endPlayerTurn()

def updateRecord():
    """ Is responsible for playing back the recorded list """
    global selectedIndex, playState,playIndex,playingRecord,computerTimer
    if playState > 0 and not gameOver:
        computerTimer += mainClock.get_time()
        if playState == 1:
            selectedIndex = record.moveList[playIndex].affectedSquares[0][0]
            playState = 2   
        if playState == 2:
            if computerTimer >= playSpeed:
                record.moveList[playIndex].do()
                selectedIndex = record.moveList[playIndex].affectedSquares[-1][0]
                playState = 3
                computerTimer = 0
                playIndex += 1
        if playState == 3:
            if computerTimer >= (playSpeed/2):
                selectedIndex = None
                computerTimer = 0
                playState = 1
                checkPieces()   
                
def statLoop():
    global players,statCounter, gameOver,numberOfGames, moveCount
    localCounter = 0
    try:
        statCounter = pickle.load(open("Stats.txt","r"))
    except:
        statCounter = 1
    while localCounter < numberOfGames:
        resetGame()
        players = [ComputerPlayer(PIECE_RED, AI_NEGA),ComputerPlayer(PIECE_BLACK, AI_ALPHA)]
        print "GAME #" , statCounter
        print players
        print ("Red first" if whosTurn&PIECE_RED else "Black first"), ",COUNT", ",TIME(MS)"
        while not gameOver:
            for player in players:
                if not player.started and player.getColor() == whosTurn:
                    isComputer = player.startTurn()
                    if isComputer[0]:
                        if moveCount > 150:
                            print "too many moves,blah"
                            gameOver = True
                        else:
                            doComputer(isComputer[1])
                        if computerMove:
                            computerMove.do(True)
                            checkPieces()
                        if gameOver: break
            for player in players:
                player.started = False
        record.clear()
        pickle.dump(statCounter, open("Stats.txt","w"))
        statCounter += 1
        localCounter += 1
        moveCount = 0
                
class statPrint:
    def write(self,txt):
        with open("log.csv","a") as f:
            f.write(txt)

if STATS:
    sys.stdout = statPrint()
    statLoop()
    sys.exit()
     
def updateGame():
    """ 
        All functions that update the game are encapsulated here. 
        Starts updated when game starts or show's the menu on startup
    """
    mainClock.tick()
    if playingRecord:
        updateRecord()
    if gameStarted and not playingRecord and not soloGame and not options:
        for player in players:
            if not player.started and player.getColor() == whosTurn:
                isComputer = player.startTurn()
                if isComputer[0]:
                    doComputer(isComputer[1])
                    drawBoard()
                    drawPieces()#update drawing so we don't get confused (ben failz)
                else:
                    setPlayerMoves()
        updateComp()
        drawInGameButtons()
        drawBoard()
        drawPieces()
        drawtext()
    elif soloGame:
        drawSoloMenu()
    elif aiGame:
        drawAIMenu()
    elif options:
        drawOptionsMenu()
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
            
            
            
            

