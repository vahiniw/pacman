from cmu_graphics import *
from PIL import Image
import copy
import math
import time

#ghost class: keeps track of ghost's coordinates
class Ghost:
    def __init__ (self, x, y, img, paths):
       self.x = x
       self.y = y
       self.img = img
       self.paths = paths  

    def change(self,x,y):
       self.x = x
       self.y = y

    #pathfinding ghost algorithm: finds legal moves that the ghost can do 
        #at its current position and sends those moves into a recursive helper function
        #the recursive function returns the move that results in the least distance to the player
        #that move is added to the ghost's corrdinates
    def moveGhost(self, playX, playY):
       moves = [ (-1,0), (0,-1), (1,0), (0,1)]
       L = self.viableMoves(moves, playX, playY)
       move = self.helper( L, playX, playY, bestOption = None, bestDistance = 0)
       if move != None:
            self.x += move[0] * 4
            self.y += move[1] * 4
       else:
            if abs(playX - self.x) < abs(playY - self.y):
                if self.x < playX:
                    self.x += 1
                else:
                    self.x -=1
            else:
                if self.y < playY:
                    self.y += 1
                else:
                    self.y -=1
       print(self.x,self.y)
  
    def viableMoves(self,moves, playX, playY):
       newL = []
       for (x,y) in moves:
           if self.isLegal(self.x+x,self.y+y, playX, playY):
               newL.append((x,y))
       return newL

    def helper(self,L, playX, playY, bestOption, bestDistance):
       if L == []:
           return bestOption
       else:
           move = L[0]
           x = self.x + move[0]
           y = self.y + move[1]
           if (bestOption == None or self.distance(playX,playY, x,y) <=  bestDistance):
               bestOption = move
               bestDistance = self.distance(playX,playY,x,y)
           return self.helper(L[1:], playX, playY, bestOption, bestDistance)
  

    def isLegal(self,x,y, playX, playY):
       for path in self.paths:
           if path.isInPath(x, y):
               return True
       return False

    def distance (self, playX, playY, x, y):
       return ((x - playX)**2 + (y - playY)**2)**(1/2)

