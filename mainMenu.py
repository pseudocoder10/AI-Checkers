from tkinter import *
import gameBoard


class MainMenu:
    def __init__(self):
        self.master = Tk()
        self.canvas = Canvas(self.master, width=400, height=400)
        self.canvas.pack()
        self.addLabels()
        self.addButtons()
        self.master.mainloop()

    def addLabels(self):
        l1 = Label(self.canvas, text="Checkers")
        l1.config(font=("Courier", 44))
        l1.pack()

        l2 = Label(self.canvas, text="Select one of the following options:\n")
        l2.config(font=("Courier", 10))
        l2.pack()

    def addButtons(self):
        button1 = Button(self.master, text="Player vs Player", command=lambda: self.test(1))
        button2 = Button(self.master, text="Player vs AI", command=lambda: self.test(2))
        button3 = Button(self.master, text="AI vs AI", command=lambda: self.test(3))

        button1.pack()
        button2.pack()
        button3.pack()

    def test(self, x):
        gameBoard.GameBoard(x)