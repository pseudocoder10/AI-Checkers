from tkinter import *
from checkerPiece import CheckerPiece
import AI
import time

class GameBoard:
    def __init__(self, state):
        self.dimensions = [30*8, 30*8]
        self.player1IsHuman = True if state < 3 else False
        self.player2IsHuman = True if state < 2 else False
        self.master = Tk()
        self.canvas = Canvas(self.master, width=30*8, height=30*8)
        self.canvas.pack()
        self.makeRectangles()
        self.checkers1, self.checkers2, self.highlightedMoves = [], [], []
        self.addCheckers()
        self.selectedChecker = self.checkers1[0]
        self.turn = 1
        self.hasToJump = False
        self.help = Label(self.master, text="Turn of white")
        self.help.pack()

        if not self.player1IsHuman:
            self.makeAIMove()

        self.master.mainloop()


    def makeRectangles(self):
        for i in range(8):
            for j in range(8):
                self.canvas.create_rectangle(i * 30, j * 30, (i + 1) * 30, (j + 1) * 30, fill="red" if (i + j)%2 == 0 else "black",
                                             outline="black")

    def getCheckerObject(self, x, y):
        for i in self.checkers1:
            if i.coord == [x, y]:
                return i
        for i in self.checkers2:
            if i.coord == [x, y]:
                return i

    def addCheckers(self):
        for j in range(3):
            for i in range(8):
                if (i + j) % 2 == 1:
                    continue
                piece = CheckerPiece(1, self.canvas, [i, j])
                if self.player1IsHuman:
                    self.canvas.tag_bind(piece.circle, "<ButtonPress-1>", self.checkerPieceClicked)
                self.checkers1.append(piece)

        for j in range(5, 8):
            for i in range(8):
                if (i + j) % 2 == 1:
                    continue
                piece = CheckerPiece(2, self.canvas, [i, j])
                if self.player2IsHuman:
                    self.canvas.tag_bind(piece.circle, "<ButtonPress-1>", self.checkerPieceClicked)
                self.checkers2.append(piece)

    def makeAIMove(self):
        res = AI.solve(self.checkers1, self.checkers2, self.turn, 4)
        moves = res[1]
        currCoord = moves[0]
        for coord in moves[1:]:
            time.sleep(0.5)
            checker = self.getCheckerObject(currCoord[0], currCoord[1])
            checker.updatePos(coord)
            if abs(currCoord[0] - coord[0]) == 2:
                self.deleteChecker((currCoord[0]+coord[0])/2, (currCoord[1]+coord[1])/2)
            self.master.update()
            currCoord = coord

        self.changeTurn()

    def checkerPieceClicked(self, event):
        if self.hasToJump:
            return

        self.removeHighlights()
        x = int(self.canvas.canvasx(event.x) / 30)
        y = int(self.canvas.canvasy(event.y) / 30)
        self.selectedChecker = self.getCheckerObject(x, y)

        if self.selectedChecker.player != self.turn:
            return

        self.showMoves()

    def validMoveClicked(self, event):
        x = int(self.canvas.canvasx(event.x) / 30)
        y = int(self.canvas.canvasy(event.y) / 30)

        [xOrig, yOrig] = self.selectedChecker.coord

        self.removeHighlights()
        self.selectedChecker.updatePos([x, y])
        self.master.update()
        self.canvas.tag_bind(self.selectedChecker.circle, "<ButtonPress-1>", self.checkerPieceClicked)

        if abs(x - xOrig) == 2:
            self.deleteChecker((x+xOrig)/2, (y+yOrig)/2)
            self.master.update()
            if len(self.getJumpNeighbours()) > 0:
                self.hasToJump = True
                self.showMoves()
            else:
                self.hasToJump = False
                self.changeTurn()
        else:
            self.hasToJump = False
            self.changeTurn()

    def deleteChecker(self, x, y):
        for i in range(len(self.checkers1)):
            if self.checkers1[i].coord == [x, y]:
                self.canvas.delete(self.checkers1[i].circle)
                del self.checkers1[i]
                break

        for i in range(len(self.checkers2)):
            if self.checkers2[i].coord == [x, y]:
                self.canvas.delete(self.checkers2[i].circle)
                del self.checkers2[i]
                break

        # add check for game over

    def removeHighlights(self):
        for i in self.highlightedMoves:
            self.canvas.delete(i)

    def changeTurn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

        if self.check_if_game_over():
            self.help.config(text=f"{'White' if len(self.checkers2)==0 else 'Black'} wins!")
            self.master.update()
            return

        self.help.config(text=f"Turn of {'white' if self.turn == 1 else 'black'}")
        self.master.update()

        if self.turn == 1 and not self.player1IsHuman:
            self.makeAIMove()
        if self.turn == 2 and not self.player2IsHuman:
            self.makeAIMove()

    def check_if_game_over(self):
        if len(self.checkers1) == 0 or len(self.checkers2) == 0:
            return True
        return False

    def getNeighbours(self):
        moves = []
        if self.selectedChecker.player == 1 or self.selectedChecker._isKing():
            moves.append([-1, 1])
            moves.append([1, 1])
        if self.selectedChecker.player == 2 or self.selectedChecker._isKing():
            moves.append([1, -1])
            moves.append([-1, -1])

        [x, y] = self.selectedChecker.coord
        neighbours = []

        for i in moves:
            if self.occupiedStatus(i[0] + x, i[1] + y) == 0:
                neighbours.append([i[0] + x, i[1] + y])

        return neighbours

    def getJumpNeighbours(self):
        moves = []
        if self.selectedChecker.player == 1 or self.selectedChecker._isKing():
            moves.append([-1, 1])
            moves.append([1, 1])
        if self.selectedChecker.player == 2 or self.selectedChecker._isKing():
            moves.append([1, -1])
            moves.append([-1, -1])

        [x, y] = self.selectedChecker.coord
        neighbours = []

        for i in moves:
            if self.occupiedStatus(2*i[0] + x, 2*i[1] + y) == 0 and self.occupiedStatus(i[0] + x, i[1] + y) != self.selectedChecker.player and self.occupiedStatus(i[0] + x, i[1] + y) > 0:
                neighbours.append([2*i[0] + x, 2*i[1] + y])

        return neighbours

    def showMoves(self):
        neigbours = self.getNeighbours() if not self.hasToJump else []
        neigbours += self.getJumpNeighbours()

        for i in neigbours:
            size = 30
            circle = self.canvas.create_oval(i[0] * size + 25, i[1] * size + 25, (i[0] + 1) * size - 25, (i[1] + 1) * size - 25,
                                             fill="blue", outline="yellow", width=3)
            self.highlightedMoves.append(circle)
            self.canvas.tag_bind(circle, "<ButtonPress-1>", self.validMoveClicked)


    def occupiedStatus(self, x, y):
        if x >= 8 or x < 0 or y >= 8 or y < 0:
            return -1

        obj_ = self.getCheckerObject(x, y)

        if not obj_:
            return 0
        else:
            return obj_.player
