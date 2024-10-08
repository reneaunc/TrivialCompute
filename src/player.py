import pygame
from colors import *
from boundingBox import boundingBox
from tile import *
from board import *
from configOptions import *

class player(object):
    circle_radius = 30
    circle_inner_radius = 20
    circle_highlight_radius = 5
    circle_x, circle_y = 0, 0  #center coordinates, by screen
    circle_color = null
    circle_shadow_color = null
    circle_highlight_color = null
    currCoordinate = (0,0)
    dragging = False  # This flag checks if the circle is being dragged
    playerScore =  {"c1":"_","c2":"_","c3":"_","c4":"_"}
    playerScorePosition = (2,2)
    playerName = "Gangster"
    playerColor = white
    isTurn = True
    hasRolled = False
    clampBox = boundingBox()
    currentNeighbors = []
    #recursively grab all of our potential next moves
    def getNeighbors(self, inboard : cBoard, curPosition, diceRolls : int, possibleNeighbors):
        if curPosition[0] < 0 or curPosition[1] < 0 or curPosition[0] >= 9 or curPosition[1] >= 9:
            return possibleNeighbors
        if diceRolls == 0:
            return possibleNeighbors
        if inboard.board[curPosition[0]][curPosition[1]].mDistinct == tileDistinction.NULL:
            return possibleNeighbors
        
        if (inboard.board[curPosition[0]][curPosition[1]].mDistinct == tileDistinction.NORMAL or 
            inboard.board[curPosition[0]][curPosition[1]].mDistinct == tileDistinction.HQ or 
            inboard.board[curPosition[0]][curPosition[1]].mDistinct == tileDistinction.ROLL or
            inboard.board[curPosition[0]][curPosition[1]].mDistinct == tileDistinction.CENTER) and curPosition not in(possibleNeighbors):
            possibleNeighbors.append(curPosition)

        self.getNeighbors(inboard, (curPosition[0] - 1, curPosition[1]), diceRolls - 1, possibleNeighbors)
        self.getNeighbors(inboard, (curPosition[0] + 1, curPosition[1]), diceRolls - 1, possibleNeighbors)
        self.getNeighbors(inboard, (curPosition[0], curPosition[1] - 1), diceRolls - 1, possibleNeighbors)
        self.getNeighbors(inboard, (curPosition[0], curPosition[1] + 1), diceRolls - 1, possibleNeighbors)

    def pruneNeighbors(self, diceRoll):
        #print(self.currentNeighbors)
        toRemove = []
        toRemove.append(self.currCoordinate)
        for entry in self.currentNeighbors:
            diff = abs((entry[0] - self.currCoordinate[0])) + abs((entry[1] - self.currCoordinate[1]))
            if(diff != diceRoll) and diff != 0:
                toRemove.append(entry)
        #python does not support in place deletions, so we have to loop AGAIN
        for entry in toRemove:
            self.currentNeighbors.remove(entry)

    def checkIfHeld(self, inEvent : pygame.event):
        if inEvent.type == pygame.QUIT:
            return False
        elif inEvent.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is clicked on the circle
            if (self.circle_x - inEvent.pos[0]) ** 2 + (self.circle_y - inEvent.pos[1]) ** 2 <= self.circle_radius ** 2:
                self.dragging = True
        elif inEvent.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif inEvent.type == pygame.MOUSEMOTION:
            # Move the circle with the mouse
            if self.dragging:
                self.circle_x, self.circle_y = inEvent.pos
    
    def checkValidMove(self, inTile : tile):
        if inTile.is_inside_bounding_box((self.circle_x, self.circle_y)):
            return True
        else:
            return

    def clampPlayer(self, screenWidth, screenHeight):
        #perform a check on the players so that it cant go off screen maybe move this to player function
        #right edge
        if self.circle_x > screenWidth - self.circle_radius:
            self.circle_x = screenWidth - self.circle_radius
        #left edge
        if self.circle_x < 0:
            self.circle_x = 0
        #lower edge
        if self.circle_y < 0:
            self.circle_y = 0
        #upper edge
        if self.circle_y > screenHeight - self.circle_radius:
            self.circle_y = screenHeight - self.circle_radius

        #clamp to our bounding box
        leftPlayerEdge = self.circle_x - self.circle_radius
        rightPlayerEdge = self.circle_x + self.circle_radius
        topPlayerEdge = self.circle_y - self.circle_radius
        bottomPlayerEdge = self.circle_y + self.circle_radius
        leftCheckEdge = self.clampBox.box.centerx - (self.clampBox.box.size[0] // 2)
        rightCheckEdge = self.clampBox.box.centerx + (self.clampBox.box.size[0] // 2)
        topCheckEdge = self.clampBox.box.centery - (self.clampBox.box.size[0] // 2)
        bottomCheckEdge = self.clampBox.box.centery + (self.clampBox.box.size[0] // 2)
        if leftPlayerEdge < leftCheckEdge:
            self.circle_x = leftCheckEdge + self.circle_radius
        if rightPlayerEdge > rightCheckEdge:
            self.circle_x = rightCheckEdge - self.circle_radius
        if topPlayerEdge < topCheckEdge:
            self.circle_y = topCheckEdge + self.circle_radius
        if bottomPlayerEdge > bottomCheckEdge:
            self.circle_y = bottomCheckEdge - self.circle_radius

    def updateBox(self, inX, inY, size = 120):
        #ALWAYS RESIZE BEFORE SETTING COORDINATES
        self.clampBox.box.size = (size, size)
        self.clampBox.box.center = (inX, inY)

    def updateBoxByDice(self, diceRoll, tileSize):
        oldCenter = self.clampBox.box.center
        self.clampBox.box.size = ((tileSize) + (tileSize * diceRoll)*2, (tileSize) + (tileSize * diceRoll)*2)
        self.clampBox.box.center = (oldCenter)

    #The all in one
    def updateBoardPos(self, inTile : tile, diceRoll : int):
        self.hasRolled = False
        self.currCoordinate = (inTile.row, inTile.col)
        self.setScreenCoords(inTile.box.centerx, inTile.box.centery)
        self.updateBox(inTile.box.centerx, #x position
                       inTile.box.centery, #y position
                       ((inTile.box.size[0]) + (inTile.box.size[0] * diceRoll)*2)) #size dependent on dice rolls
    
    #this is a forcible function, and shouldnt have to be called outside of game start
    def setScreenCoords(self, inX, inY):
        #set player coords
        self.circle_x = inX
        self.circle_y = inY
    
    def drawPlayer(self, screen):
        if configModule.optionalThreeDimensionalTokens == True:
            #draw the darker circle
            pygame.draw.circle(screen, self.circle_shadow_color, (self.circle_x, self.circle_y), self.circle_radius)
            #draw the mid tone circle, offset by the difference
            diff = self.circle_radius - self.circle_inner_radius 
            pygame.draw.circle(screen, self.circle_color, (self.circle_x - diff, self.circle_y - diff), self.circle_inner_radius)
            #draw the outline
            pygame.draw.circle(screen, self.circle_shadow_color, (self.circle_x, self.circle_y), self.circle_radius+diff, diff*2)
            #draw the highlight
            pygame.draw.circle(screen, self.circle_highlight_color, (self.circle_x - (self.circle_radius * .2), self.circle_y - (self.circle_radius * .4)), self.circle_highlight_radius)
        else:
            pygame.draw.circle(screen, self.circle_color, (self.circle_x, self.circle_y), self.circle_radius)
            diff = self.circle_radius - self.circle_inner_radius
            pygame.draw.circle(screen, black, (self.circle_x, self.circle_y), self.circle_radius+diff, 2)

    def updateColor(self):
        if configModule.optionalMatchOriginalColors:
            if self.circle_color == player_red:
                self.circle_color = match_red
                self.circle_shadow_color = darkRed
            elif self.circle_color == player_blue:
                self.circle_color = match_blue
                self.circle_shadow_color = darkBlue
            elif self.circle_color == player_yellow:
                self.circle_color = match_yellow
                self.circle_shadow_color = darkYellow
            if self.circle_color == player_green:
                self.circle_color = match_green
                self.circle_shadow_color = darkGreen
        else:
            if self.circle_color == match_red:
                self.circle_color = player_red
                self.circle_shadow_color = player_red_dark
            elif self.circle_color == match_blue:
                self.circle_color = player_blue
                self.circle_shadow_color = player_dark_blue
            elif self.circle_color == match_yellow:
                self.circle_color = player_yellow
                self.circle_shadow_color = player_yellow_dark
            if self.circle_color == match_green:
                self.circle_color = player_green
                self.circle_shadow_color = player_green_dark

    def updateReportCard(self, color, wrong):
        self.playerReportCard[color] = (self.playerReportCard[color][0], self.playerReportCard[color][1] + 1)
        if not wrong:
            self.playerReportCard[color] = (self.playerReportCard[color][0] + 1, self.playerReportCard[color][1])

    def printReportCard(self):
        print("Report Card for " + self.playerName)
        print("="*30)
        print(str(self.playerReportCard[match_red][0]) + " correct out of " + str(self.playerReportCard[match_red][1]) + " for red")
        print(str(self.playerReportCard[match_green][0]) + " correct out of " + str(self.playerReportCard[match_green][1]) + " for green")
        print(str(self.playerReportCard[match_blue][0]) + " correct out of " + str(self.playerReportCard[match_blue][1]) + " for blue")
        print(str(self.playerReportCard[match_yellow][0]) + " correct out of " + str(self.playerReportCard[match_yellow][1]) + " for yellow")

    def recolor(self, inColor, inShadow, inHighlight):
        self.circle_color = inColor
        self.circle_shadow_color = inShadow
        self.circle_highlight_color = inHighlight
        
    def __init__(self, inRadius = 2, inX = 100, inY = 100, inColor = player_blue):
        self.circle_radius = inRadius
        self.circle_inner_radius = inRadius - (inRadius // 10)
        self.circle_highlight_radius = inRadius // 10
        self.circle_color = inColor
        self.currentNeighbors = []
        #TODO add more of these conditionals for the other 4 colors
        if(inColor == player_blue):
            self.circle_shadow_color = player_dark_blue
            self.circle_highlight_color = player_blue_highlight
        elif(inColor == player_yellow):
            self.circle_shadow_color = player_yellow_dark
            self.circle_highlight_color = player_yellow_highlight
        elif(inColor == player_red):
            self.circle_shadow_color = player_red_dark
            self.circle_highlight_color = player_red_highlight
        elif(inColor == player_green):
            self.circle_shadow_color = player_green_dark
            self.circle_highlight_color = player_green_highlight
        self.circle_x = inX
        self.circle_y = inY
        self.playerScore =  {"c1":"_","c2":"_","c3":"_","c4":"_"}
        self.playerReportCard = {match_red:(0,0),match_green:(0,0),match_blue:(0,0),match_yellow:(0,0)}
        self.clampBox = boundingBox()
        self.tileOffset =(0,0)
        self.updateColor()
    
