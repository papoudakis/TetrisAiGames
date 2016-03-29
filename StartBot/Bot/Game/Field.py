import copy
import utils
import time
class Field:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.field = [[0]*self.width]*self.height

    def size(self):
        return self.width, self.height

    def updateField(self, field):
        self.field = field

    def projectPieceDown(self, piece, offset):
        piecePositions = self.__offsetPiece(piece.positions(), offset)

        field = None
        for height in range(0, self.height-1):
            tmp = self.fitPiece(piecePositions, [0, height])

            if not tmp:
                break
            field = tmp

        return field
    @staticmethod
    def __offsetPiece(piecePositions, offset):
        piece = copy.deepcopy(piecePositions)
        for pos in piece:
            pos[0] += offset[0]
            pos[1] += offset[1]

        return piece

    def __checkIfPieceFits(self, piecePositions):
        for x,y in piecePositions:
            if 0 <= x < self.width and 0 <= y < self.height:
                if self.field[y][x] > 1 and self.field[y][x] < 4 :
                    return False
            else:
                return False
        return True

    def fitPiece(self, piecePositions, offset=None):
        if offset:
            piece = self.__offsetPiece(piecePositions, offset)
        else:
            piece = piecePositions

        field = copy.deepcopy(self.field)
        if self.__checkIfPieceFits(piece):
            for x,y in piece:
                field[y][x] = 4
            tmpField = Field();
            tmpField.updateField(field)
            return tmpField
        else:
            return None

    def isAttached(self):
        attached = False
        i = -1
        for row in self.field:
            i= i+1
            if 4 in row:
                j = -1
                for x in row:
                    j = j+1
                    if i <19:
                       if x ==4 and self.field[i+1][j] == 2:
                           attached = True
                    else:
                        attached = True
        return attached
    #Returns None if not accesible and the moves if accesible
    def isAccesible(self,Piece,piecePos,targetPos):
        targetPos = (targetPos[0],targetPos[1]+1)
        fringe = utils.PriorityQueue()
        closed = set()
        fringe.push(((tuple(piecePos),Piece.rotateCount()),[],0),0)

        while(True):
            if fringe.isEmpty():
                return None
            state,moves,cost = fringe.pop()
            Piece.updateCount(state[1])
            #~ print len(closed)
            #~ print fringe.size()
            #~ print cost
            #~ print state[1].rotateCount()
            #~ if cost > 1:
                #~ print 'malakas'
                #~ time.sleep(0.1)
            if state[0] == targetPos and state[1]==0:
                return moves
            #~ print state
            if state not in closed:
                closed.add(state)
                successors = self.getSuccessors(state,targetPos,Piece)
                if successors:
                    for next_state,next_move,next_cost in successors:
                        fringe.push((next_state,moves+[next_move] ,next_cost),next_cost)
    
        return moves

    def getSuccessors(self,state,targetPos, Piece):

        piecePos , rot = state
        actions = ['left', 'right', 'turnleft', 'turnright','up']
        succ = []
        for action in actions:
            if action == 'left':
               tmpPos = [piecePos[0]-1,piecePos[1]]
               if self.__checkIfPieceFits(self.__offsetPiece(Piece.positions(),tmpPos)):
                   succ.append(((tuple(tmpPos),Piece.rotateCount()),'left',utils.manhattanDistance(tmpPos,targetPos)))
            if action == 'right':
               tmpPos = [piecePos[0]+1,piecePos[1]]
               if self.__checkIfPieceFits(self.__offsetPiece(Piece.positions(),tmpPos)):
                   succ.append(((tuple(tmpPos),Piece.rotateCount()),'right',utils.manhattanDistance(tmpPos,targetPos)))
            if action == 'up':
               tmpPos = [piecePos[0],piecePos[1]-1]
               if self.__checkIfPieceFits(self.__offsetPiece(Piece.positions(),tmpPos)):
                   succ.append(((tuple(tmpPos),Piece.rotateCount()),'up',utils.manhattanDistance(tmpPos,targetPos)))
            if action == 'turnleft':
               tmpPiece = copy.deepcopy(Piece)
               if tmpPiece.turnLeft():
                   if self.__checkIfPieceFits(self.__offsetPiece(tmpPiece.positions(),piecePos)):
                       succ.append(((piecePos,tmpPiece.rotateCount()),'turnleft',utils.manhattanDistance(piecePos,targetPos)))
            if action == 'turnright':
               tmpPiece = copy.deepcopy(Piece)
               if tmpPiece.turnRight():
                   if self.__checkIfPieceFits(self.__offsetPiece(tmpPiece.positions(),piecePos)):
                       succ.append(((piecePos,tmpPiece.rotateCount()),'turnright',utils.manhattanDistance(piecePos,targetPos)))
           
                #~ temp = [offset - 1, offset + 1]
                #~ boolean = self.__checkIfPieceFits(piecePos)
                
        return succ
        
        
         
        
    def printField(self):
        print '------------Field-------------'
        for row in self.field:
            print row  

