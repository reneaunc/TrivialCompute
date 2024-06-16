import array
import math
import sys
import cairo
import pygame
from pygame.locals import *
sys.path.append('/path/to/application/app/folder')
import wrappers.rsvg as rsvg
import random
from tile import *
from colors import *
from board import cBoard
from pprint import pprint

class pygameDemo(object):
    WIDTH = 1280
    HEIGHT = 720
    LENGTH = WIDTH
    OFFSET = HEIGHT
    if HEIGHT < WIDTH:
        LENGTH = HEIGHT
        OFFSET = WIDTH


    #globals are bad, avoid them when we can
    run = True
    moving = False
    color = green

    playBoard = cBoard(WIDTH, HEIGHT)

    #except for these, you could make an argument that this is acceptable since there will only ever be One screen and 4 players
    screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)

    player_size = LENGTH // 16
    player = pygame.Rect((300, 250, player_size, player_size))

    bounding_box = pygame.Rect(300, 200, 200, 200)
    bounding_box2 = pygame.Rect(100, 200, 200, 200)

    #detect if we are in bounding box
    
    def is_inside_bounding_box(self, point_or_rect):
        """ Check if a point or another rectangle is inside the bounding box. """
        if isinstance(point_or_rect, pygame.Rect):
            return self.bounding_box.colliderect(point_or_rect)
        elif isinstance(point_or_rect, tuple):
            return self.bounding_box.collidepoint(point_or_rect)
        return False

    def initializeBoard(self):
        
        rect_x, rect_y = self.WIDTH//4, self.HEIGHT//4  # Position of the rectangle we always work in quadrants
        rect_width, rect_height = self.LENGTH - (.1 * self.OFFSET), self.LENGTH - (.1 * self.OFFSET)  # Size of the rectangle
        cols, rows = 9, 9  # Number of columns and rows in the grid
        cell_width = rect_width // cols
        cell_height = rect_height // rows
        center_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        center_rect.center = (self.WIDTH + 200,self.HEIGHT//2)
        for col in range(cols):
            for row in range(rows):
                cell_x = rect_x + col * cell_width + (self.LENGTH * .4)
                cell_y = rect_y + row * cell_height - (self.LENGTH * .15)
                self.playBoard.board[col][row].box = pygame.Rect(cell_x, cell_y, cell_width, cell_height)
                #pygame.draw.rect(screen, playBoard.board[col][row].mColor, playBoard.board[col][row].box, 1)

    def resizeAll(self, inWidth, inHeight):
        # recalculate our offset
        off = min(inWidth, inHeight) // 2
        #re-adjust position
        print("Height DIFF: ", inHeight)
        print("Wdith DIFF: ", inWidth)
        #adjust the width and height of things
        self.player.x -= inWidth
        self.player.y -= inHeight
        for i in range(9):
            for j in range(9):
                self.playBoard.board[i][j].box.x -=inWidth
                self.playBoard.board[i][j].box.y -=inHeight
    def drawBoard(self):
        for col in range(9):
            for row in range(9):
                pygame.draw.rect(self.screen, self.playBoard.board[col][row].mColor, self.playBoard.board[col][row].box, 1)
    def mainLoop(self):
        while self.run:
            
            self.screen.fill((25, 28, 38))
            #draw calls
            #pygame.draw.rect(screen, color, bounding_box)
            #pygame.draw.rect(screen, color, bounding_box2, 7)
            #do a draw of the grid
            
            #Test for resize
            #pygame.draw.rect(screen, (200,0,0), (screen.get_width()/3, screen.get_height()/3, screen.get_width()/3, screen.get_height()/3))
            #pygame.draw.rect(screen, red, playBoard.outerBoard, 1)
            oldWidth = self.screen.get_width()
            oldHeight = self.screen.get_height()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run= False

                if event.type == pygame.VIDEORESIZE:
                    # addfunctionality to resize everything
                    print("resize grid and player")
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    print("Old WIdth: ", oldWidth, " event Widht: ", event.w)
                    print("old Height: ", oldHeight, " event height: ", event.h)
                    self.resizeAll(oldWidth - event.w, oldHeight - event.h)
                # Making player move

                if event.type == MOUSEBUTTONDOWN:
                    if self.player.collidepoint(event.pos):
                        self.moving = True
                elif event.type == MOUSEBUTTONUP:
                    self.moving = False
                #player moves while mouse is held
                elif event.type == MOUSEMOTION and self.moving:
                    self.player.move_ip(event.rel)
                # Test a moving point (mouse position)
            #update the bounding box
            mouse_pos = pygame.mouse.get_pos()
            if self.is_inside_bounding_box(self.player.center):
                self.color = red
            elif self.is_inside_bounding_box(mouse_pos):
                self.color = blue
            else:
                self.color = green
            
            #perform a check on the player cube so that it cant go off screen
            #right edge
            if self.player.x > self.WIDTH - self.player_size:
                self.player.x = self.WIDTH - self.player_size
            #left edge
            if self.player.x < 0:
                self.player.x = 0
            #lower edge
            if self.player.y < 0:
                self.player.y = 0
            #upper edge
            if self.player.y > self.HEIGHT - self.player_size:
                self.player.y = self.HEIGHT - self.player_size

            self.drawBoard()
            pygame.draw.rect(self.screen, base1, self.player)
            pygame.display.update()
            

        pygame.quit()

def main(): 
    #rows = 10  # Number of rows in the board
    #cols = 10  # Number of columns in the board

    # Generate the board
    #game_board = create_board(rows, cols)

    # Print the generated board
    #print_board(game_board)
    # Example usage
    #n = 2  # Depth of recursion, generates a 3**3 x 3**3 grid
    #sierpinski_carpet = generate_sierpinski_carpet(n)
    #print_carpet(sierpinski_carpet)
    demo = pygameDemo()
    demo.initializeBoard()
    demo.mainLoop()
    
if __name__=="__main__": 
    main() 