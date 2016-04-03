from random import randint
import sys,os
sys.path.append(os.getcwd() + '/Bot/Game')
from GameState import GameState
from AbstractStrategy import AbstractStrategy
import time
import copy
#~ from Field import field
class NoobStrategy(AbstractStrategy):
    def __init__(self, game):
        AbstractStrategy.__init__(self, game)
        
    def choose(self):
        #~ start1 = time.time()
        self.initGameState = self._game.getInitGameState();
        legalFields = self.initGameState.getLegalActions()
        
        bestFields, bestMoves , bestScores = self.FirstLevelStates(legalFields)
        index = self.SecondLevelStates(bestFields)
        #~ print len(bestFields)
        #~ print len(bestMoves)

        #~ bestFields[index].printField()
        #~ print legalFields[best_moves].numOfHoles()
        #~ print legalFields[best_moves].computeBumbiness()
        #~ end1 = time.time()
        #~ print end1 - start1
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
        finalScores = []
        MAX_FIELDS = min(3, len(fields))
        for i in range(MAX_FIELDS):
            finalFields.append(fields[scores_index[i]])
            finalMoves.append(moves[scores_index[i]])
            finalScores.append(scores[scores_index[i]]) 
            
        return finalFields, finalMoves,finalScores
        
        
    def SecondLevelStates(self, legalFields):
        best_score = -float('Inf')
        i = 0
        index = 0 
        for field in legalFields:
            score = []
            nextState = GameState(copy.deepcopy(field), 0, 0,self.initGameState.nextPiece, None, [3, -1])
            legalFields2 = nextState.getLegalActions()
            for f in legalFields2.values():
                score.append(self.evaluate(f))
            if score:
                max_score = max(score)
            if max_score > best_score:
                index = i
                best_score = max_score
            i = i + 1
        return index
            
