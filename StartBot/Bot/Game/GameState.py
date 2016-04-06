from Player import Player 
import utils
import copy

class GameState:
    def __init__(self,field,combo,skips,currentPiece,nextPiece,piecePos, timebank):
        self.field = copy.deepcopy(field);
        self.combo = combo
        self.skips = skips
        self.currentPiece = currentPiece
        self.nextPiece = nextPiece
        self.piecePos = piecePos
        self.timebank = timebank
        self.hurry = False
        if self.timebank < 3000:
            self.hurry = True
            
        
    def getLegalActions(self):
        legalFields = { }
        #~ legalMoves = { }
        for x in range(-2,self.field.width):
            for y in range(-2,self.field.height):
                for rot in range(0,len(self.currentPiece._rotations)):
                    piecePos = self.currentPiece._rotations[rot]
                    if self.field.isFit(piecePos,[x,y]):
                        tmpPiece = copy.deepcopy(self.currentPiece)
                        tmpPiece.updateCount(rot)
                        moves = self.field.isAccesible(tmpPiece,[x,y],self.piecePos)
                        if moves:
                            legalFields[tuple(moves)] = self.field.fitPiece(piecePos,[x,y])
        return legalFields
                                
    def printState(self):
        
        print "Combos : " + str(self.combo) 
        print "Skips  : " + str(self.skips)
        self.field.printField()
        
        
        
