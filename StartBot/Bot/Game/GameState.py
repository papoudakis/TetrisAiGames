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
        k = 0
        for x in range(-2,self.field.width):
            for y in range(-2,self.field.height):
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
                                #~ tmpField.printField()
                                #~ print moves
        #~ print 'Number of fields is ' + str(k)
        return legalFields
        
    def getLegalActions2(self):
        legalFields = { }
        for x in range(-2,self.field.width):
            for y in range(-2,self.field.height):
                for rot in range(0,len(self.currentPiece._rotations)):
                    piecePos = self.currentPiece._rotations[rot]
                    if self.field.isFit(piecePos,[x,y]):
                        #~ print 'AAAAAAAAAA'
                        moves = self.field.isAccesible(copy.deepcopy(self.currentPiece),[x,y],self.piecePos)
                        if moves:
                            legalFields[(x,y,rot)] = self.field.fitPiece(piecePos,[x,y])
        return legalFields
                                
    def printState(self):
        
        print "Combos : " + str(self.combo) 
        print "Skips  : " + str(self.skips)
        self.field.printField()
        
