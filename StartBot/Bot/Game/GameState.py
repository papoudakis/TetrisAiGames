from Player import Player 
import utils
import copy
class GameState:
    def __init__(self,field,combo,skips,currentPiece,nextPiece,piecePos):
        self.field = copy.deepcopy(field);
        self.combo = 0
        self.skips = 0
        self.currentPiece = currentPiece
        self.nextPiece = nextPiece
        self.piecePos = piecePos
    
    
    def getLegalActions(self):
        legalFields = {};
        for x in range(0,self.field.width):
            for y in range(-1,self.field.height-1):
                #~ if self.field.field[y][x] == 0:
                tmpPiece = copy.deepcopy(self.currentPiece)
                for rot in range(0,len(tmpPiece._rotations)):
                    cool = tmpPiece.turnRight(rot)
                    if not cool:
                        print 'Rotation Failed'
                        exit()
                    piecePos = tmpPiece.positions()
                    # Check if it fits
                    tmpField = self.field.fitPiece(piecePos,[x,y])
                    if  tmpField:
                        #Check if it is not in the air
                        if tmpField.isAttached():
                            #Check if it is accesible
                            moves = tmpField.isAccesible(copy.deepcopy(tmpPiece),[x,y],self.piecePos)
                            #~ print moves
                            if moves:
                                legalFields[(x,y,rot)] = tmpField  
                                tmpField.printField()
                                print moves

                                
    def printState(self):
        
        print "Combos : " + str(self.combo) 
        self.field.printField()
        