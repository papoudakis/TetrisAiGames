import copy
import utils
import time
class Field:
    def __init__(self,points):
        self.width = 10
        self.height = 20
        self.field = [[0]*self.width]*self.height
        self.points = points
        self.rowsReward = { 0 : 0 ,1 : 0, 2 : 3 , 3 : 6, 4 : 10, 'all': 18}

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
        
    def updatePoints(self,points):
        self.points = points
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
                if self.field[y][x] > 1:
                    return False
            else:
                return False
        return True

    def __checkIfPieceFits2(self, piecePositions):
        for x,y in piecePositions:
            if y == -1:
               continue
            elif 0 <= x < self.width and -1 <y < self.height :
                if self.field[y][x] > 1:
                    return False
            else:
                return False
        return True
    
    
    def __checkIfPieceAttaches(self,piecePositions):
        attached = False
        for x,y in piecePositions:
            if 0 <= x < self.width and 0 <= y < self.height:
                if  y == 19 or self.field[y+1][x] > 1 :
                    attached = True
        return attached

    

    def fitPiece(self, piecePositions, offset=None):
        if offset:
            piece = self.__offsetPiece(piecePositions, offset)
        else:
            piece = piecePositions

        field = copy.deepcopy(self.field)
        if self.__checkIfPieceFits(piece):
            for x,y in piece:
                field[y][x] = 4
            tmpField = Field(self.points);
            tmpField.updateField(field)
            return tmpField
        else:
            return None
    
    def isFit(self,piecePositions,offset):
        piece = self.__offsetPiece(piecePositions, offset)
        if self.__checkIfPieceFits(piece):
            if self.__checkIfPieceAttaches(piece):
                return True
        
        return False
         


    #Returns None if not accesible and the moves if accesible
    def isAccesible(self,Piece,piecePos,targetPos):
        targetPos = (targetPos[0],targetPos[1])
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
                #~ moves.append('down')
                moves = moves[::-1]
                return moves
            #~ print state
            if state not in closed:
                closed.add(state)
                successors = self.getSuccessors(state,targetPos,Piece)
                if successors:
                    for next_state,next_move,next_cost in successors:
                        fringe.push((next_state,moves+[next_move] ,next_cost),next_cost)
        #~ moves.append('down')
        moves = moves[::-1]
        print moves
        return moves

    def getSuccessors(self,state,targetPos, Piece):

        piecePos , rot = state
        actions = ['left', 'right', 'turnleft', 'turnright','up']
        succ = []
        for action in actions:
            if action == 'left':
               tmpPos = [piecePos[0]-1,piecePos[1]]
               if self.__checkIfPieceFits2(self.__offsetPiece(Piece.positions(),tmpPos)):
                   succ.append(((tuple(tmpPos),Piece.rotateCount()),'right',utils.manhattanDistance(tmpPos,targetPos)))
            if action == 'right':
               tmpPos = [piecePos[0]+1,piecePos[1]]
               if self.__checkIfPieceFits2(self.__offsetPiece(Piece.positions(),tmpPos)):
                   succ.append(((tuple(tmpPos),Piece.rotateCount()),'left',utils.manhattanDistance(tmpPos,targetPos)))
            if action == 'up':
               tmpPos = [piecePos[0],piecePos[1]-1]
               if self.__checkIfPieceFits2(self.__offsetPiece(Piece.positions(),tmpPos)):
                   succ.append(((tuple(tmpPos),Piece.rotateCount()),'down',utils.manhattanDistance(tmpPos,targetPos)))
            if action == 'turnleft':
               tmpPiece = copy.deepcopy(Piece)
               if tmpPiece.turnLeft():
                   if self.__checkIfPieceFits2(self.__offsetPiece(tmpPiece.positions(),piecePos)):
                       succ.append(((piecePos,tmpPiece.rotateCount()),'turnright',utils.manhattanDistance(piecePos,targetPos)))
            if action == 'turnright':
               tmpPiece = copy.deepcopy(Piece)
               if tmpPiece.turnRight():
                   if self.__checkIfPieceFits2(self.__offsetPiece(tmpPiece.positions(),piecePos)):
                       succ.append(((piecePos,tmpPiece.rotateCount()),'turnleft',utils.manhattanDistance(piecePos,targetPos)))
           
                #~ temp = [offset - 1, offset + 1]
                #~ boolean = self.__checkIfPieceFits(piecePos)
                
        return succ
    
    def getPoints(self):
        return self.points
        
    def maxHeigth(self):
        for row in self.field:
			if 4 in row or 2 in row:
				return self.height - self.field.index(row) + 1
	
    def numOfCompleteRows(self):
        completeRows = 0
        perfect_clear = True
        for row in self.field:
            if 0  not in row and 3 not in row:
                completeRows = completeRows + 1
                self.field.pop(self.field.index(row))
                self.field.insert(0, [0,0,0,0,0,0,0,0,0,0])
        if (4 in row for row in self.field )or (2 in row for row in self.field):
            perfect_clear = False
                
        if perfect_clear:
            dict_key = 'all'
        else:
            dict_key = completeRows
        
        return completeRows, self.rowsReward[dict_key]

    def numOfHoles(self,heights):
        holes = 0
        for i in range(self.width):
            found = False
            counter = 0
            for j in range(self.height):
                if self.field[j][i] > 1 :
                    found = True
                   
                if found and self.field[j][i]==0:
                    if i ==0 and heights[i+1]>= self.height - j:
                        counter = counter + 1
                        print str(i) + ',' + str(j)
                    elif i == self.width -1 and heights[i-1]>=self.height -j:
                        counter = counter +1
                        print str(i) + ',' + str(j)
                    elif i!=0 and i != self.width - 1 and heights[i-1] >= self.height -j and heights[i+1] >=self.height -j:
                        counter = counter +1
                        print str(i) + ',' + str(j)
                if not found and self.field[j][i]==0:
                    if i == 0 and heights[i+1] > self.height -j and self.field[j][i + 1] == 0:
                        counter = counter +1
                        print str(i) + ',' + str(j)
                    elif i == self.width - 1 and heights[i-1] > self.height - j and self.field[j][i - 1] == 0:
                        counter = counter +1
                        print str(i) + ',' + str(j)
                    elif i!=0 and i != self.width - 1:
                    #~ and  heights[i-1] >  self.height - 1- j and heights[i+1] > self.height -1-j:
                        if self.field[j][i - 1] == 0 and heights[i+1] >= self.height -j and  heights[i-1] > self.height - j:
                            counter = counter +1
                            print str(i) + ',' + str(j)
                        if self.field[j][i + 1] == 0 and heights[i-1] >= self.height -j and heights[i+1] > self.height -j:
                            counter = counter +1
                            print str(i) + ',' + str(j)
            holes = holes + counter	
        return holes


    def computeHeigths(self):
        heights = list([0]*self.width)
        for i in range(self.width):
            for j in range(self.height):
                if self.field[j][i] > 1:
                    heights[i] = self.height - j
                    break
        return heights
                    
    def computeBumbines(self,heights):
        diffs = [abs(j-i) for i, j in zip(heights[:-1], heights[1:])]
        return sum(diffs)
        
    def printField(self):
        print '------------Field-------------'
        for row in self.field:
            print row  

   
