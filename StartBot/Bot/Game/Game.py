from Player import Player
from GameState import GameState

class Game:
    def __init__(self):
        self.timebank = 0
        self.timePerMove = 0

        self.enemy = Player()
        self.me = Player()

        self.piece = None
        self.piecePosition = None
        self.nextPiece = None
        self.Round = 0
    
    def getInitGameState(self):
        initState = GameState(self.me.field,self.me.combo,self.me.skips
            ,self.piece,self.nextPiece,self.piecePosition, self.timebank,self.Round)
        return initState

    def nextGameState(self,field,combo,skips,currentPiece,nextPiece,piecePos, timebank,Round):
        nextState =  GameState(field,combo,skips,currentPiece,nextPiece,piecePos, timebank,Round)
        return nextState
