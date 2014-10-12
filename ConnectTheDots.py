__author__ = 'Jonathan'
# filename: ConnectTheDots.py
# Problem Name: Question 2
# Author: Jonathan Nuno
# Date: October 9, 2014
#
# Objective:
#   You need to create a program that allows you to create, edit or load connect the dot pictures.
#
# Algorithm:
#   1. Create a connect the dot picture
#       A. Points on the GUI will be entered by mouse clicks.
#       B. Label each point with the appropriate number (the sequence number)
#   2. Must support a canvas of at least 600x600 px
#   3. Create a menu to implement certain features
#       A. Tracer Button, to toggle lines
#           i. Clicking it will show the lines, if they are not shown and vise versa
#       B. Save Button, to save file
#           i. Clicking the save button will save the points in one line of a text file
#           ii. e.g. (141 50 87 30)
#           iii. Said format has each point saves as "x 'space' y 'space'"
#       C. Load Button, to load file
#           i. Clear screen on load
#           ii. Load points into list of points
#           iii. Make lines and draw if tracer option is toggled on
#       D. Exit Button, just because
#   4. Allow user to click to create points
#       A. The dots should also be numbered in sequential order on screen
#
# Additional Ideas/To Do:
#   Confirm load if unsaved changes - DONE
#   Confirm in-application exit if unsaved changes -
#   Verify program stability when a file has an incomplete point - DONE (will ignore the half point)
#   Verify program stability when a file has words/text - DONE (will print error to console and continue)
#   Create a dot class to hold a filled in circle and a corresponding number - DONE
#
# Imports:
#   graphics - naturally.
#   os.path - to verify if a file exists as to not overwrite it

from button import Button
from dot import Dot
from graphics import *
import os.path

def createButton(anchorPoint, width, height, text, fill, outline):
    """
    Helper method to streamline button creation
    :param anchorPoint: top left corner
    :param width: button width
    :param height: button height
    :param text: button text
    :param fill: button fill
    :param outline: button outline
    :return: button made
    """
    rectSizePoint = Point(anchorPoint.getX() + width, anchorPoint.getY() + height)
    rect = Rectangle(anchorPoint, rectSizePoint)
    rect.setFill(fill)
    rect.setOutline(outline)

    # Button Text
    textAnchor = Point(anchorPoint.getX() + width / 2, anchorPoint.getY() + height / 2)
    text = Text(textAnchor, text)
    text.setTextColor(outline)
    text.setStyle("bold")
    button = Button(rect, text)

    return button

