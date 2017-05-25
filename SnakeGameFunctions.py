from random import randint
import random
import colorsys
from math import sin
import SnakeGameData as data


def getRandomColour():
    #random.random() is a random number between 0.0 and 1.0
    h = random.random()             #between 0.0 and 1.0
    s = 0.9 + random.random()/10    #between 0.9 and 1.0
    l = 0.4 + random.random()/5.0   #between 0.4 and 0.6
    r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
    return "#%02x%02x%02x" % (r, g, b)

def setThemes(theTheme):
    data.outOfBoundsColour = theTheme[0]
    data.backgroundColour = theTheme[1]
    data.snakeColour = theTheme[2]
    data.pelletColour = theTheme[3]

def keyPressDetector(event):
    k = event.keysym
    if data.gameStarted == False:
        if k == "Return":
            data.gameStarted = True
        elif k == "Left" and data.changedTheme == True:
            data.currentThemeNumber -= 1
            data.leftArrowSize = 0.5
            data.changedTheme = False
        elif k == "Right" and data.changedTheme == True:
            data.currentThemeNumber += 1
            data.rightArrowSize = 0.5
            data.changedTheme = False
        setThemes(data.themesColours[data.themesList[data.currentThemeNumber%len(data.themesList)]])
    else:
        if k == "Return":
            if data.wantToPause == True:
                data.wantToPause = False
            elif data.wantToPause == False:
                data.wantToPause = True
        if data.updatedValue == True:
            if k == "Up" and data.newDirection != "Down":
                data.newDirection = "Up"
            elif k == "Down" and data.newDirection != "Up":
                data.newDirection = "Down"
            elif k == "Left" and data.newDirection != "Right":
                data.newDirection = "Left"
            elif k == "Right" and data.newDirection != "Left":
                data.newDirection = "Right"
            data.updatedValue = False

def keyReleaseDetector(event):
    k = event.keysym
    if data.gameStarted == False:
        if k == "Left":
            data.leftArrowSize = 1
            data.changedTheme = True
        elif k == "Right":
            data.rightArrowSize = 1
            data.changedTheme = True

def makeBitmap(x, y, squareSize, bitmap, screen):
    squaresPixelsArray = []
    for i in range(len(bitmap)):
        for j in range(len(bitmap[i])):
            colourCode = bitmap[i][j]
            if colourCode != 0:
                if colourCode == 1:
                    colour = "#62d6e0"
                elif colourCode == 2:
                    colour = "#000000"
                elif colourCode == 3:
                    colour = "#ffffff"
                squaresPixelsArray.append(screen.create_rectangle(x + squareSize * j, y + squareSize * i, x + squareSize * (j + 1), y + squareSize * (i + 1), fill = colour, width = 0))
    return squaresPixelsArray
    
def changeSnakePositions():
    for i in range(data.snakeLength):
        if data.snakeDirection[i] == "Up":
            data.snakeY[i] -= 1
        elif data.snakeDirection[i] == "Down":
            data.snakeY[i] += 1
        elif data.snakeDirection[i] == "Left":
            data.snakeX[i] -= 1
        elif data.snakeDirection[i] == "Right":
            data.snakeX[i] +=1


def updateSnakeDirections():
    for i in range(data.snakeLength-1, 0, -1):
        data.snakeDirection[i] = data.snakeDirection[i-1]
    data.snakeDirection[0] = data.newDirection
    data.updatedValue = True


def checkOutOfBounds():
    if data.snakeX[0] < 0 or data.snakeX[0] > data.gridSize or data.snakeY[0] < 0 or data.snakeY[0] > data.gridSize:
        data.outOfBounds = True


def checkEatItself():
    for i in range(1, data.snakeLength):
        if data.snakeX[0] == data.snakeX[i] and data.snakeY[0] == data.snakeY[i]:
            data.eatItself = True


def makePellet(screen):
    onSnake = True
    while onSnake == True:
        data.pelletX = randint(0, data.gridSize)
        data.pelletY = randint(0, data.gridSize)
        for i in range(1, data.snakeLength):
            if data.pelletX == data.snakeX[i] and data.pelletY == data.snakeY[i]:
                onSnake = True
                break
            else:
                onSnake = False
    data.pellet = screen.create_rectangle(1+data.squareSize*(data.pelletX+1), 1+data.squareSize*(data.pelletY+1), 1+data.squareSize*(data.pelletX + 2), 1+data.squareSize*(data.pelletY+2), fill = data.pelletColour, width = 0)

def checkIfEatPellet():
    if data.snakeX[0] == data.pelletX and data.snakeY[0] == data.pelletY:
        data.eatPellet = True


def grow():
    if data.snakeDirection[data.snakeLength - 1] == "Up":
        data.snakeX.append(data.snakeX[data.snakeLength - 1])
        data.snakeY.append(data.snakeY[data.snakeLength - 1] + 1)
    elif data.snakeDirection[data.snakeLength - 1] == "Down":
        data.snakeX.append(data.snakeX[data.snakeLength - 1])
        data.snakeY.append(data.snakeY[data.snakeLength - 1] - 1)
    elif data.snakeDirection[data.snakeLength - 1] == "Left":
        data.snakeX.append(data.snakeX[data.snakeLength - 1] + 1)
        data.snakeY.append(data.snakeY[data.snakeLength - 1])
    elif data.snakeDirection[data.snakeLength - 1] == "Right":
        data.snakeX.append(data.snakeX[data.snakeLength - 1] - 1)
        data.snakeY.append(data.snakeY[data.snakeLength - 1])
    if data.themesList[data.currentThemeNumber%len(data.themesList)] == "Rainbow":
        data.snakeColours.append(getRandomColour())
    else:
        data.snakeColours.append(data.snakeColour)
    data.snakeDirection.append(data.snakeDirection[data.snakeLength - 1])
    data.snakeBodySegments.append(0)
    data.snakeLength += 1
    data.eatPellet = False
