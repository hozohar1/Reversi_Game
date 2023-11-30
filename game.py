
# hodaya zohar

import copy

EMPTY, BLACK, WHITE = '.', '⚫', '○'
HUMAN, COMPUTER = '●', '○'

UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)
VIC = 10000000  # The value of a winning board (for max)
LOSS = -VIC  # The value of a losing board (for max)
TIE = 0  # The value of a tie

'''
The state of the game is represented by a list of 4 items:
0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
   the comp's cells = COMPUTER and the human's = HUMAN
1. The heuristic value of the state.
2. Who's turn is it: HUMAN or COMPUTER
3. flag to end game

'''


# The user decides who plays first
def whoIsFirst(s):
    global HUMAN, COMPUTER
    ans = input("CHOOSE FIRST PLAYER: h/c")  # h for human and c for computer
    if ans == "h":
        s[2] == HUMAN
        HUMAN = '●'
        COMPUTER = '○'
    else:
        s[2] == COMPUTER
        HUMAN = '○'
        COMPUTER = '●'
    return s


def isHumTurn(s):
    # Returns True iff it the human's turn to play
    return s[2] == HUMAN


def squares():
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]


# The HUMAN plays first (=BLACK)
def create():
    global HUMAN, COMPUTER
    board = [EMPTY] * 100
    for i in squares():
        board[i] = EMPTY
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    HUMAN, COMPUTER = '●', '○'
    return [board, 0.00001, HUMAN, False]


def printState(s):
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10 * row + 1, 10 * row + 9
        rep += '%d %s\n' % (row, ' '.join(s[0][begin:end]))
    print(rep)
    if s[1] == VIC:
        print("Ha ha ha I won!")
    elif s[1] == LOSS:
        print("You did it!")
    elif s[1] == TIE:
        print("It's a TIE")


def inputMove(s):
    # Reads, enforces legality and executes the user's move.
    flag = True
    while flag:
        printState(s)
        move = int(
            input("To make your move enter a two digits number, the first number is row and the second is column" "\n" \
                  "For example: if you want to choose the first row and the third column enter 13" "\n" \
                  "Enter your next move: "))
        if isLegal(move, s) == False:
            print("Illegal move.")
        else:
            flag = False
            makeMove(move, s)


def isLegal(move, s):
    hasbracket = lambda direction: findBracket(move, s, direction)
    return s[0][move] == EMPTY and any(map(hasbracket, DIRECTIONS))




'''The given heuristic function calculates the heuristic value for a given state `s` in the Reversi game.
 The heuristic is based on summing up the number of discs for each player and then determining the value of the board
 based on the difference between the number of discs controlled by the computer and the number of discs controlled by the human player.

The heuristic value is obtained by subtracting the number of discs controlled by the human player (`sumPerson`) from the number of discs 
controlled by the computer player (`sumComputer`), and assigning the result to `s[1]`.

If the heuristic value is 0, which indicates a draw or a balanced position, the value is set to 0.001. This is likely
 done to avoid returning exactly 0, which might cause issues with certain algorithms or decision-making processes that
rely on non-zero heuristic values.

The logic behind this heuristic is to prioritize positions where the computer has more discs on the board compared 
to the human player. 
A higher positive heuristic value suggests that the computer is in a favorable position, while a higher negative value
 suggests the human player has the advantage. 
By considering this heuristic value, the computer player can make decisions that aim to maximize its disc count 
and minimize the human player's disc count, ultimately aiming to achieve a more advantageous board position.
'''
def value(s):
    # Returns the heuristic value of s
    # sum the amount of discs then assume the value of the board
    sumComputre = 0 # negative
    sumPerson = 0  # positive
    # sum amount of each player discs
    for i in squares():
        if s[0][i] == HUMAN:
            sumPerson += 1
        if s[0][i] == COMPUTER:
            sumComputre += 1
    s[1] = sumComputre - sumPerson
    # tie is 0 so return 0.001
    if s[1] == 0:
        s[1] = 0.001
    return s[1]







def isFinished(s):
    # if s[3]:
    #    s[1]=VIC if s[0].count(HUMAN)<s[0].count(COMPUTER)else TIE if s[0].count(HUMAN)==s[0].count(COMPUTER) else LOSS
    #   return True
    # if the board is full
    if (s[0].count(HUMAN) + s[0].count(COMPUTER)) == 64:
        s[3] = True
        s[1] = whoWin(s)
        return s[3]
    # if the current player have legal moves
    if len(legalMoves(s)) > 0:
        return False
    # change to other player
    s[2] = HUMAN if s[2] == COMPUTER else COMPUTER
    # if the other player have legal moves
    if len(legalMoves(s)) > 0:
        return False

    # both players have no moves
    s[3] = True
    s[1] = VIC if s[0].count(HUMAN)<s[0].count(COMPUTER)else TIE if s[0].count(HUMAN)==s[0].count(COMPUTER) else LOSS#whoWin(s)
    return s[3]



# get a list of legal moves for the player
def legalMoves(s):
    return [sq for sq in squares() if isLegal(sq, s)]


# Is there any legal move for this player
def anyLegalMove(s):
    isAny = any(isLegal(sq, s) for sq in squares())
    if (not (isAny)):
        s[3] = True
    return isAny


def makeFlips(move, s, direction):
    bracket = findBracket(move, s, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        s[0][square] = s[2]
        square += direction


def changePlayer(s):
    if s[2] == COMPUTER:
        s[2] = HUMAN
    else:
        s[2] = COMPUTER


def makeMove(move, s):
    s[0][move] = s[2]
    for d in DIRECTIONS:
        makeFlips(move, s, d)
    value(s)
    changePlayer(s)
    return s


def whoWin(s):
    computerScore = 0
    humanScore = 0
    for sq in squares():
        piece = s[0][sq]
        if piece == COMPUTER:
            computerScore += 1
        elif piece == HUMAN:
            humanScore += 1
    if (computerScore > humanScore):
        return VIC

    elif (computerScore < humanScore):
        return LOSS

    elif (computerScore == HUMAN):
        return TIE

    return 0.00001  # not 0 because TIE is 0


def isValid(move):
    return isinstance(move, int) and move in squares()


def findBracket(square, s, direction):
    bracket = square + direction
    if s[0][bracket] == s[2]:
        return None
    opp = BLACK if s[2] is WHITE else WHITE
    while s[0][bracket] == opp:
        bracket += direction
    return None if s[0][bracket] in (EMPTY) else bracket


def getNext(s):
    # returns a list of the next states of s
    ns = []
    for m in legalMoves(s):
        tmp = copy.deepcopy(s)
        makeMove(m, tmp)
        ns += [tmp]
    return ns
