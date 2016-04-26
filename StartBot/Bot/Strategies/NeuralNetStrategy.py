import numpy as np
from random import randint
import sys,os
sys.path.append("/home/konstantinos/AiGames/TetrisAiGames/StartBot/Bot/Game")
sys.path.append("/home/argiris/Desktop/TetrisAiGames/StartBot/Bot/Game")
sys.path.append(os.getcwd() + '/Bot/Game')
sys.path.append("/src/StartBot/Bot/Game")
from GameState import GameState
from AbstractStrategy import AbstractStrategy
import time
import copy

class NeuralNetStrategy(AbstractStrategy):
    
    def __init__(self, game):
        AbstractStrategy.__init__(self, game)
        self.W1 = np.random.rand(200, 50)
        self.W2 = np.random.rand(50, 1)
        
        self.alpha = 0.0001
        self.discount = 0.9
        
    
    def choose(self):
        self.initGameState = self._game.getInitGameState();
        #~ self.initGameState.field.printField()
        legalFields = self.initGameState.getLegalActions()
        if self.initGameState.skips > 0:
            legalFields[tuple(['skip'])] = self.initGameState.field
        
        best_val, moves = self.getValue(legalFields, self.initGameState.currentPiece, self.initGameState.Round)
        #~ sys.stderr.write('Best_val:' + str(best_val) +' ')
        if moves == tuple(['drop']):
            return moves
            
        reward = self.computeReward(copy.deepcopy(legalFields[moves]),moves)

        self.update(legalFields, moves, self.initGameState.currentPiece, self.initGameState.Round, reward)
        #~ f = open('weights.txt','w')
        #~ f.write(str(self.weights))
        #~ f.close()
        
        return moves
        
    def computeReward(self,legalField,moves):
        tSpin = legalField.computeTspin(self.initGameState.currentPiece, moves)#???????
        complete_rows =  legalField.numOfCompleteRows()
        heights = legalField.computeHeigths()
        numOfTholes = legalField.checkForTholes()
        numOfHoles, holes = legalField.numOfHoles(heights)
        semiCompleteRows = legalField.computeSemiCompleteRows(holes)
        reward = legalField.computeReward(complete_rows, tSpin)
        reward = self.initGameState.combo*(reward>0)  + reward  
        reward = (3*reward + complete_rows**2)*(complete_rows > 0) + numOfTholes**2 - (max(heights)/3.0)*(complete_rows==0 and numOfTholes==0)
        #~ sys.stderr.write('Reward:' + str(reward) + '\n')
        return reward
        
    #~ def computeFeatures(self, legalField, moves, piece,Round):
        #~ # Compute values of features and store them in a list
        #~ 
        #~ features = []
        #~ tSpin = legalField.computeTspin(piece, moves)
        #~ complete_rows =  legalField.numOfCompleteRows()
        #~ isDeath = legalField.solidLines(Round)
        #~ if isDeath:
            #~ return -float('Inf'),0
            #~ 
        #~ reward = legalField.computeReward(complete_rows, tSpin)
        #~ reward = self.initGameState.combo*(reward>0)  + reward
        #~ heights = legalField.computeHeigths()
        #~ w_heights = [0.5, 0.75, 0.75, 1, 1, 1, 1, 0.75, 0.75, 0.5] 
        #~ agg_heights = sum([a*b for a,b in zip(heights,w_heights)])
        #~ agg_heights = sum(heights)
        #~ numOfTholes = legalField.checkForTholes()
        #~ numOfHoles, holes = legalField.numOfHoles(heights)
        #~ coastline = legalField.computeCoastLine(holes)
        #~ bumbiness = legalField.computeBumbines(heights)
        #~ semiCompleteRows = legalField.computeSemiCompleteRows(holes)
        #~ features.append(reward)
        #~ features.append(max(heights))
        #~ features.append(numOfHoles)
        #~ features.append(bumbiness)
        #~ features.append(complete_rows)
        #~ features.append(tSpin)
        #~ features.append(numOfTholes**2)
        #~ features.append(coastline)
        #~ features.append(semiCompleteRows**2*(semiCompleteRows>1))
        #~ return features
    
    def getQValue(self, legalFields, moves, piece,Round):
    # evalute a field based on moves 
        qValue = 0.0
        tempField = copy.deepcopy(legalFields[moves])
        
        # delete complete rows
        complete_rows =  tempField.numOfCompleteRows()
        
        field = np.array(tempField.field)
        field = field.ravel().T
        
        # Forward pass
        self.X1 = self.sigmoid(field.dot(self.W1))
        
        qValue = self.sigmoid(self.X1.dot(self.W2))
        
        
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
        
        #~ features = self.computeFeatures(legalFields[moves], moves, piece,Round)
        #delete complete rows
        complete_rows = legalField[moves].numOfCompleteRows()
        
        nextState = GameState(legalFields[moves], (self.initGameState.combo+1)*(legalFields[moves].points>0), self.initGameState.skips,self.initGameState.nextPiece, None, [3, -1], self.initGameState.timebank,self.initGameState.Round +1)
        legalFields2 = nextState.getLegalActions()
        bestQValue, bst_moves = self.getValue(legalFields2, nextState.currentPiece, nextState.Round)
        
        field = np.array(legalFields[moves].field).ravel().T
        
        # back propagation
        
        loss = -(reward + self.discount * bestQValue  - self.getQValue(legalFields, moves, piece, Round))
        
        dloss = self.sigmoid(loss) * (1 - self.sigmoid(loss))
        
        dloss = np.array(dloss)
        print dloss.size
        
        dW2 = -self.X1 * (dloss)
        
        dX1 = -dloss * self.W2
        
        #~ print dX1.shape
        field = np.array([field])
        #~ print field.shape
        dX1 = self.sigmoid(dX1)*(1 - self.sigmoid(dX1))
        
        dW1 = dX1.dot(field)
        dW1 = dW1.T
        dW2 = dW2.T
        print self.W2.shape
        print dW2.shape
        
# gradient descent 
        #~ print self.W1
        self.W1 -= self.alpha*dW1
        #~ print self.W1
        
        A =  self.alpha*dW2
        A = np.array([A])
        A = A.T
        self.W2 -= A
        
                #~ print dW1.shape
        #~ for i in range(len(features)):
            # getValues should be fixed !!!!!!!!!!!!!!!!
            
            #~ self.weights[i] += self.alpha * (reward + self.discount * bestQValue  - self.getQValue(legalFields, moves, piece, Round)) * features[i]
    
    def sigmoid(self, X):
        exponencial = np.exp(-X) + 1
        return np.divide(1.0, exponencial)
