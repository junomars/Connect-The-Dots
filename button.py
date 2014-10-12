__author__ = 'Jonathan'
# filename: ConnectTheDots.py
# Problem Name: Question 2
# Author: Jonathan Nuno
# Date: October 9, 2014
#
# A class to simulate a GUI Button
#

class Button():
    """ Just a structure to define a generic button """

    def __init__(self, rect, text, toggle=False):
        self.rect = rect
        self.text = text
        self.toggle = toggle

    def isClicked(self, point):
        return self.rect.isPointInsideMe(point)

    def toggleButton(self):
        self.toggle = not self.toggle
        return self

    def isToggled(self):
        return self.toggle

    def setFill(self, color):
        self.rect.setFill(color)
        return self

    def setText(self, text):
        self.text.setText(text)
        return self

    def setSize(self, size):
        self.text.setSize(size)
        return self

    def draw(self, win):
        self.rect.draw(win)
        self.text.draw(win)
        return self

    def undraw(self):
        self.rect.undraw()
        self.text.undraw()
        return self