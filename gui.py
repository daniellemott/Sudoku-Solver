"""
 Danielle Mott
 30/12/2019


 Code referenced:

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids
 Explanation video: http://youtu.be/vRB_983kUMc
 https://www.youtube.com/watch?v=jl5yUEdekEM&t=130s
 https://pythonbasics.org/pyqt-qmessagebox/

"""

import pygame
import sudoku as s
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

# Colours
BLACK = (0, 0, 0)
GREY = (70, 70, 70)
WHITE = (255, 255, 255)
YELLOW = (255,255,153)
PURPLE = (218,112,214)
RED = (220,20,60)
GREEN = (50,205,50)


# Display initial entries in board
def makeSquares(sudokuGrid, height, width, margin, screen, colour):
    myfont = pygame.font.SysFont('Comic Sans MS', 25)
    i = -1
    j = -1
    for column in range(0 + margin, 355, width + margin):
        i += 1
        for row in range(0 + margin, 355, height + margin):
            j += 1
            pygame.draw.rect(screen, colour, [column, row, width, height])
            num = getGridEntry(sudokuGrid, j % 9, i % 9)
            textsurface = myfont.render(" " + num, False, (0, 0, 0))
            screen.blit(textsurface, (column + 2.5, row + 5))
    pygame.display.flip()


# Change numeric entry in a rectangle
def changeSquare(height, width, screen, colour, pos, entry):
    # Determine corresponding white rectangle based on position of mouse click
    col = getRectangleCoordinate(pos)[0]
    row = getRectangleCoordinate(pos)[1]

    myfont = pygame.font.SysFont('Comic Sans MS', 25)
    pygame.draw.rect(screen, colour, [col, row, width, height])
    textsurface2 = myfont.render(" " + entry, False, GREY)
    screen.blit(textsurface2, (col + 2.5, row + 5))

    pygame.display.flip()


# Return coordinates to corresponding rectangle
def getRectangleCoordinate(pos):
    col = (pos[0] // 40) * 40 + 15
    row = (pos[1] // 40) * 40 + 15
    return col, row

def getGridEntry(sudokuGrid, i, j):
    arrEntry = sudokuGrid.accessUnsolvedGridEntry(i, j)
    if arrEntry:
        return str(arrEntry)
    # If grid entry is a 0, nothing is displayed
    return ""

# Given event key, return the number that was entered
def getEntry(event):
    entry = ""
    if event.key == pygame.K_1:
        entry = "1"
    elif event.key == pygame.K_2:
        entry = "2"
    elif event.key == pygame.K_3:
        entry = "3"
    elif event.key == pygame.K_4:
        entry = "4"
    elif event.key == pygame.K_5:
        entry = "5"
    elif event.key == pygame.K_6:
        entry = "6"
    elif event.key == pygame.K_7:
        entry = "7"
    elif event.key == pygame.K_8:
        entry = "8"
    elif event.key == pygame.K_9:
        entry = "9"
    return entry

# Determine if it's a mutable entry in the sudoku grid
def notOccupied(grid, x, y):
    if grid[x][y] != 0:
        return False
    return True

# Change specified rectangle colour
def highlightRectangle(screen, colour, pos, width, height):
    col = getRectangleCoordinate(pos)[0]
    row = getRectangleCoordinate(pos)[1]
    pygame.draw.rect(screen, colour, [col, row, width, height])
    pygame.display.flip()

# Determine corresponding sudoku array indices
def getArrCoordinates(pos, height, width, margin):
    y = pos[0] // (width + margin)
    x = pos[1] // (height + margin)
    return x, y


# Pop up window to solve sudoku grid
def window():
    app = QApplication(sys.argv)
    win = QWidget()
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Question)
    msgBox.setText("Solve Sudoku?")
    msgBox.setWindowTitle("Sudoku")
    msgBox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

    returnValue = msgBox.exec()
    return returnValue

# Should be refactored into multiple different methods
def main():
    validInput = [str(i) for i in range(1, 10)]
    grid = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0],
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0]]
    gridObject = s.Sudoku(grid)
    solved = gridObject.accessSolvedGrid()

    pygame.init()
    size = (375, 375)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    width = 25
    height = 25
    margin = 15
    pygame.display.set_caption("Sudoku")
    screen.fill(PURPLE)
    makeSquares(gridObject, height, width, margin, screen, WHITE)

    # Flags
    done = False
    mousePress = False
    entryFlag = False
    pos = None
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pos:
                    x = getArrCoordinates(pos, height, width, margin)[0]
                    y = getArrCoordinates(pos, height, width, margin)[1]

                    if gridObject.accessUnsolvedGridEntry(x, y) == 0:
                        if not entryFlag:
                            entry = ""
                        changeSquare(height, width, screen, WHITE, pos, entry)
                        entryFlag = False
                pos = pygame.mouse.get_pos()
                mousePress = True
                # ugly piece of code
                if pos:
                    x = getArrCoordinates(pos, height, width, margin)[0]
                    y = getArrCoordinates(pos, height, width, margin)[1]
                    if gridObject.accessUnsolvedGridEntry(x, y) == 0:
                        highlightRectangle(screen, YELLOW, pos, width, height)
            elif mousePress and event.type == pygame.KEYDOWN:
                x = getArrCoordinates(pos, height, width, margin)[0]
                y = getArrCoordinates(pos, height, width, margin)[1]
                if gridObject.accessUnsolvedGridEntry(x, y) == 0:
                    entry = getEntry(event)
                    if entry in validInput:
                        changeSquare(height, width, screen, YELLOW, pos, entry)
                        if int(solved[x][y]) == int(entry):
                            changeSquare(height, width, screen, GREEN, pos, entry)
                        else:
                            changeSquare(height, width, screen, RED, pos, entry)
                        pygame.time.delay(250)
                        entryFlag = True
                mousePress = False
            # Solve sudoku
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # pop up window
                returnVal = window()
                # yes, solve sudoku grid
                if returnVal == 16384:
                    # solve sudoku cube
                    grid = gridObject.accessSolvedGrid()
                    newGrid = s.Sudoku(grid)
                    makeSquares(newGrid, height, width, margin, screen, WHITE)
            clock.tick(60)
    pygame.quit()

main()


