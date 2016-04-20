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
        
    def initEveryThing(self):
        self.weigths = [50, -0.5, -10, 10, -1, 3]
        self.alpha = 0.5
        self.discount = 0.8
        
    def choose(self):
        #~ start1 = time.time()
        self.initEveryThing()
        print 'ante geia'
        self.initGameState = self._game.getInitGameState();
        #~ self.initGameState.field.printField()
        legalFields = self.initGameState.getLegalActions()
        if self.initGameState.skips > 0:
            legalFields[tuple(['skip'])] = self.initGameState.field
        
        return  self.getValue(legalFields, self.initGameState.currentPiece, self.initGameState.Round)
    
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
        
        feature.append(tSpin)
        feature.append(agg_heights)
        feature.append(numOfHoles)
        feature.append(numOfTholes**2)
        feature.append(coastline)
        feature.append(semiCompleteRows**2*(semiCompleteRows>1))
        return features
    
    def getQValue(self, legalFields, moves, piece,Round):
    # evalute a field based on moves 
        qValue = 0.0
        features = self.computefeatures(copy.deepcopy(legalFields[moves]), moves, piece, Round)
        for i in range(len(features)):
            qValue += (self.weights[i] * features[i])
        return qValue
        
    
    def getValue(self, legalFields, piece, Round):
        # Evaluate all field and choose the best
        possibleStateQValues = {}
        for moves in legalFields.keys():
            possibleStateQValues[moves] = self.getQValue(legalFields, moves, piece,Round)
        
        return max(possibleStateQValues, key=possibleStateQValues.get)
    
    
    def update(self, legalFields, moves, piece, Round, nextState, reward):
        
    #  Should update your weights based on transition
        
        features = self.computefeatures(legalFields[moves], moves, piece,Round)
        for i in range(len(features)):
            # getValues should be fixed !!!!!!!!!!!!!!!!
            self.weights[i] += self.alpha * (reward + self.discount * self.getValue(legalFields, piece, Round) - self.getQValue(legalFields, moves, piece, Round) * features[i])
        return moves    
