import copy

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
                if self.field[y][x] > 1:
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
            #~ print i
            if 4 in row:
                #~ print('AA')
                j = -1
                for x in row:
                    j = j+1
                    #~ print i
                    if i <19:
                       if x ==4 and self.field[i+1][j] == 2:
                           #~ print('AA')
                           attached = True
                    else:
                        attached = True
        return attached
                        
                        
                    
            
         

        
    def printField(self):
        print '------------Field-------------'
        for row in self.field:
            print row  

