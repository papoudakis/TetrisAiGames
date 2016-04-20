from random import randint
import sys,os
sys.path.append("/home/konstantinos/AiGames/TetrisAiGames/StartBot/Bot/Game")
sys.path.append("/home/giorgos/University/TetrisAiGames/StartBot/Bot/Game")
sys.path.append("/home/argiris/Desktop/TetrisAiGames/StartBot/Bot/Game")
sys.path.append(os.getcwd() + '/Bot/Game')
sys.path.append("/src/StartBot/Bot/Game")
from GameState import GameState
from AbstractStrategy import AbstractStrategy
import time
import copy


class QLearningStrategy(AbstractStrategy):
    
    def __init__(self, game):
        AbstractStrategy.__init__(self, game)        
        #~ self.weights = [50, -0.5, -10, 10, -1, 3]
        self.weights = [50.0, -1.1730124359580474, -9.96388286249445, 9.977906246576895, -0.2072693538683254, 2.8544003030622247]
        self.alpha = 0.0001
        self.discount = 0.5
        
    def choose(self):
        #~ start1 = time.time()
        #~ self.initEveryThing()
        #~ print 'ante geia'
        self.initGameState = self._game.getInitGameState();
        #~ self.initGameState.field.printField()
        legalFields = self.initGameState.getLegalActions()
        if self.initGameState.skips > 0:
            legalFields[tuple(['skip'])] = self.initGameState.field
        
        best_val, moves = self.getValue(legalFields, self.initGameState.currentPiece, self.initGameState.Round)
        tSpin = legalFields[moves].computeTspin(self.initGameState.currentPiece, moves)
        complete_rows =  legalFields[moves].numOfCompleteRows()
        reward = legalFields[moves].computeReward(complete_rows, tSpin)
        reward = self.initGameState.combo*(reward>0)  + reward
        reward = reward - max(legalFields[moves].computeHeigths())/3
        self.update(legalFields, moves, self.initGameState.currentPiece, self.initGameState.Round, reward)
        return moves
        
    def computeFeatures(self, legalField, moves, piece,Round):
        # Compute values of features and store them in a list
        
        features = []
        tSpin = legalField.computeTspin(piece, moves)
        complete_rows =  legalField.numOfCompleteRows()
        #~ isDeath = legalField.solidLines(Round)
        #~ if isDeath:
            #~ return -float('Inf'),0
            #~ 
        #~ reward = legalField.computeReward(complete_rows, tSpin)
        #~ reward = self.initGameState.combo*(reward>0)  + reward
        heights = legalField.computeHeigths()
        w_heights = [0.5, 0.75, 0.75, 1, 1, 1, 1, 0.75, 0.75, 0.5] 
        agg_heights = sum([a*b for a,b in zip(heights,w_heights)])
        numOfTholes = legalField.checkForTholes()
        #~ print legalField.computeCostLine(heights)
        
        #~ print numOfTholes
        #~ print agg_heights
        #~ agg_heights2 = sum([a - min(agg_heights) for a in agg_heights])
        #~ numOfHoles, holes = legalField.numOfHoles(heights)
        #~ coastline = legalField.computeCoastLine(holes)
        #~ return 7*reward - 2*max(heights) - 10*numOfHoles - 2*legalField.computeBumbines(heights)  + 12*legalField.points - 0.2*agg_heights + 8*numOfTholes**2, reward
        numOfHoles, holes = legalField.numOfHoles(heights)
        coastline = legalField.computeCoastLine(holes)
        semiCompleteRows = legalField.computeSemiCompleteRows(holes)
        
        features.append(tSpin)
        features.append(agg_heights)
        features.append(numOfHoles)
        features.append(numOfTholes**2)
        features.append(coastline)
        features.append(semiCompleteRows**2*(semiCompleteRows>1))
        return features
    
    def getQValue(self, legalFields, moves, piece,Round):
    # evalute a field based on moves 
        qValue = 0.0
        features = self.computeFeatures(copy.deepcopy(legalFields[moves]), moves, piece, Round)
        for i in range(len(features)):
            qValue += (self.weights[i] * features[i])
        return qValue
        
    
    def getValue(self, legalFields, piece, Round):
        # Evaluate all field and choose the best
        possibleStateQValues = {}
        for moves in legalFields.keys():
            possibleStateQValues[moves] = self.getQValue(legalFields, moves, piece,Round)
        
        return max(possibleStateQValues.values()), max(possibleStateQValues, key=possibleStateQValues.get)
    
    
    def update(self, legalFields, moves, piece, Round, reward):
        
    #  Should update your weights based on transition
        
        features = self.computeFeatures(legalFields[moves], moves, piece,Round)
        
        
        
        nextState = GameState(copy.deepcopy(legalFields[moves]), (self.initGameState.combo+1)*(legalFields[moves].points>0), self.initGameState.skips,self.initGameState.nextPiece, None, [3, -1], self.initGameState.timebank,self.initGameState.Round +1)
        legalFields2 = nextState.getLegalActions()
        bestQValue, bst_moves = self.getValue(legalFields2, nextState.currentPiece, nextState.Round)
        
        for i in range(len(features)):
            # getValues should be fixed !!!!!!!!!!!!!!!!
            
            self.weights[i] += self.alpha * (reward + self.discount * bestQValue  - self.getQValue(legalFields, moves, piece, Round)) * features[i]
        sys.stderr.write(str(self.weights) + '\n')
