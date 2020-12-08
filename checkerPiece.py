class CheckerPiece:
    def __init__(self, player, canvas, coord):
        self.player = player
        self.isKing = False
        self.coord = coord
        self.canvas = canvas
        self.size = 30
        self.circle = self.drawPiece()
        self.isSelected = False

    def drawPiece(self):
        x, y = self.coord[0], self.coord[1]
        size = self.size
        color = "white" if self.player == 1 else "black"
        circle = self.canvas.create_oval(x * size + 25, y * size + 25, (x + 1) * size - 25, (y + 1) * size - 25,
                                         fill=color, outline="cyan" if self.isKing else "black",
                                         width=3 if self.isKing else 1)
        return circle

    def updatePos(self, newCoord):
        self.canvas.delete(self.circle)
        self.updateCoords(newCoord[0], newCoord[1])
        self.circle = self.drawPiece()

    def updateCoords(self, x, y):
        if self.player == 1 and y == 7:
            self.makeKing()
        if self.player == 2 and y == 0:
            self.makeKing()
        self.coord = [x, y]

    def getCoords(self):
        return self.coord

    def makeKing(self):
        self.isKing = True

    def _isKing(self):
        return self.isKing

    def _isSelected(self):
        return self.isSelected

    def markSelected(self):
        self.isSelected = True

    def markUnselected(self):
        self.isSelected = False