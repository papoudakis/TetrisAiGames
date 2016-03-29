from random import randint
from AbstractStrategy import AbstractStrategy

class NoobStrategy(AbstractStrategy):
    def __init__(self, game):
        AbstractStrategy.__init__(self, game)
        
        self._actions = ['left', 'right', 'turnleft', 'turnright', 'down', 'drop']

    def choose(self):
        self.initGameState = self._game.getInitGameState();
        ind = [randint(0, 4) for _ in range(1, 10)]
        moves = map(lambda x: self._actions[x], ind)
        moves.append('drop')
        self.initGameState.printState()
        self.initGameState.getLegalActions()
        return moves