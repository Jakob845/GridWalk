from flask import Flask, render_template
import datetime
import random
import square

app = Flask(__name__)

steps = []
squares = []
# endPositions = [50, 60, 70, 80, 90, 91, 92, 93, 94]
# startPositions = [5, 6, 7, 8, 9, 19, 29, 39, 49]
endPositions = [10, 20, 30, 40, 50, 60, 70, 80]
startPositions = [19, 29, 39, 49, 59, 69, 79, 89]
startPos = "square" + str(random.choice(startPositions))
endPos = "square" + str(random.choice(endPositions))
# endPos = "square50"

def CreateSquares(squares):
    i = 0
    while i < 100:
        sqr = square.square("square" + str(i), False, False)
        squares.append(sqr)
        i += 1

CreateSquares(squares)

def SetObstacles(squares):
    #For testing
    # squares[40].obstacle = True
    # squares[60].obstacle = True

    i = 0
    while i < 25:
        noObsticals = [19, 20, 29, 30, 39, 40, 49, 50, 59, 60, 69, 70, 79, 80, 89, 90]
        rnd = random.randrange(11,88)
        sq = "square" + str(rnd)
        sqr = next(square for square in squares if square.id == sq)
        if sq != startPos and sq != endPos and rnd not in noObsticals and sqr.obstacle == False:
            sqr = next(square for square in squares if square.id == sq)
            sqr.obstacle = True
            i += 1

SetObstacles(squares)

def Left(currentPos):
    tempHolder = int(currentPos[-1])
    if tempHolder != 0:
        currentPos = currentPos[:-1]
        currentPos += str(tempHolder -1)
    return currentPos

def Down(currentPos):
    tempHolder = int(currentPos[-OneOrTwoDigits(currentPos):])

    if tempHolder <= 89:
        currentPos = currentPos[:-OneOrTwoDigits(currentPos)]
        currentPos += str(tempHolder +10)
    return currentPos

def Up(currentPos):
    tempHolder = int(currentPos[-OneOrTwoDigits(currentPos):])
    
    if tempHolder >= 10:
        currentPos = currentPos[:-OneOrTwoDigits(currentPos)]
        currentPos += str(tempHolder -10)
    return currentPos

def Right(currentPos):
    tempHolder = int(currentPos[-1])
    if tempHolder < 9:
        currentPos = currentPos[:-1]
        currentPos += str(tempHolder +1)
    return currentPos

def OneOrTwoDigits(square):
    if len(square) == 8:
        return 2
    else:
        return 1

def FindPath(Pos):
    #Nuvarande steg
    currentPos = Pos
    if currentPos == endPos:
        return
    #Sparar eventuella nästa steg i variabler
    leftSquare = next(square for square in squares if square.id == Left(currentPos))

    downSquare = next(square for square in squares if square.id == Down(currentPos))

    upSquare = next(square for square in squares if square.id == Up(currentPos))

    rightSquare = next(square for square in squares if square.id == Right(currentPos))


    #Kollar så de inte är sista steget till mål
    if currentPos != endPos: #leftSquare != endPos and downSquare != endPos and upSquare != endPos and rightSquare != endPos:
        if int(currentPos[-OneOrTwoDigits(currentPos):]) != 0: #Om sista siffran inte är 0 (Raden längst till vänster)
            #Kollar så nästa steg inte har ett hinder eller är markerat som deadend eller redan finns i steg
            if leftSquare.obstacle == False and leftSquare.deadEnd == False and leftSquare.id not in steps and leftSquare.id != currentPos:
                currentPos = leftSquare.id
            elif downSquare.obstacle == False and downSquare.deadEnd == False and downSquare.id not in steps and downSquare.id != currentPos:
                currentPos = downSquare.id
            elif upSquare.obstacle == False and upSquare.deadEnd == False and upSquare.id not in steps and upSquare.id != currentPos:
                currentPos = upSquare.id
            elif rightSquare.obstacle == False and rightSquare.deadEnd == False and rightSquare.id not in steps and rightSquare.id != currentPos:
                currentPos = rightSquare.id
            else:
                #Markerar nuvarande och alla nästa steg som deadEnds eftersom det inte gick att komma vidare
                next(square for square in squares if square.id == currentPos).deadEnd = True
                leftSquare.deadEnd = True
                downSquare.deadEnd = True
                upSquare.deadEnd = True
                rightSquare.deadEnd = True
                
                steps.pop()
                currentPos = steps[-1]

        elif int(currentPos[-OneOrTwoDigits(currentPos):]) < int(endPos[-OneOrTwoDigits(endPos):]):
            currentPos = Down(currentPos)
        elif int(currentPos[-OneOrTwoDigits(currentPos):]) > int(endPos[-OneOrTwoDigits(endPos):]):
            currentPos = Up(currentPos)
        else:
            return
            
        if currentPos not in steps:
            steps.append(currentPos)

        FindPath(currentPos)

    else:
        return

FindPath(startPos)

#Render all squares
@app.route("/")
def home():
    content = '<div style="margin:auto; margin-Top:50px; width:715px;">'

    i = 0
    while i < 100:
        if squares[i].obstacle == True:
            content += '<div class="square" id="square%i" style="height:50px; width:50px; position:relative; display:inline-block; margin:10px 10px 10px 10px; background-color:black;"></div>' % i
        elif("square" + str(i)) == startPos:
            content += '<div class="square" id="square%i" style="height:50px; width:50px; display:inline-block; margin:10px 10px 10px 10px; background-color:orange;"></div>' % i
        elif("square" + str(i)) == endPos:
            content += '<div class="square" id="square%i" style="height:50px; width:50px; display:inline-block; margin:10px 10px 10px 10px; background-color:lightgreen;"></div>' % i
        else:
            content += '<div class="square" id="square%i" style="height:50px; width:50px; display:inline-block; margin:10px 10px 10px 10px; "></div>' % i
        i += 1

    content += '</div>'
    date = datetime.datetime.now()
    year = date.strftime("%G")

    stepsStr = ""
    i = 0
    while i < len(steps):
        stepsStr += steps[i] + ","
        i += 1
    
    return render_template("home.html", content=content, year=year, steps=stepsStr, startPos=startPos, endPos=endPos)

# New functions
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")


    