def main():
    """
    Our main function
    :return: None
    """
    # Color Palette and other Variables
    back_color = color_rgb(249,205,173)
    fill_color= color_rgb(252,157,154)
    out_color = color_rgb(254,67,101)
    point_color = color_rgb(131,175,155)
    line_color = color_rgb(200,200,169)
    WIN_WIDTH = 800
    WIN_HEIGHT = 800
    dialog = 0
    userDots = []
    userLines = []
    defaultPoint = Dot(Circle(Point(0,0), 3), Text(Point(0,0), "0"))
    defaultPoint.setFill(point_color)
    defaultPoint.setTextColor(out_color)

    # GUI Objects!
    buttonText = ['T','C','S','L','E']
    buttons = []
    saveload = []
    totalButtons = len(buttonText)
    B_WIDTH = 25
    B_HEIGHT = 25
    MARGIN = 10

    # Window Creation
    win = GraphWin("Connect The Dots!", WIN_WIDTH, WIN_HEIGHT)
    win.setBackground(back_color)

    # Creating buttons, buttons consist of a text element and a rectangle element
    for index in range(totalButtons):
        # Creating button anchor point itself
        anchorPoint = Point(WIN_WIDTH - ((totalButtons - index) * MARGIN) - ((totalButtons - index) * B_WIDTH), MARGIN)

        # Add it to our button list
        buttons.append(createButton(anchorPoint, B_WIDTH, B_HEIGHT, buttonText[index], fill_color, out_color))

    for button in buttons:
        button.draw(win)

    # Creating Save/Load Box
    anchorPoint = Point(WIN_WIDTH - (WIN_WIDTH / 4) - MARGIN, MARGIN * 2 + B_HEIGHT)
    rectSizePoint = Point(WIN_WIDTH - MARGIN, anchorPoint.getY() + MARGIN * 3 + B_HEIGHT * 2)
    rect = Rectangle(anchorPoint, rectSizePoint)
    rect.setOutline(out_color)
    rect.setFill(fill_color)
    saveload.append(rect)

    entryPoint = Point(anchorPoint.getX()+MARGIN, anchorPoint.getY()+2*MARGIN)
    entryWidth = (rectSizePoint.getX() - anchorPoint.getX() - 2 * MARGIN) / 10
    entry = Entry(entryPoint, int(entryWidth))
    entry.setTextColor(out_color)
    entry.setStyle("bold")
    entry.setFace("courier")
    entry.setSize(12)
    entry.setFill(line_color)
    entry.move(entryWidth * 5, 0)
    saveload.append(entry)

    line = Line(Point(WIN_WIDTH - 92.5, 35), Point(WIN_WIDTH - 92.5, 45))
    line.setOutline(out_color)
    saveload.append(line)

    # Save/Load Button, added to our list
    anchorPoint = Point(rectSizePoint.getX() - (WIN_WIDTH / 4) + MARGIN, rectSizePoint.getY() - MARGIN - B_HEIGHT)
    buttons.append(createButton(anchorPoint, (WIN_WIDTH / 4) - MARGIN * 2, B_HEIGHT, "Save", fill_color, out_color))

    # Not a button but a dialog
    anchorPoint = Point(WIN_WIDTH - (WIN_WIDTH / 4) - MARGIN, MARGIN*6+B_HEIGHT*3)
    dialog = createButton(anchorPoint, WIN_WIDTH / 4, B_HEIGHT, "DIALOG", fill_color, out_color)

    # Logic Loop
    changesFlag = False
    confirmFlag = False

    while True:
        try:
            pointClicked = win.getMouse()
        except GraphicsError:
            # Only happens when window is closed through the exit button
            return None

        if buttons[0].isClicked(pointClicked):
            # Tracer button pressed, toggle lines between points
            buttons[0].toggleButton()

            # Show toggle on or off and update lines
            if buttons[0].isToggled():
                buttons[0].setFill(line_color)

                for line in userLines:
                    line.draw(win)
            else:
                buttons[0].setFill(fill_color)

                for line in userLines:
                    line.undraw()
        elif buttons[1].isClicked(pointClicked):
            # Clear screen pressed, remove dots / lines
            for dot in userDots:
                dot.undraw()

            for line in userLines:
                line.undraw()

            # Clear records
            userDots.clear()
            userLines.clear()

            # Remove flags
            confirmFlag = False
            changesFlag = False
        elif buttons[2].isClicked(pointClicked):
            # Open or close Save menu, close load menu if it is opened
            buttons[2].toggleButton()

            # Remove dialog is it is open
            if dialog.isToggled():
                dialog.toggleButton().undraw()

            # If the load button is toggled open, "close" it
            if buttons[3].isToggled():
                buttons[3].toggleButton()
                buttons[5].setText("Save")
                saveload[2].move(-B_WIDTH-MARGIN, 0)
            # If the save button is toggled closed, remove windows
            elif not buttons[2].isToggled():
                for element in saveload:
                    element.undraw()

                buttons[5].undraw()
            # Open the buttons
            else:
                for element in saveload:
                    element.draw(win)

                buttons[5].setText("Save")
                buttons[5].draw(win)

            # Reset confirmation flag in case there are any unsaved changes
            confirmFlag = False
        elif buttons[3].isClicked(pointClicked):
            # Open or close load menu, close save menu if it is opened
            buttons[3].toggleButton()

            # Remove dialog is it is open
            if dialog.isToggled():
                dialog.toggleButton().undraw()

            # If the save button is toggled open, "close" it
            if buttons[2].isToggled():
                buttons[2].toggleButton()
                buttons[5].setText("Load")
                saveload[2].move(+B_WIDTH+MARGIN, 0)
            # If the load button is toggled closed, remove windows
            elif not buttons[3].isToggled():
                for element in saveload:
                    element.undraw()

                buttons[5].undraw()
                saveload[2].move(-B_WIDTH-MARGIN, 0)
            # Open the buttons
            else:
                for element in saveload:
                    element.draw(win)

                buttons[5].setText("Load")
                buttons[5].draw(win)
                saveload[2].move(+B_WIDTH+MARGIN, 0)

            # Reset confirmation flag in case there are any unsaved changes
            confirmFlag = False
        elif buttons[4].isClicked(pointClicked):
            # Exit button pressed, closing program
            win.close()
            return None
        elif buttons[5].isClicked(pointClicked) and(buttons[2].isToggled() or buttons[3].isToggled()):
            # Save/Load Button hit
            fileName = saveload[1].getText()

            # If the save button is open, save the points after checking file name
            if fileName is "":
                fileName = "untitled.txt"

            # To make sure we are saving a text file
            if fileName.find(".txt") == -1 or fileName.find(".txt") != len(fileName) - 4:
                fileName += ".txt"

            # If save option is open
            if buttons[2].isToggled():
                # Open file
                outfile = open(fileName, "w")

                # Write to file
                pointsStr = ""
                for dot in userDots:
                    pointsStr += str(int(dot.getCenter().getX())) + " " + str(int(dot.getCenter().getY())) + " "
                outfile.write(pointsStr)

                # Close file
                outfile.close()

                # Save successful
                dialog.setText("File saved successfully!").setSize(12)
                if not dialog.isToggled():
                    dialog.draw(win).toggleButton()
                changesFlag = False
                confirmFlag = True

            # If save isn't open, load must be open
            else:
                # If the load button is open, load the points after checking file name
                # Checking if any unsaved changes are present
                t = None
                if changesFlag and not confirmFlag:
                    confirmFlag = True

                    dialog.setText("Unsaved changes, load anyway?").setSize(9)
                    if not dialog.isToggled():
                        dialog.draw(win).toggleButton()

                # Checking if we confirmed, made separately to ensure load clicked twice
                else:
                    # Clear changes flag
                    changesFlag = False

                    # Clear current points
                    for point in userDots:
                        point.undraw()

                    for line in userLines:
                        line.undraw()

                    userDots.clear()
                    userLines.clear()

                    # Verify file
                    if os.path.isfile(fileName):
                        # Open the file
                        infile = open(fileName, "r")

                        # Get the points within the file
                        try:
                            coord = [int(x) for x in infile.readline().split()]
                            if len(coord) % 2 == 1:
                                coord.pop()

                            if len(coord) > 1:
                                for index in range(1, len(coord), 2):
                                    tmp = defaultPoint.clone()
                                    tmp.setText(len(userDots) + 1)
                                    tmp.move(coord[index-1], coord[index])
                                    tmp.draw(win)
                                    userDots.append(tmp)

                        except ValueError:
                            errorfile = open("error_log.txt", "w")
                            errorfile.write("File contained a type that could not be converted to int.")
                            errorfile.close()
                            dialog.setText("File load unsuccessful.").setSize(9)
                            if not dialog.isToggled():
                                dialog.draw(win).toggleButton()
                            continue

                        # Recreate lines
                        if len(userDots) > 0:
                            prevPoint = None
                            for nextPoint in userDots:
                                if prevPoint is None:
                                    prevPoint = nextPoint
                                else:
                                    lntmp = Line(prevPoint.getCenter(), nextPoint.getCenter())
                                    lntmp.setFill(line_color)
                                    lntmp.setWidth(2)
                                    userLines.append(lntmp)
                                    prevPoint = nextPoint
                                    if buttons[0].isToggled():
                                        lntmp.draw(win)
                        # Close the file
                        infile.close()

                        # load successful
                        dialog.setText("File loaded successfully!").setSize(12)
                        if not dialog.isToggled():
                            dialog.draw(win).toggleButton()
                    else:
                        dialog.setText("No such file found.").setSize(12)
                        if not dialog.isToggled():
                            dialog.draw(win).toggleButton()
        else:
            # Changes were made
            changesFlag = True

            # Draw points
            tmp = defaultPoint.clone()
            tmp.setText(len(userDots) + 1)
            tmp.move(pointClicked.getX(),pointClicked.getY())
            tmp.draw(win)
            userDots.append(tmp)

            # Make the line, only drawn if tracer toggled
            if len(userDots) > 1:
                lntmp = Line(userDots[len(userDots)-2].getCenter(), userDots[len(userDots)-1].getCenter())
                lntmp.setFill(line_color)
                lntmp.setWidth(2)
                userLines.append(lntmp)

                if buttons[0].isToggled():
                    lntmp.draw(win)

main()