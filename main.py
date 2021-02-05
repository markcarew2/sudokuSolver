import pandas as pd
from random import randrange
from board import Board
from backTrackSearch import backTrackSearch
from queue import PriorityQueue

df = pd.read_csv("sud1.csv")

dfProblems = df["puzzle"]
f = open("output.txt","w")
f.close()

#Grabs first 1000 puzzles from the set
#First tries to solve with AC3, when this doesn't work, solves with BTS
#The work done by AC3 carries over to BTS
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
        print("     BTS Solution: ", board.returnSolution())
        print("Provided Solution: ", puzzleSolution)
        print("********")

        with open("output.txt","a") as f:
            f.write(stringy + "\n")
