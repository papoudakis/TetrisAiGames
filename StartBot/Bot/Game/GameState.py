from Player import Player 
import copy
class GameState:
    def __init__(self,field,combo,skips,currentPiece,nextPiece,piecePos):
        self.field = copy.deepcopy(field);
        self.combo = 0
        self.skips = 0
        self.currentPiece = currentPiece
        self.nextPiece = nextPiece
        self.piecePos = piecePos
    
    
    def getLegalActions:
        
        
    def printState(self):
        print "Combos : " + str(self.combo) 
        self.field.printField()
        