#path function: contains all of the viable paths that the ghost and pacman can move on
class Path: 
    def __init__(self,x0,y0,x1,y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
    #if ghost or pacman are in any path or very close, they are allowed to move
    def isInPath(self, pacX, pacY):
        if (abs(self.x0- pacX) <= 4 and self.y0 <= pacY <= self.y1) or (abs(self.y0 - pacY) <= 4 and self.x0 <= pacX <= self.x1) or (abs(self.x1- pacX) <= 4 and self.y0 <= pacY <= self.y1) or (abs(self.y1- pacY) <= 4 and self.x0 <= pacX <= self.x1) or (abs(self.x0- pacX) <= 4 and self.y1 <= pacY <= self.y0) or (abs(self.y0 - pacY) <= 4 and self.x1 <= pacX <= self.x0) or (abs(self.x1- pacX) <= 4 and self.y1 <= pacY <= self.y0) or (abs(self.y1- pacY) <= 4 and self.x1 <= pacX <= self.x0):
            return True
        return False 
     
def onAppStart(app):
    app.stepCounter = 0
    imageFilename = 'pacmanImg.png'
    #"https://pngimg.com/uploads/pacman/pacman_PNG62.png"
    imPIL = Image.open(imageFilename)
    app.imgPacman = CMUImage(imPIL)
    app.imgPacmanFlipped = CMUImage(imPIL.transpose(Image.FLIP_TOP_BOTTOM))
    imageFilename = 'livesLeftImg.png'
    #"https://steamcommunity.com/sharedfiles/filedetails/?id=1646388632"
    imPIL = Image.open(imageFilename)
    app.imgLivesLeft = CMUImage(imPIL)
    imageFilename = 'livesLostImg.png'
    #"https://www.istockphoto.com/vector/pixel-shaped-heart-neon-sign-bright-glowing-symbol-on-a-black-background-gm1035678952-277259219"
    imPIL = Image.open(imageFilename)
    app.imgLivesLost = CMUImage(imPIL)
    app.direction = 0
    app.width = 900
    app.height = 800
    app.isRunning = True 
    app.flip = False
    app.playerX = 450
    app.playerY = 565
    app.stepsPerSecond = 8
    app.speed = 4
    app.xCoord = []
    app.yCoord = []
    app.circleCoord = []
    app.powerCoord = []
    app.rotate = 0
    app.diagCoordX= []
    app.diagCoordY = []
    app.points = 0
    app.power = False
    app.win = False
    app.liveScreen = False
    app.lives = [True, True, True]
    app.livesLeft = 3
    app.livesLost = 0
    app.paths=[]
    p1 = Path(75, 57, 75, 220)
    p2 = Path(75,57,405,57)
    p3 = Path(495,57,830,57)
    p4 = Path(75,220,225,220)
    p5 = Path(75,150,830,150)
    p6 = Path(225,57,225,633)
    p7 = Path(495,57,495,150)
    p8 = Path(405,57,405,150)
    p9 = Path(675,57,675,633)
    p10 = Path(825, 57, 825, 220)
    p11 = Path(825,220,675,220)
    p12 = Path(315,150,315,220)
    p13 = Path(585,150,585,220)
    p14 = Path(315,220,405,220)
    p15 = Path(405,220,405,290)
    p16 = Path(495,220,495,290)
    p17 = Path(495,220,585,220)
    p18 = Path(325,290,575,290)
    p19 = Path(325,290,325,495)
    p20 = Path(575,290,575,495)
    p21 = Path(325,420,575,420)
    p22 = Path(75,495,405,495)
    p23 = Path(495,495,830,495)
    p24 = Path(225,565,675,565)
    p25 = Path(75, 495, 75, 565)
    p26 = Path(405, 495, 405, 565)
    p27 = Path(825, 495, 825, 565)
    p28 = Path(495, 495, 495, 565)
    p29 = Path(495, 495, 495, 565)
    p30 = Path(75, 703, 825, 703)
    p31 = Path(75,633, 225,633)
    p32 = Path(75, 633, 75, 703)
    p33 = Path(825, 633, 825, 703)
    p34 = Path(825,633, 675,633)
    p35 = Path(75, 565, 135, 565)
    p36 = Path(825, 563, 762, 565)
    p37 = Path(135, 565, 135, 630)
    p38 = Path(765, 565, 765, 630)
    p39 = Path(315,565,315,630)
    p40 = Path(585,565,585,630)
    p41 = Path(315, 630, 405, 630)
    p42 = Path(495, 630, 585, 630)
    p43 = Path(405, 630, 405, 703)
    p44 = Path(495, 630, 495, 703)
    app.paths.append(p1)
    app.paths.append(p2)
    app.paths.append(p3)
    app.paths.append(p4)
    app.paths.append(p5)
    app.paths.append(p6)
    app.paths.append(p7)
    app.paths.append(p8)
    app.paths.append(p9)
    app.paths.append(p10)
    app.paths.append(p11)
    app.paths.append(p12)
    app.paths.append(p13)
    app.paths.append(p14)
    app.paths.append(p15)
    app.paths.append(p16)
    app.paths.append(p17)
    app.paths.append(p18)
    app.paths.append(p19)
    app.paths.append(p20)
    app.paths.append(p21)
    app.paths.append(p22)
    app.paths.append(p23)
    app.paths.append(p24)
    app.paths.append(p25)
    app.paths.append(p26)
    app.paths.append(p27)
    app.paths.append(p28)
    app.paths.append(p29)
    app.paths.append(p30)
    app.paths.append(p31)
    app.paths.append(p32)
    app.paths.append(p33)
    app.paths.append(p34)
    app.paths.append(p35)
    app.paths.append(p36)
    app.paths.append(p37)
    app.paths.append(p38)
    app.paths.append(p39)
    app.paths.append(p40)
    app.paths.append(p41)
    app.paths.append(p42)
    app.paths.append(p43)
    app.paths.append(p44)
    #board citation: https://github.com/plemaster01/PythonPacman/blob/main/board.py
    app.board = [
[6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
[3, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 2, 3, 0, 0, 3, 1, 3, 0, 0, 0, 3, 1, 3, 3, 1, 3, 0, 0, 0, 3, 1, 3, 0, 0, 3, 2, 3, 3],
[3, 3, 1, 7, 4, 4, 8, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 7, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 7, 4, 4, 4, 4, 5, 1, 3, 7, 4, 4, 5, 0, 3, 3, 0, 6, 4, 4, 8, 3, 1, 6, 4, 4, 4, 4, 8, 3],
[3, 0, 0, 0, 0, 0, 3, 1, 3, 6, 4, 4, 8, 0, 7, 8, 0, 7, 4, 4, 5, 3, 1, 3, 0, 0, 0, 0, 0, 3],
[3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
[8, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 4, 4, 9, 9, 4, 4, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 7],
[4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4],
[5, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 7, 4, 4, 4, 4, 4, 4, 8, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 6],
[3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
[3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 4, 4, 4, 4, 4, 4, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
[3, 6, 4, 4, 4, 4, 8, 1, 7, 8, 0, 7, 4, 4, 5, 6, 4, 4, 8, 0, 7, 8, 1, 7, 4, 4, 4, 4, 5, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 5, 3, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 3, 6, 4, 8, 1, 3, 3],
[3, 3, 2, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 2, 3, 3],
[3, 7, 4, 5, 1, 3, 3, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 3, 3, 1, 6, 4, 8, 3],
[3, 6, 4, 8, 1, 7, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 8, 1, 7, 4, 5, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 4, 4, 8, 7, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 8, 7, 4, 4, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 3],
[7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8]
         ]
    app.rotate = 0
    getCoords(app)
    app.imgGhost = "https://www.giantbomb.com/a/uploads/scale_small/8/87790/2469740-blinky.png"
    app.ghost = Ghost(400, 290, app.imgGhost, app.paths)

#uses numbers on board to get exact coordinates of pellets,power ups, and walls
def getCoords(app):
    wid = app.width//30
    heig = (app.height-50)//32
    for i in range(len(app.board)):
        for j in range(len(app.board[0])):
            currLevel = app.board[i][j]
            if currLevel == 1:
                t = ((j * wid + (0.5 * wid)), (i * heig + (0.5 * heig))) 
                app.circleCoord.append(t)
            if currLevel == 2:
                t = ((j * wid + (0.5 * wid)), (i * heig + (0.5 * heig))) 
                app.powerCoord.append(t)
            if currLevel == 3:
                app.xCoord.append((j * wid + (0.5 * wid)))
                app.xCoord.append((j * wid + (0.5 * wid)))
                app.yCoord.append((i * heig))
                app.yCoord.append((i * heig + heig))
            
            if currLevel == 4:
                app.xCoord.append((j * wid))
                app.xCoord.append((j * wid + wid))
                app.yCoord.append((i * heig + (0.5 * heig)))
                app.yCoord.append((i * heig + (0.5 * heig)))

def redrawAll(app):
    if app.liveScreen:
        drawRect(450, 475, 900, 950, fill = "black", align = "center")
        drawLabel("Life Lost!", 450, 415, size = 50, fill = "white", align = "center")
        drawLabel("Press c to Continue!",450, 475, size = 30, fill = "white", align = "center")
    elif app.isRunning: 
        drawRect(450, 475, 900, 950, fill = "black", align = "center")
        #draws paths
        for path in app.paths: 
            drawLine(path.x0, path.y0, path.x1, path.y1, fill = "red")
        #drawLine(75, 57, 75, 220, fill = "red")
        #drawLine(75,57,405,57, fill = "red")
        #drawLine(495,57,830,57, fill = "red")
        #drawLine(75,220,225,220, fill = "red")
        #drawLine(75,150,830,150, fill = "red")
        #drawLine(225,57,225,633, fill = "red")
        #drawLine(495,57,495,150,fill="red")
        #drawLine(405,57,405,150,fill="red")
        #drawLine(675,57,675,633,fill="red")
        #drawLine(825, 57, 825, 220, fill = "red")
        #drawLine(825,220,675,220, fill = "red")
        #drawLine(315,150,315,220, fill = "red")
        #drawLine(585,150,585,220, fill = "red")
        #drawLine(315,220,405,220, fill = "red")
        #drawLine(405,220,405,290, fill = "red")
        #drawLine(495,220,495,290, fill = "red")
        #drawLine(495,220,585,220, fill = "red")
        #drawLine(325,290,575,290, fill = "red")
        #drawLine(325,290,325,495, fill = "red")
        #drawLine(575,290,575,495, fill = "red")
        #drawLine(325,420,575,420, fill = "red")
        #drawLine(75,495,405,495, fill = "red")
        #drawLine(495,495,830,495, fill = "red")
        #drawLine(225,565,675,565, fill = "red")
        #drawLine(75, 495, 75, 565, fill = "red")
        #drawLine(405, 495, 405, 565, fill = "red")
        #drawLine(825, 495, 825, 565, fill = "red")
        #drawLine(495, 495, 495, 565, fill = "red")
        #drawLine(495, 495, 495, 565, fill = "red")
        #drawLine(75, 703, 825, 703, fill = "red")
        #drawLine(75,633, 225,633, fill = "red")
        #drawLine(75, 633, 75, 703, fill = "red")
        #drawLine(825, 633, 825, 703, fill = "red")
        #drawLine(825,633, 675,633, fill = "red")
        #drawLine(75, 565, 135, 565, fill = "red")
        #drawLine(825, 563, 762, 565, fill = "red")
        #drawLine(135, 565, 135, 630, fill = "red")
        #drawLine(765, 565, 765, 630, fill = "red")
        #drawLine(315,565,315,630, fill = "red")
        #drawLine(585,565,585,630, fill = "red")
        #drawLine(315, 630, 405, 630, fill = "red")
        #drawLine(495, 630, 585, 630, fill = "red")
        #drawLine(405, 630, 405, 703, fill = "red")
        #drawLine(495, 630, 495, 703, fill = "red")
        wid = app.width//30
        heig = (app.height-50)//32
        #draws pellets, powerups, lines
        for (x,y) in app.circleCoord:
            drawCircle(x, y, 4, fill = "white")
        for (x,y) in app.powerCoord: 
            drawCircle(x, y, 10, fill = "white")
        for i in range(0, len(app.xCoord), 2):
            drawLine(app.xCoord[i], app.yCoord[i], app.xCoord[i+1], app.yCoord[i+1], fill = "blue", lineWidth = 3)
        for i in range(0, len(app.diagCoordX), 2):
            drawLine(app.diagCoordX[i], app.diagCoordY[i], app.diagCoordX[i+1], app.diagCoordY[i+1], fill = "blue", lineWidth = 3)
        imageWidth, imageHeight = getImageSize(app.imgPacman)
        if app.flip == True: 
            drawImage(app.imgPacmanFlipped, 
                app.playerX, app.playerY, align = 'center', rotateAngle = 180, width = imageWidth//30, height = imageHeight //30)
        else:
            drawImage(app.imgPacman, 
                app.playerX, app.playerY, align = 'center', rotateAngle = app.rotate, width = imageWidth//30, height = imageHeight //30)
        drawLabel("Press q to Quit!", 450, 770, fill = "white", size = 15)
        scoreString = "Score: " + str(app.points)
        drawLabel(scoreString, 450,15, fill = "white", size = 15)
        imageWidth, imageHeight = getImageSize(app.imgLivesLeft)
        for i in range(len(app.lives)):
            x = 830 + i *30
            if app.lives[i]:
                drawImage(app.imgLivesLeft, x, 20, align = "center", width = imageWidth//10, height = imageHeight//10)
            else:
                drawImage(app.imgLivesLost, x, 20, align = "center", width = imageWidth//18, height = imageHeight//20)
        drawImage(app.ghost.img, app.ghost.x, app.ghost.y, align = "center", width = imageWidth//24, height = imageHeight//28)
    
    elif app.isRunning == False:     
        drawRect(450, 475, 900, 950, fill = "black", align = "center")
        drawLabel("GAME OVER!", 450, 415, size = 50, fill = "white", align = "center")
        drawLabel("Press r to Play Again!",450, 475, size = 30, fill = "white", align = "center")
    
    elif app.win == True: 
        drawRect(450, 475, 900, 950, fill = "black", align = "center")
        scoreString = "Score: " + str(app.points)
        drawLabel("YOU WON!", 450, 355, size = 50, fill = "white", align = "center")
        drawLabel(scoreString, 450, 415, size = 50, fill = "white", align = "center")
        drawLabel("Press r to Play Again!",450, 475, size = 30, fill = "white", align = "center")
  
def restartApp(app):    
    app.stepCounter = 0
    app.direction = 0
    app.width = 900
    app.height = 800
    app.isRunning = True 
    app.flip = False
    app.playerX = 450
    app.playerY = 565
    app.stepsPerSecond = 8
    app.speed = 4
    app.xCoord = []
    app.yCoord = []
    app.circleCoord = []
    app.powerCoord = []
    app.rotate = 0
    app.diagCoordX= []
    app.diagCoordY = []
    app.points = 0
    app.power = False
    app.win = False
    app.liveScreen = False
    app.lives = [True, True, True]
    app.livesLeft = 3
    app.livesLost = 0
    app.rotate = 0
    getCoords(app)
    app.imgGhost = "https://www.giantbomb.com/a/uploads/scale_small/8/87790/2469740-blinky.png"
    app.ghost = Ghost(400, 290, app.imgGhost, app.paths)

def onKeyPress(app, key):
    if key == "q":
        app.isRunning = False
    elif key == "r":
        app.isRunning = True
        app.win = False
        restartApp(app)
    elif key == "c":
        app.liveScreen = False
    #each key movement checks if the player has collided with pellets, powerups, and is moving legally
    #determines if any lives are lost
    elif key == "right":
        app.playerX += app.speed
        if not(isLegalMove(app,0)):
           app.playerX -= app.speed
        else:
            app.flip = False
            app.rotate = 0
            hitPellets(app)
            hitPower(app)
        if isCollision(app) and app.power:
            app.win = True
        elif isCollision(app) and app.power == False and app.livesLeft > 0:
            app.livesLeft -=1
            app.livesLost += 1
            if app.livesLeft == 0:
                app.isRunning = False
            else:
                app.liveScreen = True
            app.lives[app.livesLeft] = False
            app.playerX, app.playerY = 450, 565
            app.ghost.change(400,290)
        elif isCollision(app) and app.power == False and app.livesLeft == 0:
            app.isRunning = False
    elif key == "left":
        app.playerX -= app.speed
        if not(isLegalMove(app,1)):
            app.playerX += app.speed
        else:
            app.rotate = 0
            app.flip = True
            hitPellets(app)
            hitPower(app)
        if isCollision(app) and app.power:
                app.win = True
        elif isCollision(app) and app.power == False and app.livesLeft > 0:
            app.livesLeft-=1
            app.livesLost += 1
            app.lives[app.livesLeft] = False
            if app.livesLeft == 0:
                app.isRunning = False
            else:
                app.liveScreen = True
            app.liveScreen = True
            app.playerX, app.playerY = 450, 565
            app.ghost.change(400,290)
        elif isCollision(app) and app.power == False and app.livesLeft == 0:
            app.isRunning = False
    elif key == "up":
        app.playerY -= app.speed
        if not(isLegalMove(app,2)):
            app.playerY += app.speed
        else:
            app.flip = False
            app.rotate = 0
            app.rotate = 270
            hitPellets(app)
            hitPower(app)
        if isCollision(app) and app.power:
                app.win = True
        elif isCollision(app) and app.power == False and app.livesLeft > 0:
            app.livesLeft-=1
            app.livesLost += 1
            app.lives[app.livesLeft] = False
            if app.livesLeft == 0:
                app.isRunning = False
            else:
                app.liveScreen = True
            app.liveScreen = True
            app.playerX, app.playerY = 450, 565
            app.ghost.change(400,290)
        elif isCollision(app) and app.power == False and app.livesLeft == 0:
            app.isRunning = False
    elif key == "down":
        app.playerY += app.speed
        if not(isLegalMove(app,3)):
            app.playerY -= app.speed
        else:
            app.flip = False
            app.rotate = 0
            app.rotate = 90
            hitPellets(app)
            hitPower(app)
        if isCollision(app) and app.power:
                app.win = True
        elif isCollision(app) and app.power == False and app.livesLeft > 0:
            app.livesLeft-=1
            app.livesLost += 1
            app.lives[app.livesLeft] = False
            if app.livesLeft == 0:
                app.isRunning = False
            else:
                app.liveScreen = True
            app.liveScreen = True
            app.playerX, app.playerY = 450, 565
            app.ghost.change(400,290)
        elif isCollision(app) and app.power == False and app.livesLeft == 0:
            app.isRunning = False

def onKeyHold(app,keys):
    if "right" in keys:
        app.playerX += app.speed
        if not(isLegalMove(app,0)):
           app.playerX -= app.speed
        else:
            app.flip = False
            app.rotate = 0
            hitPellets(app)
            hitPower(app)
        if isCollision(app) and app.power:
                app.win = True
        elif isCollision(app) and app.power == False and app.livesLeft > 0:
            app.livesLeft-=1
            app.livesLost += 1
            app.lives[app.livesLeft] = False
            if app.livesLeft == 0:
                app.isRunning = False
            else:
                app.liveScreen = True
            app.playerX, app.playerY = 450, 565
            app.ghost.change(400,290)
        elif isCollision(app) and app.power == False and app.livesLeft == 0:
            app.isRunning = False
    elif "left" in keys:
        app.playerX -= app.speed
        if not(isLegalMove(app,1)):
            app.playerX += app.speed
        else:
            app.rotate = 0
            app.flip = True
            hitPellets(app)
            hitPower(app)
        if isCollision(app) and app.power:
                app.win = True
        elif isCollision(app) and app.power == False and app.livesLeft > 0:
            app.livesLeft-=1
            app.livesLost += 1
            if app.livesLeft == 0:
                app.isRunning = False
            else:
                app.liveScreen = True
            app.lives[app.livesLeft] = False
            app.playerX, app.playerY = 450, 565
            app.ghost.change(400,290)
        elif isCollision(app) and app.power == False and app.livesLeft == 0:
            app.isRunning = False
    elif "up" in keys:
        app.playerY -= app.speed
        if not(isLegalMove(app,2)):
            app.playerY += app.speed
        else:
            app.flip = False
            app.rotate = 0
            app.rotate = 270
            hitPellets(app)
            hitPower(app)
        if isCollision(app) and app.power:
                app.win = True
        elif isCollision(app) and app.power == False and app.livesLeft > 0:
            app.livesLeft-=1
            app.livesLost += 1
            app.lives[app.livesLeft] = False
            if app.livesLeft == 0:
                app.isRunning = False
            app.lives[app.livesLeft] = False
            app.playerX, app.playerY = 450, 565
            app.ghost.change(400,290)
        elif isCollision(app) and app.power == False and app.livesLeft == 0:
            app.isRunning = False
    elif "down" in keys:
        app.playerY += app.speed
        if not(isLegalMove(app,3)):
            app.playerY -= app.speed
        else:
            app.flip = False
            app.rotate = 0
            app.rotate = 90
            hitPellets(app)
            hitPower(app)
        if isCollision(app) and app.power:
                app.win = True
        elif isCollision(app) and app.power == False and app.livesLeft > 0:
            app.livesLeft-=1
            app.livesLost += 1
            app.lives[app.livesLeft] = False
            if app.livesLeft == 0:
                app.isRunning = False
            app.lives[app.livesLeft] = False
            app.playerX, app.playerY = 450, 565
            app.ghost.change(400,290)
        elif isCollision(app) and app.power == False and app.livesLeft == 0:
            app.isRunning = False

#checks if any pellets are hit based on the distance between player and pellet    
def hitPellets(app):
    for (x,y) in app.circleCoord:
        if distance(x,y,app.playerX,app.playerY) < 4:
            app.circleCoord.remove((x,y))
            app.points += 10
    if len(app.circleCoord) == 0:
        app.win = True

def hitPower(app):
    for (x,y) in app.powerCoord:
        if distance(x,y,app.playerX,app.playerY) < 10:
            app.powerCoord.remove((x,y))
            app.points += 100
            app.power = True

def distance(x0,y0,x1,y1):
    return ((x0-x1)**2 + (y0-y1)**2)**(1/2)

#checks if it is a legal move if it is on or close to a path
def isLegalMove(app, direction):
    for path in app.paths:
        if path.isInPath(app.playerX, app.playerY):
            return True
    return False

#checks if a collision has been made based on distance
def isCollision(app):
    if distance(app.playerX, app.playerY, app.ghost.x, app.ghost.y) < 15: 
        return True
    return False

#if a powerup is enabled, the ghost stops moving, and the player has 10 seconds to find and eat the ghost to win the game
def countPower(app):
    startTime = time.time()
    while (time.time() - startTime < 10): 
        continue
    app.power = False

#calls moveGhost and checks for collisions
def onStep(app):
    app.stepCounter += 1
    if app.power == True:
        countPower(app)
    else:
        app.ghost.moveGhost(app.playerX, app.playerY)
        if isCollision(app) and app.power:
                app.win = True
        elif isCollision(app) and app.power == False and app.livesLeft > 0:
            app.livesLeft-=1
            app.livesLost += 1
            app.lives[app.livesLeft] = False
            if app.livesLeft == 0:
                app.isRunning = False
            else:
                app.liveScreen = True
            app.playerX, app.playerY = 450, 565
            app.ghost.change(400,290)
        elif isCollision(app) and app.power == False and app.livesLeft == 0:
            app.isRunning = False
           
runApp()
