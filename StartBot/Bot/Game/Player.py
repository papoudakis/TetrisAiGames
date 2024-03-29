from Field import Field


class Player:
    def __init__(self, name=None):
        self.name = name
        self.rowPoints = 0
        self.combo = 0
        self.skips = 0
        self.field = Field(0)

    def updateRowPoints(self, rowPoints):
        self.rowPoints = rowPoints

    def updateCombo(self, combo):
        self.combo = combo
    
    def updateSkips(self, skips):
        self.skips = skips
        

