from Bot.Strategies.RandomStrategy import RandomStrategy
from Bot.Strategies.NoobStrategy import NoobStrategy
def create(strategyType, game):
    switcher = {
        "random": RandomStrategy(game),
        "noob": NoobStrategy(game)
    }

    strategy = switcher.get(strategyType.lower())

    return Planner(strategy)

class Planner:
    def __init__(self, strategy):
        self._strategy = strategy

    def makeMove(self):
        return self._strategy.choose()
