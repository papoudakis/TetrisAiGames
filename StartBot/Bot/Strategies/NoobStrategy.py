from random import randint
from AbstractStrategy import AbstractStrategy
import time

class NoobStrategy(AbstractStrategy):
    def __init__(self, game):
        AbstractStrategy.__init__(self, game)
        
        self._actions = ['left', 'right', 'turnleft', 'turnright', 'down', 'drop']

    def choose(self):
        self.initGameState = self._game.getInitGameState();
        ind = [randint(0, 4) for _ in range(1, 10)]
        moves = map(lambda x: self._actions[x], ind)
        moves.append('drop')
        #~ self.initGameState.printState()
        start1 = time.time()
        oldlegalFields = self.initGameState.getLegalActions()
        end1 = time.time()
        print 'Number of fields in OldFields is ' + str(len(oldlegalFields))
        start2 = time.time()
        newLegalFields = self.initGameState.getLegalActions2()
        end2 = time.time()
        print 'Number of fields in NewFields is ' + str(len(newLegalFields))
       
        print 'Old Fields completed Calculations in ' + str(-start1+end1)
        print 'New Fields completed Calculations in ' + str(-start2 +end2)
        return moves
