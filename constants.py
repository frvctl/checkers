from buttons import button
from game import *

INFINITY = 99999999 # Constant used for the AI algorithms

## ==== Initializes Colors ==== ##
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
ORANGE = (255, 128, 0)
## ============================ ##

## ============================================================ ##
CELL_X = board_XRES / 8   # Length of a single checker square
CELL_Y = board_YRES / 8   # Height of a single checker square
## ============================================================ ##

## ============= Piece constants =========== ##
OCCUPIED = 0    # An occupied square
PIECE_BLACK = 2 # Technically the red piece
PIECE_RED = 1   # Technically the black piece
MAN = 4         # Pieces are MEN if not KING
KING = 8        # Pieces are KING if not MEN
FREE = 16       # Space with nothing on it
## ======================================== ## 

## ======================= Bitwise - used for switch's ================= ##
COLORS = PIECE_BLACK | PIECE_RED    
TYPES = OCCUPIED | PIECE_BLACK | PIECE_RED | MAN | KING | FREE
## ===================================================================== ##

## ============= Index's - Legal moves for a given piece ============== ##
BLACK_INDEX = [-5,-6]       # Possible black moves 
RED_INDEX = [5,6]           # Possible red moves
KING_INDEX = [-6,-5,5,6]    # All possible king moves
## ==================================================================== ##

## ======================================= Size of the window ====================================== ##
boardOffSetLeft_X = 300  # The extra space on the left - used for displaying information to the user
board_XRES = 1000        # Length of the board   
board_YRES = 1000        # Width of the board
## ================================================================================================= ##

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

## ======================== Evaluation list numbers =========================== ##
# All valid square positions based on above board
validSquares = [6,7,8,9,12,13,14,15,17,18,19,20,23,24,25,26,
                     28,29,30,31,34,35,36,37,39,40,41,42,45,46,
                     47,48]
value = [0,0,0,0,0,1,256,0,0,16,4096,0,0,0,0,0,0]
edge = [6,7,8,9,15,17,26,28,37,39,45,46,47,48]
center = [18,19,24,25,29,30,35,36]
# values used to calculate tempo -- one for each square on board (0, 48)
row = [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,2,2,2,2,0,0,3,3,3,3,0,  
           4,4,4,4,0,0,5,5,5,5,0,6,6,6,6,0,0,7,7,7,7]
safeedge = [9,15,39,45]
rank = {0:0, 1:-1, 2:1, 3:0, 4:1, 5:1, 6:2, 7:1, 8:1, 9:0,
            10:7, 11:4, 12:2, 13:2, 14:9, 15:8}
## ============================================================================ ##

## ============ Evaluation Constants =============== ##
TURN = 2      # Molor to move gets + turn
BRV = 3       # Multiplier for back rank
KCV = 5       # Multiplier for kings in center
MCV = 1       # Multiplier for men in center

MEV = 1       # Multiplier for men on edge
KEV = 5       # Multiplier for kings on edge
CRAMP = 5     # Multiplier for cramp

OPENING = 2   # Multipliers for tempo
MIDGAME = -1
ENDGAME = 2
INTACTDOUBLECORNER = 3
## ================================================== ##

## ===================== Positional Dictionaries ========================== ##
# Maps compressed grid indices xi + yi * 8 to internal board indices. All
# valid locations were a click may occur within the confines of the board 
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
## ======================================================================== ##

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
playingRecord = False       # Determines if the recording is being played
playState = 0               # Used for going through the recorded game
playIndex = 0               # Same as above
awaitingSecondJump = False  # For double jump checking - making sure pieces are used correctly
playSpeed = 1000            # The standard speed for play back, 1 second per move
players = []                # Used to determine who or what plays who or what
playerIndexs = []           # 
## ===================================================================================================================================== ##

buttonlist = [
              button(527,303,171,105,"Multi-Player",startmulti),
              button(527,600,171,105,"Exit",exitbutton),
              button(286,303,173,103,"Play-Back",playRecordButton),
              button(286, 450, 173, 105, "VS MiniMax", miniMaxButton),
              button(527, 450, 173, 105, "VS AlphaBeta", alphaBetaButton),
              button(286, 600, 173, 105, "VS NegaScout", negaScoutButton),
              button(527, 750, 173, 105, "Computer Battle", computerBattleButton)   
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