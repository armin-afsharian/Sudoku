import pygame
from sudokuSolverAlgo import *
from chooseLevel import *
import time
import sys
import copy
from csv import writer

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
L_GREEN = (150, 255, 150)
RED = (255, 0, 0)
L_RED = (255, 204, 203)
GRAY = (60, 60, 60)
L_GRAY = (220, 220, 220)
YELLOW = (255, 255, 0)


# This sets the WIDTH and HEIGHT of each grid location
CHAR_LIMIT = 50

WIDTH = HEIGHT = 50

SUBMIT_WIDTH = 2 * WIDTH
SUBMIT_HEIGHT = HEIGHT
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 750

SUBMIT_LOCATION = [200, 550, 300, 600]

# This sets the margin between each cell
MARGIN = 5
numbers_1to9 = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                pygame.K_9]

# Set the width and height of the screen [width, height]
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
# screen = pygame.display.set_mode(size)
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)

# pygame.display.set_caption("Sudoku King")

# Loop until the user clicks the close button.
done = False


def cheatingAllTheWay(sol): 
    for row in range(len(Board)):
        for column in range(len(Board[row])):
          if Board[row][column] == 0: #Update unsolved locations
            Board[row][column] = sol[row][column] #Use the solution to update board
            addNumToBoard(Board[row][column], row, column, L_GREEN)
            time.sleep(0.05)
            pygame.display.flip()
    #validateSubmission(sol)


def addNumToBoard(number, row, column, color):
    addNewRect(row, column, WHITE, 5)
    addNewRect(row, column, color, None)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(number), True, BLACK, )
    textRect = text.get_rect()  # get_rect() -> Returns a new rectangle covering the entire surface.
    textRect.center = ((MARGIN + WIDTH) * column + MARGIN + WIDTH / 2, (MARGIN + HEIGHT) * row + MARGIN + WIDTH / 2)
    screen.blit(text, textRect)
    drawTheBorder()


def getIncorrectCells(sol, board):
    incorrectCells = []
    for i in range(len(sol)):
        for j in range(len(sol[i])):
            if(int(sol[i][j]) != int(board[i][j])):
                incorrectCells.append(tuple((i + 1, j + 1)))
    return incorrectCells


