"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, Response, jsonify, request 
from array import  *
from operator import itemgetter
import re
import random
# seed random number generator
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

def WinningLines():
    WinLines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]
    return WinLines

def BadBoard():
     return Response(
        "Please check the board parameter",
        status=400,
    )

def BoardIsValid(stateStr):
    biv = False
    if len(stateStr) > 9:
        return biv
    
    #Game is over
    x = re.findall("[ox]", stateStr) 
    if len(x) == len(stateStr) and len(stateStr) == 9:
        return biv

    #Check for invalid characters
    x = re.findall("[ox\s]", stateStr)
    if len(x) == len(stateStr) and len(stateStr) == 9:
       biv = True

    return biv


def MarkBox(boardState, index):
    bstr = list(boardState)
    bstr[index] = "o"
    return "".join(bstr)

#
def MakeMove(boardState):

    #New game
    corners = [0,2,6,8]
    if(boardState.isspace()):
        sel = random.choice(corners)
        return MarkBox(boardState, sel)

    line = []
    emptyBoxes = []
    #Check what moves are possible
    for i in range(len(boardState)):
        if(boardState[i] ==  ' '):
            emptyBoxes.append(i)

    #only one move left
    if(len(emptyBoxes) == 1):
        return MarkBox(boardState, emptyBoxes[0])

    #Check for win or block move
    for y in range(8):
        line = WinningLines()[y]
        moves = itemgetter(*line)(boardState)
        strMoves = "".join(moves)
        if((strMoves.count('x') == 2 or strMoves.count('o') == 2) and strMoves.find(' ') != -1):
            nm = moves.index(' ')
            nextMove = line[nm]
            return MarkBox(boardState, nextMove)
    
    #Mark opposite corner
    moves = itemgetter(*corners)(boardState)
    strMoves = "".join(moves)
    if(strMoves.find(' ') != -1):
        nextMove = corners[moves.index(' ')]
        return MarkBox(boardState, nextMove)
    
    #Mark middle square in the empty side
    middle = [1,3,5,7]
    moves = itemgetter(*middle)(boardState)
    strMoves = "".join(moves)
    if(strMoves.find(' ') != -1):
        nextMove = middle[moves.index(' ')]
        return MarkBox(boardState, nextMove)


    #for x in emptyBoxes:
        #if(boxes.Count(x) == 1):

#Check if the game is won
def CheckWin(boardState):
    line = []
    for y in range(8):
        line = WinningLines()[y]
        moves = itemgetter(*line)(boardState)
        strMoves = "".join(moves)
        if (strMoves.count('x') == 3 or strMoves.count('o') == 3):
            return True

    return False



@app.route('/ttt/play',  methods=['GET'])
def TTTgame():

    """Make sure we have values for the boardstate"""
    boardState = request.args.get("board", default=None, type=str)
    if boardState is None or not boardState:
           return BadBoard()

    #Make sure values for the boardstate are valid
    boardState = str(boardState).lower()
    if not BoardIsValid(boardState):
        return BadBoard()
    
    win = CheckWin(boardState)

    if not win:
        boardState = MakeMove(boardState)

    return jsonify(boardState)

if __name__ == '__main__':
    #import os
    #HOST = os.environ.get('SERVER_HOST', 'localhost')
    #try:
        #PORT = int(os.environ.get('SERVER_PORT', '5555'))
    #except ValueError:
        #PORT = 5555
    app.run(debug=True, host='0.0.0.0')#(HOST, PORT)


