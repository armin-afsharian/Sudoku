
import copy
from sudokuGenerator import *

# -------- Global board ----------------

Board1 = [
        [0, 1, 0, 0, 4, 5, 0, 0, 0],
        [6, 9, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 3, 6, 0, 0, 0, 1],
        [5, 7, 9, 6, 3, 4, 0, 1, 0],
        [0, 0, 6, 0, 0, 2, 0, 4, 9],
        [0, 0, 0, 9, 7, 8, 0, 0, 0],
        [0 ,0, 0, 0, 9, 0, 3, 5, 4],
        [0, 2, 0, 4, 8, 0, 0, 6, 0],
        [0, 0, 7, 5, 1, 0, 0, 9, 8],
    ]

Board2 = [
        [0, 9, 3, 0, 0, 0, 0, 6, 4],
        [0, 0, 0, 4, 6, 3, 5, 0, 8],
        [0, 4, 8, 9, 2, 0, 0, 0, 0],
        [8, 6, 4, 5, 3, 7, 9, 0, 1],
        [0, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 6],
        [0, 0, 1, 0, 5, 2, 6, 0, 7],
        [0, 0, 0, 7, 9, 6, 8, 1, 0],
        [2, 7, 0, 0, 8, 0, 0, 0, 9],
    ]

TestBoard =[
                    [7, 8, 0, 4, 0, 0, 1, 2, 0],
                    [6, 0, 0, 0, 7, 5, 0, 0, 9],
                    [0, 0, 0, 6, 0, 1, 0, 7, 8],
                    [0, 0, 7, 0, 4, 0, 2, 6, 0],
                    [0, 0, 1, 0, 5, 0, 9, 3, 0],
                    [9, 0, 4, 0, 6, 0, 0, 0, 5],
                    [0, 7, 0, 3, 0, 0, 0, 1, 2],
                    [1, 2, 0, 0, 0, 7, 4, 0, 0],
                    [0, 4, 9, 2, 0, 6, 0, 0, 7]
                ]


Board = []
solvedBoard = []

def solve(board):
    # end condition:- getting to the end of the board - the function findEmpty return NONE
    find = findEmpty(board)
    if find is None:  # if find != False
        return True
    else:
        row, col = find
    for number in range(1, 10):
        if validCheck(board, number, (row, col)):
            board[row][col] = number
            # TODO: need to show it on the GUI

            if solve(board):
                return True

            board[row][col] = 0
            # TODO: delete the number in the GUI
    return False


def mainSolver(level, boardSelection):
    # sudokuGenerate(Board, level)
    Board = copy.deepcopy(Board1)
    if boardSelection == 1:
        Board = copy.deepcopy(Board2)
    else:
        Board = copy.deepcopy(TestBoard)
    solvedBoard = copy.deepcopy(Board)
    solve(solvedBoard)
    return solvedBoard, Board
   