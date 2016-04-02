from random import randint
from AbstractStrategy import AbstractStrategy
import time
#~ from Field import field
class NoobStrategy(AbstractStrategy):
    def __init__(self, game):
        AbstractStrategy.__init__(self, game)
        
        self._actions = ['left', 'right', 'turnleft', 'turnright', 'down', 'drop']

    def choose(self):
        self.initGameState = self._game.getInitGameState();
        #~ ind = [randint(0, 4) for _ in range(1, 10)]
        #~ moves = map(lambda x: self._actions[x], ind)
        #~ moves.append('drop')
        #~ self.initGameState.printState()
        #~ start1 = time.time()
        #~ oldlegalFields = self.initGameState.getLegalActions()
        #~ 
        #~ print 'Number of fields in OldFields is ' + str(len(oldlegalFields))
        #~ start2 = time.time()
        legalFields = self.initGameState.getLegalActions2()
        best_eval = -11111111111111111111111
        #~ bestField = Field()
        for moves in legalFields.keys():
			field = legalFields[moves]
			score = self.evaluate(field)
			if score > best_eval:
				best_eval = score
				best_moves = moves
        #~ end2 = time.time()
        #~ print 'Number of fields in NewFields is ' + str(len(newLegalFields))
       #~ 
        #~ print 'Old Fields completed Calculations in ' + str(-start1+end1)
        #~ print 'New Fields completed Calculations in ' + str(-start2 +end2)
        #~ legalFields[best_moves].printField()
        #~ print legalFields[best_moves].numOfHoles()
        #~ print legalFields[best_moves].computeBumbiness()
        #~ end1 = time.time()
        #~ print end1 - start1
        return best_moves
    
    
    def evaluate(self, legalField):
		return 10*legalField.numOfCompleteRows() - 2*legalField.maxHeigth() - 4*legalField.numOfHoles() - 0.5*legalField.computeBumbiness()
		