def addNewRect(row, col, color, width):
    rectSize = pygame.Rect((MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                           HEIGHT)
    if width is not None:
        pygame.draw.rect(screen, color, rectSize, width)  # coloring only the border
    else:
        pygame.draw.rect(screen, color, rectSize)  # coloring the whole rectangle


def flickering(timeFlickering, color):  # flickering with color on-off
    addNewRect(row, column, color, 5)
    pygame.display.flip()
    time.sleep(timeFlickering)
    addNewRect(row, column, WHITE, 5)
    pygame.display.flip()
    time.sleep(timeFlickering)
    addNewRect(row, column, color, 5)
    pygame.display.flip()
    time.sleep(timeFlickering)
    addNewRect(row, column, WHITE, 5)
    pygame.display.flip()


def drawTheBorder():
    dif = 500 // 9
    for i in range(10):
        thick = 5
        pygame.draw.line(screen, GRAY, (0, i * dif + 2), (500, i * dif + 2), thick)
        pygame.draw.line(screen, GRAY, (i * dif + 2, 0), (i * dif + 2, 500), thick)
    for i in range(10):
        if i % 3 == 0:
            thick = 8
            pygame.draw.line(screen, BLACK, (0, i * dif), (500, i * dif), thick)
            pygame.draw.line(screen, BLACK, (i * dif, 0), (i * dif, 500), thick)


def drawSubmitButton(left, top, color, textInButton):
    rectSize = pygame.Rect(left, top, SUBMIT_WIDTH, SUBMIT_HEIGHT)
    pygame.draw.rect(screen, color, rectSize)  # left, top, width, height
    pygame.draw.rect(screen, BLACK, rectSize, 3)
    fontButton = pygame.font.Font('freesansbold.ttf', 20)
    textButton = fontButton.render(textInButton, True, BLACK, )
    textRectButton = textButton.get_rect()
    textRectButton.center = (left + (SUBMIT_WIDTH / 2), top + (SUBMIT_HEIGHT / 2))
    screen.blit(textButton, textRectButton)
    return rectSize


def drawInitBoard():
    # printBoard(solvedBoard)
    for row in range(len(Board)):
        for column in range(len(Board[row])):
            color = L_GRAY
            if Board[row][column] == 0:  # if we want to change to background of the empty cells
                color = WHITE
                # ----- drawing the rect ------
            pygame.draw.rect(screen, color,
                             [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
            # show nothing if the number is 0
            font = pygame.font.Font('freesansbold.ttf', 32)
            if Board[row][column] == 0:
                text = font.render(" ", True, BLACK, )  # render(text, anti-alias[True], color, background=None)
            else:
                text = font.render(str(Board[row][column]), True, BLACK, )

            textRect = text.get_rect()  # get_rect() -> Returns a new rectangle covering the entire surface.
            textRect.center = (
                (MARGIN + WIDTH) * column + MARGIN + WIDTH / 2, (MARGIN + HEIGHT) * row + MARGIN + WIDTH / 2)
            screen.blit(text, textRect)
            drawTheBorder()
    
    


def isComplete(board):
    for line in board:
        if not all(int(digit) != 0 for digit in line):
            return False
        
    return True


def getTextLines(msg):
    remaining_msg = msg
    msg_chunks = []
    while len(remaining_msg) > CHAR_LIMIT:
        cutoff_index = CHAR_LIMIT
        while cutoff_index < len(remaining_msg) and remaining_msg[cutoff_index] != " ":
            cutoff_index += 1

        msg_chunks.append(remaining_msg[:cutoff_index])
        remaining_msg = remaining_msg[cutoff_index:]

    msg_chunks.append(remaining_msg)
    return msg_chunks


def createAlert(msg):
    textLines = getTextLines(msg)
    rectSize = pygame.Rect(0, 605, SCREEN_WIDTH, SCREEN_HEIGHT - 605)
    pygame.draw.rect(screen, BLACK, rectSize)
    font = pygame.font.Font('freesansbold.ttf', 16)
    i = 0
    for textLine in textLines:
        txt = font.render(textLine, True, WHITE, )
        txtRect = txt.get_rect()
        txtRect.center = (250, 620 + (22 * i))
        i += 1
        screen.blit(txt, txtRect)
    

# -------- Main Program Loop -----------
if __name__ == "__main__":
    flag1 = True

    while flag1:
        name = enterName()
        if(name != ""):
            flag1 = False

    print(name)
    level = 3
    pygame.display.set_caption("Sudoku")
    screen = pygame.display.set_mode(size)

    sol = mainSolver(level)  # first at all the script solve the sudoku by itself

    print("solveBoard")
    printBoard(sol)
    feedback = int(sys.argv[1])
    # ------ draw the board ------
    pygame.init()
    screen.fill(BLACK)
    drawInitBoard()
    cursor1 = pygame.SYSTEM_CURSOR_ARROW
    cursor2 = pygame.SYSTEM_CURSOR_HAND  
    # Draw the Submit button
    submitButton = drawSubmitButton((SCREEN_WIDTH - SUBMIT_WIDTH) / 2, 9 * HEIGHT + 100, GREEN, "Submit")
    readyForInput = False
    key = None
    currentBoard = copy.deepcopy(Board)
    startTime = time.time()
    faults = 0
    submitFaults = 0
    correctionCount = 0
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in numbers_1to9:
                    key = chr(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # ------ if clicked on the submit button ------
                if submitButton.collidepoint(pos):
                    if not isComplete(currentBoard):
                        createAlert("Incomplete submission. Please fill out all empty blocks.")
                        # Alert that the table is not complete
                    else: 
                        incorrectCells = getIncorrectCells(sol, currentBoard)
                        submitFaults += len(incorrectCells)
                        if len(incorrectCells) == 0:
                            createAlert("Congrats!")
                            done = True
                            # Alert that the table is not complete
                        else: 
                            msg = "Try again - Some mistakes found: "
                            for cell in incorrectCells:
                                msg += ("row=" + str(cell[0]) + "-column=" + str(cell[1]) + " // ")
                            createAlert(msg)

                # ------ if clicked on a cell get his row and column ------
                if readyForInput is True:
                    if currentBoard[row][column] != 0:
                        currentBoard[row][column] = 0
                        correctionCount += 1
                        
                    addNewRect(row, column, WHITE, None)
                    drawTheBorder()
                    readyForInput = False

                #pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (WIDTH + MARGIN)
                if(column > 8 or row > 8):
                    continue
                # ------ checking if it is a empty (0 inside) ------
                if Board[row][column] == 0:
                    # ------ coloring the border of the clicked cell ----- #TODO YELLOW
                   
                    addNewRect(row, column, YELLOW, 5)
                    readyForInput = True
                    # ------ now only wait for input from the user -----

        pos = pygame.mouse.get_pos()

        if(submitButton.collidepoint(pos)):
            pygame.mouse.set_cursor(cursor2)
        else:
            pygame.mouse.set_cursor(cursor1)

        if readyForInput and key is not None:
            # ------ checking if the key is good at it's place ------
            if currentBoard[row][column] != 0:
                correctionCount += 1
            currentBoard[row][column] = int(key)
            color = WHITE
            if int(key) == sol[row][column]:
                if(feedback):
                    flickering(0.1, GREEN)
                    color = L_GREEN
                addNumToBoard(key, row, column, color)
            else:
                faultBoard[row][column] += 1
                faults += 1
                if(feedback):
                    flickering(0.1, RED)
                    color = L_RED
                addNumToBoard(key, row, column, color)
            # -----------------------------------------------
            drawTheBorder()
            readyForInput = False

        key = None
        pygame.display.flip()
        pygame.display.update()

finishTime = time.time()
duration = finishTime - startTime
brute_force = 0
for row in faultBoard:
    for cellFault in row:
        if(cellFault >= 2):
            brute_force += 1

list = [name, feedback, int(duration), faults, submitFaults, correctionCount, brute_force]
 
# Open our existing CSV file in append mode
# Create a file object for this file
with open('Data.csv', 'a', newline='') as f_object:
 
    # Pass this file object to csv.writer()
    # and get a writer object
    writer_object = writer(f_object)
 
    # Pass the list as an argument into
    # the writerow()
    writer_object.writerow(list)
 
    # Close the file object
    f_object.close()

pygame.time.wait(1000)
# Close the window and quit.
pygame.quit()
