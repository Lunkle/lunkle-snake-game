from Tkinter import *
from time import *
from random import randint
import random
import colorsys
from math import sin
import SnakeGameData as data
from SnakeGameFunctions import *

myInterface = Tk()

setThemes(data.themesColours[data.themesList[data.currentThemeNumber%len(data.themesList)]])

s = Canvas(myInterface, width=data.canvasSize, height=data.canvasSize, background = data.outOfBoundsColour)
s.focus_set()
s.bind("<Key>",  keyPressDetector)
s.bind("<KeyRelease>", keyReleaseDetector)
s.pack()

frame = 0
while data.gameStarted == False:
    #13 * 6 = 78
    s.create_rectangle(0, 0, data.canvasSize, data.canvasSize, fill = data.outOfBoundsColour, width = 0)
    s.create_rectangle(data.squareSize + 1, data.squareSize + 1, data.canvasSize - data.squareSize + 1, data.canvasSize - data.squareSize + 1, fill = data.backgroundColour, width = 0)
    title = makeBitmap(data.canvasSize/2 - 78 - 2*sin(frame), data.canvasSize/2 - 90 - sin(frame), 6 + (sin(frame))/6, data.snakeGameTitle, s)
    textLine1 = s.create_text(data.canvasSize/2, data.canvasSize/2 + 20, text = "Choose your theme with the left and right arrows,", anchor = CENTER, font = "Courier 10")
    textLine2 = s.create_text(data.canvasSize/2, data.canvasSize/2 + 30, text = "and press enter when ready.", anchor = CENTER, font = "Courier 10")
    leftButton = makeBitmap(data.canvasSize/2 - 55 - len(data.leftArrowKey[0])*(1-data.leftArrowSize/2), data.canvasSize/2 + 80 - len(data.leftArrowKey)*data.leftArrowSize/2, data.leftArrowSize, data.leftArrowKey, s)
    rightButton =makeBitmap(data.canvasSize/2 + 60 - len(data.rightArrowKey[0])*data.rightArrowSize/2, data.canvasSize/2 + 80 - len(data.rightArrowKey)*data.rightArrowSize/2, data.rightArrowSize, data.rightArrowKey, s)
    themeDisplayString = s.create_text(data.canvasSize/2, data.canvasSize/2 + 80, text = data.themesList[data.currentThemeNumber%len(data.themesList)], font = "Courier 10")
    s.update()
    sleep(0.08)
    s.delete(themeDisplayString)
    for squares in range(len(title)):
        s.delete(title[squares])
    for squares in range(len(leftButton)):
        s.delete(leftButton[squares])
    for squares in range(len(rightButton)):
        s.delete(rightButton[squares])
    frame += 1
s.delete(textLine1, textLine2)
for i in range(data.snakeLength):
    data.snakeDirection.append("Down")
    data.snakeBodySegments.append(0)
    data.snakeX.append(0)
    data.snakeY.append(data.snakeLength-i)
    if data.themesList[data.currentThemeNumber%len(data.themesList)] == "Rainbow":
        data.snakeColours.append(getRandomColour())
    else:
        data.snakeColours.append(data.snakeColour)

makePellet(s)
while True:
    updateSnakeDirections()
    changeSnakePositions()
    checkOutOfBounds()
    checkEatItself()
    checkIfEatPellet()
    for i in range(data.snakeLength):
        data.snakeBodySegments[i] = s.create_rectangle(1+data.squareSize*(data.snakeX[i]+1), 1+data.squareSize*(data.snakeY[i]+1), 1+data.squareSize*(data.snakeX[i] + 2), 1+data.squareSize*(data.snakeY[i]+2), fill = data.snakeColours[i], width = 0)
    sleep(0.1)
    if data.eatPellet == True:
        s.delete(data.pellet)
        makePellet(s)
        grow()
    if data.outOfBounds == True or data.eatItself == True:
        break
    score = s.create_text(data.squareSize + 2, data.squareSize, text = data.snakeLength - 5, anchor = NW, font = "Courier 25")
    s.update()
    for i in range(data.snakeLength):
        s.delete(data.snakeBodySegments[i])
        s.delete(score)

s.create_rectangle(1+data.squareSize*(data.snakeX[0]+1), 1+data.squareSize*(data.snakeY[0]+1), 1+data.squareSize*(data.snakeX[0] + 2), 1+data.squareSize*(data.snakeY[0]+2), fill = "#ff4a00", width = 0)
s.create_text(data.canvasSize/2, data.canvasSize/2, text = "U LOSED", anchor = CENTER, font = "Courier 50")
mainloop()
