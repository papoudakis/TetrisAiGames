
def create(type):
    switcher = {
        "L": LPiece(),
        "O": OPiece(),
        "I": IPiece(),
        "J": JPiece(),
        "S": SPiece(),
        "T": TPiece(),
        "Z": ZPiece(),
        "H": HPiece()
    }

    return switcher.get(type.upper())

class Piece:
    def __init__(self):
        self._rotateIndex = 0
        self._rotations = []

    def turnLeft(self, times=1):
        if self._rotateIndex > times-1:
            self._rotateIndex -= times
            return True
        return False

    def turnRight(self, times=1):
        if self._rotateIndex < len(self._rotations) - times:
            self._rotateIndex += times
            return True
        return False

    def rotateCount(self):
        return self._rotateIndex

    def updateCount(self, rot):
        self._rotateIndex = rot

    def positions(self):
        return self._rotations[self._rotateIndex]
    
    def appendRotation(self, rotation):
        self._rotations.append(rotation)

class LPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        # rotations ordered by their rotation to the right
        self._rotations.append([[2, 0], [0, 1], [1, 1], [2, 1]])
        self._rotations.append([[1, 0], [1, 1], [1, 2], [2, 2]])
        self._rotations.append([[0, 1], [1, 1], [2, 1], [0, 2]])
        self._rotations.append([[0, 0], [1, 0], [1, 1], [1, 2]])
    def returnType(self):
        return 'L'
        
class OPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        self._rotations.append([[0, 0], [1, 0], [0, 1], [1, 1]])
    def returnType(self):
        return 'O'

        
class IPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        # rotations ordered by their rotation to the right
        self._rotations.append([[0, 1], [1, 1], [2, 1], [3, 1]])
        self._rotations.append([[2, 0], [2, 1], [2, 2], [2, 3]])
        # self._rotations.append([[0, 2], [1, 2], [2, 2], [3, 2]])
        # self._rotations.append([[1, 0], [1, 1], [1, 2], [1, 3]])
    def returnType(self):
        return 'I'

class JPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        # rotations ordered by their rotation to the right
        self._rotations.append([[0, 0], [0, 1], [1, 1], [2, 1]])
        self._rotations.append([[1, 0], [2, 0], [1, 1], [1, 2]])
        self._rotations.append([[0, 1], [1, 1], [2, 1], [2, 2]])
        self._rotations.append([[1, 0], [1, 1], [0, 2], [1, 2]])
    def returnType(self):
        return 'J'

class SPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        # rotations ordered by their rotation to the right
        self._rotations.append([[1, 0], [2, 0], [0, 1], [1, 1]])
        self._rotations.append([[1, 0], [1, 1], [2, 1], [2, 2]])
        # self._rotations.append([[1, 1], [2, 1], [0, 2], [1, 2]])
        # self._rotations.append([[0, 0], [0, 1], [1, 1], [1, 2]])
    def returnType(self):
        return 'S'

class TPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        # rotations ordered by their rotation to the right
        self._rotations.append([[1, 0], [0, 1], [1, 1], [2, 1]])
        self._rotations.append([[1, 0], [1, 1], [2, 1], [1, 2]])
        self._rotations.append([[0, 1], [1, 1], [2, 1], [1, 2]])
        self._rotations.append([[1, 0], [0, 1], [1, 1], [1, 2]])

    def returnType(self):
        return 'T'

class ZPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        self._rotations.append([[0, 0], [1, 0], [1, 1], [2, 1]])
        self._rotations.append([[2, 0], [1, 1], [2, 1], [1, 2]])
        # self._rotations.append([[0, 1], [1, 1], [1, 2], [2, 2]])
        # self._rotations.append([[1, 0], [0, 1], [1, 1], [0, 2]])
    def returnType(self):
        return 'Z'

class HPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        self._rotations.append([[0, 0]])
        #~ self._rotations.append([[0, 0], [1, 0]])
