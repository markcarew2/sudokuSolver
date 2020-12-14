import pandas as pd
from random import randrange
from board import Board, backTrackSearch
from queue import PriorityQueue

df = pd.read_csv("sud1.csv")

dfProblems = df["puzzle"]
f = open("output.txt","w")
f.close()
#pick a puzzle
id = randrange(0,1000)

for idx in range(1000):
    puzzle = dfProblems.iloc[idx]
    puzzleSolution = df.iloc[idx,1]


    board = Board(puzzle)
    board.AC3()
    if board.isSolved():
        stringy = str(idx)+ ", " + board.returnSolution() + ", " + "AC3"
        with open("output.txt","a") as f:
            f.write(stringy + "\n")
    else:
        backTrackSearch(board)
        stringy = str(idx)+ ", " + board.returnSolution() + ", " + "BTS"
        with open("output.txt","a") as f:
            f.write(stringy + "\n")