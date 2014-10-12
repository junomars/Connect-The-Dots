__author__ = 'Jonathan'
# filename: ConnectTheDots.py
# Problem Name: Question 2
# Author: Jonathan Nuno
# Date: October 9, 2014
#
# A class to simulate a GUI Button
#

class Dot():
    """ Just a structure to define a generic dot """
    def __init__(self, dot, sequence):
        self.dot = dot
        self.sequence = sequence
        self.sequence.move(7,7)

    def setFill(self, color):
        self.dot.setFill(color)
        self.dot.setOutline(color)

    def setTextColor(self, color):
        self.sequence.setTextColor(color)

    def setText(self, sequence):
        self.sequence.setText(sequence)

    def getCenter(self):
        return self.dot.getCenter()

    def move(self, dx, dy):
        self.dot.move(dx, dy)
        self.sequence.move(dx, dy)

    def draw(self, win):
        self.dot.draw(win)
        self.sequence.draw(win)

    def undraw(self):
        self.dot.undraw()
        self.sequence.undraw()

    def clone(self):
        other = Dot(self.dot.clone(), self.sequence.clone())
        return other