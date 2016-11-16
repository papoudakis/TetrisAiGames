from random import randint
import sys,os
from AbstractStrategy import AbstractStrategy
import time
import copy
import re
import random


class QLearningStrategy(AbstractStrategy):
    
    def __init__(self, game):
        AbstractStrategy.__init__(self, game)
        self.reward = 0
        if not os.path.exists("weights.txt"):
            fl = open('weights.txt', 'w')
        else:
            fl = open('weights.txt', 'r')
        weights_str = fl.readline()
        
        weights_str = weights_str[1:-1]#remove brackets
        weights_str = weights_str.split(',')
        try:
            self.weights = [float(w) for w in  weights_str]
        except ValueError:
            self.weights = [0 for i in range(8)]             
        self.alpha = 0.0001
        self.discount = 0
        
        fl.close()
        
    def choose(self):
        self.initGameState = self._game.getInitGameState();
        legalFields = self.initGameState.getLegalActions()
        if self.initGameState.skips > 0:
            legalFields[tuple(['skip'])] = self.initGameState.field
        
        best_val, moves = self.getValue(legalFields, self.initGameState.currentPiece, self.initGameState.Round)
        sys.stderr.write('Best_val:' + str(best_val) +' ')
        if moves == tuple(['drop']):
            return moves
            
        reward = self.computeReward(copy.deepcopy(legalFields[moves]),moves)
        self.reward += reward
        self.update(legalFields, moves, self.initGameState.currentPiece, self.initGameState.Round, reward)
        f = open('weights.txt','w')
        f.write(str(self.weights))
        f.close()
        
        return moves
        
    def computeReward(self,legalField,moves):
        tSpin = legalField.computeTspin(self.initGameState.currentPiece, moves)
        complete_rows =  legalField.numOfCompleteRows()
        heights = legalField.computeHeigths()
        reward = legalField.computeReward(complete_rows, tSpin)
        reward = self.initGameState.combo*(reward>0)  + reward  
        reward = reward - max(heights)
        sys.stderr.write('Reward:' + str(self.reward) + '\n')
        return reward
        
    def computeFeatures(self, legalField, moves, piece,Round):
        # Compute values of features and store them in a list
        
        features = []
        tSpin = legalField.computeTspin(piece, moves)
        complete_rows =  legalField.numOfCompleteRows()
        reward = legalField.computeReward(complete_rows, tSpin)
        reward = self.initGameState.combo*(reward>0)  + reward
        heights = legalField.computeHeigths()
        w_heights = [0.5, 0.75, 0.75, 1, 1, 1, 1, 0.75, 0.75, 0.5] 
        agg_heights = sum([a*b for a,b in zip(heights,w_heights)])
        numOfTholes = legalField.checkForTholes()
        numOfHoles, holes = legalField.numOfHoles(heights)
        coastline = legalField.computeCoastLine(holes)
        bumbiness = legalField.computeBumbines(heights)
        semiCompleteRows = legalField.computeSemiCompleteRows(holes)
        features.append(max(heights))
        features.append(numOfHoles)
        features.append(bumbiness)
        features.append(complete_rows)
        features.append(tSpin)
        features.append(numOfTholes**2)
        features.append(coastline)
        features.append(semiCompleteRows**2*(semiCompleteRows>1))
        return features
    
    def getQValue(self, legalFields, moves, piece,Round):
    # evalute a field based on moves 
        qValue = 0.0
        tempField = copy.deepcopy(legalFields[moves])
        features = self.computeFeatures(tempField, moves, piece, Round)
        for i in range(len(features)):
            qValue += (self.weights[i] * features[i])
        return qValue
        
    
    def getValue(self, legalFields, piece, Round):
        # Evaluate all field and choose the best
        possibleStateQValues = {}
        for moves in legalFields.keys():
            possibleStateQValues[moves] = self.getQValue(legalFields, moves, piece,Round)
        if len(possibleStateQValues.keys())==0:
            return 0, tuple(['drop'])
        else:
            return max(possibleStateQValues.values()), max(possibleStateQValues, key=possibleStateQValues.get)
    
        
    def update(self, legalFields, moves, piece, Round, reward):
        
    #  Should update your weights based on transition
        
        features = self.computeFeatures(legalFields[moves], moves, piece,Round)
        nextState = self._game.nextGameState(legalFields[moves], (self.initGameState.combo+1)*(legalFields[moves].points>0), self.initGameState.skips,self.initGameState.nextPiece, None, [3, -1], self.initGameState.timebank,self.initGameState.Round +1)
        legalFields2 = nextState.getLegalActions()
        bestQValue, bst_moves = self.getValue(legalFields2, nextState.currentPiece, nextState.Round)
        
        for i in range(len(features)):            
            self.weights[i] += self.alpha * (reward + self.discount * bestQValue  - self.getQValue(legalFields, moves, piece, Round)) * features[i]

