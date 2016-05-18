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
        fl = open('weights.txt', 'r')
        weights_str = fl.readlines()
        counter = 0
        self.secondLayer = 1000
        self.W1 = np.zeros((200, self.secondLayer))
        self.W2 = np.zeros((self.secondLayer, 1))
        self.b1 = np.zeros((self.secondLayer, 1))
        for line in weights_str:
            if counter > 202:
                break
            if line in ['\n', '\r\n']:
                self.W1 = np.random.rand(200, self.secondLayer)/np.sqrt(2000/2)
                self.W2 = np.random.rand(self.secondLayer, 1)/np.sqrt(self.secondLayer/2)
                self.b1 = np.random.rand(self.secondLayer, 1)/np.sqrt(self.secondLayer/2)
                break
            else:
                
                if counter < 200:
                    weights_str = line[1:-2]#remove brackets
                    weights_str = weights_str.split(',')
                    weights = [float(w) for w in  weights_str]
                    self.W1[counter] = weights
                elif counter == 201:
                    weights_str = line[2:-3]#remove brackets
                    weights_str = weights_str.split(',')
                    weights = [float(w) for w in  weights_str]
                    self.W2 = np.array([weights])
                    self.W2 = self.W2.transpose()
                else:
                    weights_str = line[2:-3]#remove brackets
                    weights_str = weights_str.split(',')
                    weights = [float(w) for w in  weights_str]
                    self.b1 = np.array([weights])
                    self.b1 = self.b1.transpose()
            counter = counter + 1

        self.alpha = 0.0001
        self.reg = 0.000
        self.discount = 0.0
        fl.close()
        
    
    def choose(self):
        self.initGameState = self._game.getInitGameState();
        #~ self.initGameState.field.printField()
        legalFields = self.initGameState.getLegalActions()
        if self.initGameState.skips > 0:
            legalFields[tuple(['skip'])] = self.initGameState.field
        
        best_val, moves = self.getValue(legalFields, self.initGameState.currentPiece, self.initGameState.Round)
        sys.stderr.write('Best_val:' + str(best_val[0][0]) +' ')
        if moves == tuple(['drop']):
            return moves
            
        reward = self.computeReward(copy.deepcopy(legalFields[moves]),moves)

        self.update(legalFields, moves, self.initGameState.currentPiece, self.initGameState.Round, reward)
        f = open('weights.txt','w')
        for line in self.W1:
            f.write(str(line.tolist()) + '\n')
        f.write(str(self.W2.transpose()[:].tolist()) +  '\n')
        f.write(str(self.b1.transpose()[:].tolist()) + '\n')
        f.close()
        
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
        sys.stderr.write('Reward:' + str(reward) + '\n')
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
        
        field = np.array(tempField.field)
        field = field.ravel().T
        field[field == 1] = 0
        field[field == 2] = 1
        field[field == 4] = 1
        field = self.changeComRows(field)
        # Forward pass
        #~ A = field.dot(self.W1)
        #~ print A.shape
        #~ print self.b1.shape
        self.X1 = self.sigmoid(field.dot(self.W1) + self.b1.T)
        #~ sys.stderr.write('Redsdfsfsdfdsf:' + str(max(max(field.dot(self.W1) + self.b1.T))) + '\n')
        #~ print self.X1.shape
        qValue = self.X1.dot(self.W2)
        
        
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
        #~ complete_rows = legalFields[moves].numOfCompleteRows()
        
        nextState = GameState(legalFields[moves], (self.initGameState.combo+1)*(legalFields[moves].points>0), self.initGameState.skips,self.initGameState.nextPiece, None, [3, -1], self.initGameState.timebank,self.initGameState.Round +1)
        legalFields2 = nextState.getLegalActions()
        bestQValue, bst_moves = self.getValue(legalFields2, nextState.currentPiece, nextState.Round)
        
        field = np.array(legalFields[moves].field).ravel().T
        field[field==1] = 0
        field[field == 2] = 1
        field[field == 4] = 1
        field = self.changeComRows(field)
        # back propagation
        
        diff = (reward + self.discount * bestQValue  - self.getQValue(legalFields, moves, piece, Round))
            
        loss = diff**2
        
        dloss = -2*diff
        
        
        
        dW2 = dloss.dot(self.X1)
        
        dX1 = dloss.dot(self.W2.T)
        
        #~ print dX1.shape
        field = np.array([field])
        #~ print field.shape
        
        dX1 = self.X1*(1 - self.X1)*dX1
        
        
        dW1 = dX1.T.dot(field)
        
        
        db1 = dX1.T +  self.reg*self.b1
            
        dW1 = dW1.T + self.reg*self.W1
        dW2 = dW2.T + self.reg*self.W2
        
# gradient descent 
        
        self.W1 -= self.alpha*dW1
        self.W2 -= self.alpha*dW2
        self.b1 -= self.alpha*db1
    
    
    def changeComRows(self, field):
        i = 0
        #~ sys.stderr.write(str(field.shape) + '\n')
        for i in range(20):
            row = field[10*i:i+10]
            a = row.tolist()
            #~ sys.stderr.write(str(row) + '\n')
            if a.count(1)==10:
                field[10*i:i+10] = -np.ones(10)
        #~ sys.stderr.write(str(field) + '\n')
        return field

        
    def sigmoid(self, X):
        try:
            exponencial = np.exp(-X) + 1
        except ValueError:
            sys.stderr.write('paixthke malakia' + '\n')
            return 0   
        return np.divide(1.0, exponencial)
