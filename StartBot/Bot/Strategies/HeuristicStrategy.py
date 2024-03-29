from random import randint
import sys,os
from AbstractStrategy import AbstractStrategy
import time
import copy

class HeuristicStrategy(AbstractStrategy):
    def __init__(self, game):
        AbstractStrategy.__init__(self, game)
        
    def choose(self):
        
        self.initGameState = self._game.getInitGameState();
        legalFields = self.initGameState.getLegalActions()
        if self.initGameState.skips > 0:
            legalFields[tuple(['skip'])] = self.initGameState.field
            
        bestFields, bestMoves , bestScores = self.FirstLevelStates(legalFields)

    # choose best move based on second field
    
        index = self.SecondLevelStates(bestFields)
        print index
        return bestMoves[index]
    
    
    def evaluate(self, legalField, moves, piece,Round):
        tSpin = legalField.computeTspin(piece, moves)
        complete_rows =  legalField.numOfCompleteRows()
        isDeath = legalField.solidLines(Round)
        if isDeath:
            return -float('Inf'),0
    # compute reward        
        reward = legalField.computeReward(complete_rows, tSpin)
        reward = self.initGameState.combo*(reward>0)  + reward

    # compute features
        heights = legalField.computeHeigths()
        w_heights = [0.5, 0.75, 0.75, 1, 1, 1, 1, 0.75, 0.75, 0.5] 
        agg_heights = sum([a*b for a,b in zip(heights,w_heights)])
        numOfTholes = legalField.checkForTholes()
        numOfHoles, holes = legalField.numOfHoles(heights)
        coastline = legalField.computeCoastLine(holes)
        numOfHoles, holes = legalField.numOfHoles(heights)
        
        return 7*reward - 2*max(heights) - 10*numOfHoles - 2*legalField.computeBumbines(heights)  + 12*legalField.points - 0.2*agg_heights + 8*numOfTholes**2, reward

    def FirstLevelStates(self,legalFields):
        scores  = []
        fields = []
        moves = []
        for move in legalFields.keys():
            field = legalFields[move]
            score, reward = self.evaluate(field,move,self.initGameState.currentPiece,self.initGameState.Round)
            field.updatePoints(reward)
            scores.append(score)
            fields.append(field)
            moves.append(move)
        
        
        scores_index =  sorted(range(len(scores)), key=lambda k: scores[k])
        scores_index = scores_index[::-1]

        finalFields = []
        finalMoves =[]
        finalScores = []
        
        if self.initGameState.hurry:
            MAX_FIELDS = min(3, len(fields))
        else:
            MAX_FIELDS = min(5, len(fields))
            
        for i in range(MAX_FIELDS):
            finalFields.append(fields[scores_index[i]])
            finalMoves.append(moves[scores_index[i]])
            finalScores.append(scores[scores_index[i]]) 
            
        return finalFields, finalMoves,finalScores
        
        
    def SecondLevelStates(self, legalFields):
        best_score = -float('Inf')
        max_score =  -float('Inf')
        i = 0
        index = 0 
        for field in legalFields:
            score = []
            nextState = self._game.nextGameState(copy.deepcopy(field), (self.initGameState.combo+1)*(field.points>0), self.initGameState.skips,self.initGameState.nextPiece, None, [3, -1], self.initGameState.timebank,self.initGameState.Round +1)
            legalFields2 = nextState.getLegalActions()
            for move in legalFields2.keys():
                f = legalFields2[move]
                s = self.evaluate(f, move, nextState.currentPiece,nextState.Round)[0]
                score.append(s)

                
            if score:
                max_score = max(score)
            if max_score > best_score:
                index = i
                best_score = max_score
            i = i + 1
        return index
        
    def report(self, bestFields, bestMoves , bestScores):
        for i in range(len(bestFields)):
            bestFields[i].printField()
            print 'Score:'+ str(bestScores[i])
            
        
