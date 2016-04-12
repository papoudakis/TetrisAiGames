from random import randint
import sys,os
sys.path.append("/home/konstantinos/AiGames/TetrisAiGames/StartBot/Bot/Game")
sys.path.append(os.getcwd() + '/Bot/Game')
sys.path.append("/src/StartBot/Bot/Game")
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
        #~ self.initGameState.field.printField()
        legalFields = self.initGameState.getLegalActions()
        if self.initGameState.skips > 0:
            legalFields[tuple(['skip'])] = self.initGameState.field
            
        bestFields, bestMoves , bestScores = self.FirstLevelStates(legalFields)
        #~ self.report(bestFields,bestMoves,bestScores)
        index = self.SecondLevelStates(bestFields)
        #~ print len(bestFields)
        #~ print len(bestMoves)

        #~ print 'Chosen field ...'
        #~ bestFields[index].printField()
        #~ print bestFields[index].numOfHoles(bestFields[index].computeHeigths())
        #~ print bestFields[index].computeHeigths()
        #~ print bestFields[index].computeBumbines(bestFields[index].computeHeigths())
        #~ end1 = time.time()
        #~ print end1 - start1
        return bestMoves[index]
    
    
    def evaluate(self, legalField, moves, piece,Round):
        tSpin = legalField.computeTspin(piece, moves)
        complete_rows =  legalField.numOfCompleteRows()
        isDeath = legalField.solidLines(Round)
        if isDeath:
            return -float('Inf'),0
            
        reward = legalField.computeReward(complete_rows, tSpin)
        reward = self.initGameState.combo*(reward>0)  + reward
        heights = legalField.computeHeigths()
        w_heights = [0.5, 0.75, 0.75, 1, 1, 1, 1, 0.75, 0.75, 0.5] 
        agg_heights = sum([a*b for a,b in zip(heights,w_heights)])
        numOfTholes = legalField.checkForTholes()
        
        #~ print numOfTholes
        #~ print agg_heights
        #~ agg_heights2 = sum([a - min(agg_heights) for a in agg_heights])
        return 7*reward - 2*max(heights) - 10*legalField.numOfHoles(heights) - 2*legalField.computeBumbines(heights)  + 12*legalField.points - 0.2*agg_heights + 8*numOfTholes**2, reward


    def FirstLevelStates(self,legalFields):
        scores  = []
        fields = []
        moves = []
        for move in legalFields.keys():
            field = legalFields[move]
            score, reward = self.evaluate(field,move,self.initGameState.currentPiece,self.initGameState.Round)
            field.updatePoints(reward)
            #~ print move
            #~ field.printField()
            #~ print score
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
            
        for i in range(5):
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
            nextState = GameState(copy.deepcopy(field), (self.initGameState.combo+1)*(field.points>0), self.initGameState.skips,self.initGameState.nextPiece, None, [3, -1], self.initGameState.timebank,self.initGameState.Round +1)
            legalFields2 = nextState.getLegalActions()
            #~ print 'First Field'
            #~ field.printField()
            #~ print field.points
            for move in legalFields2.keys():
                f = legalFields2[move]
                s = self.evaluate(f, move, nextState.currentPiece,nextState.Round)[0]
                score.append(s)
                #~ print 'Child field'
                #~ print s
                
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
    #~ def report
            
        
