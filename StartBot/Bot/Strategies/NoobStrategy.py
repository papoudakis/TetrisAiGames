from random import randint
from AbstractStrategy import AbstractStrategy
from Game.GameState import GameState
import time
import copy
#~ from Field import field
class NoobStrategy(AbstractStrategy):
    def __init__(self, game):
        AbstractStrategy.__init__(self, game)

    def choose(self):
        start1 = time.time()
        self.initGameState = self._game.getInitGameState();
        legalFields = self.initGameState.getLegalActions()
        
        bestFields, bestMoves = self.FirstLevelStates(legalFields)
        index = self.SecondLevelStates(bestFields)
        

        #~ bestFields[index].printField()
        #~ print legalFields[best_moves].numOfHoles()
        #~ print legalFields[best_moves].computeBumbiness()
        end1 = time.time()
        print end1 - start1
        return bestMoves[index]
    
    
    def evaluate(self, legalField):
		return 10*legalField.numOfCompleteRows() - 2*legalField.maxHeigth() - 4*legalField.numOfHoles() - 0.5*legalField.computeBumbiness()

    def FirstLevelStates(self,legalFields):
        scores  = []
        fields = []
        moves = []
        
        for move in legalFields.keys():
            field = legalFields[move]
            score = self.evaluate(field)
            scores.append(score)
            fields.append(field)
            moves.append(move)
        
        
        scores_index =  sorted(range(len(scores)), key=lambda k: scores[k])
        scores_index = scores_index[::-1]

        finalFields = []
        finalMoves =[]
        
        MAX_FIELDS = max(5, len(fields))
        for i in range(MAX_FIELDS):
            finalFields.append(fields[scores_index[i]])
            finalMoves.append(moves[scores_index[i]]) 
        return finalFields, finalMoves
        
        
    def SecondLevelStates(self, legalFields):
        best_score = -float('Inf')
        #~ best_Fieds
        for field in legalFields:
            i = 0
            score = []
            nextState = GameState(copy.deepcopy(field), 0, 0,self.initGameState.nextPiece, None, [3, -1])
            legalFields2 = nextState.getLegalActions()
            for f in legalFields2.values():
                score.append(self.evaluate(f))
            max_score = max(score)
            if max_score > best_score:
                index = i
                best_score = max_score
            i = i + 1
        return i
            
