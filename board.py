from queue import Queue, PriorityQueue
import copy

class Board():
    def __init__(self, puzzle):

        """
        Takes Sudoku string as input, Constructs a board with 
        rows indexed by letters A-I and columns indexed by 1-9

        The rows, columns and boxes are dictionaries. Keys for rows
        and columns are aforementioned indices, keys for boxes are 1-9.
        Values for all are a tuple (a,b), first element (a) is a set representing the numbers
        currently in that row, column, or box. Second element (b) is a list containing the
        coordinates of the squares that are in that row, column, or box

        This stores all data about the board as divided by rows, columns, boxs, and grid.
        Since almost all the data is in sets and dictionaries, it's really fast to look up
        the information we need. This is important because our searches will be looking
        up a lot of stuff, over and over.
        """

        global numbers
        global letters
        global coordinates

        letters = ["A", "B", "C", "D", "E","F","G","H", "I"]
        numbers = [str(a) for a in range(1,10)]

        #Set up hashtables for the whole board, the rows, the columns and boxes, for faster lookup
        coordinates = []
        rows = {letter:(set(),[]) for letter in letters}
        cols = {number:(set(),[]) for number in numbers}
        boxs = {box:(set(),[]) for box in range(1,10)}
        board = {}
        domains = {}

        for j, letter in enumerate(letters):
            j = j+1
            for number in numbers:
                coordinates.append(letter+number)
                rows[letter][1].append(letter+number)
                cols[number][1].append(letter+number)
                domains[letter+number] = {1,2,3,4,5,6,7,8,9}
                if int(number) < 4:
                    if j < 4:
                        boxs[letter+number] = 1
                        boxs[boxs[letter+number]][1].append(letter+number)
                    elif j < 7 and j >3:
                        boxs[letter+number] = 4
                        boxs[boxs[letter+number]][1].append(letter+number)
                    else:
                        boxs[letter+number] = 7
                        boxs[boxs[letter+number]][1].append(letter+number)
                elif int(number) > 3 and int(number) < 7:
                    if j < 4:
                        boxs[letter+number] = 2
                        boxs[boxs[letter+number]][1].append(letter+number)
                    elif j < 7 and j >3:
                        boxs[letter+number] = 5
                        boxs[boxs[letter+number]][1].append(letter+number)
                    else:
                        boxs[letter+number] = 8
                        boxs[boxs[letter+number]][1].append(letter+number)

                else:
                    if j < 4:
                        boxs[letter+number] = 3
                        boxs[boxs[letter+number]][1].append(letter+number)
                    elif j < 7 and j >3:
                        boxs[letter+number] = 6
                        boxs[boxs[letter+number]][1].append(letter+number)
                    else:
                        boxs[letter+number] = 9
                        boxs[boxs[letter+number]][1].append(letter+number)

        #populate the hashtables
        for idx in range(len(puzzle)):
            board[coordinates[idx]] = puzzle[idx]
            rows[coordinates[idx][0]][0].add(puzzle[idx])
            cols[coordinates[idx][1]][0].add(puzzle[idx])
            boxs[boxs[coordinates[idx]]][0].add(puzzle[idx])
            if puzzle[idx] != "0":
                domains[coordinates[idx]] = {puzzle[idx]}

        #Assign the object variables
        self.board = board
        self.rows = rows
        self.cols = cols
        self.boxs = boxs
        self.coordinates = coordinates
        self.domains = {coord:set() for coord in coordinates}

        #Constrain the Domains based on puzzles initial values
        for coord in coordinates:

            if self.board[coord] != "0":
                self.domains[coord] = {self.board[coord]}

            else:
                while(True):
                    try:
                        value = domains[coord].pop()
                        value = str(value)
                        if conflict(self,value,coord):
                            pass
                        else:
                            self.domains[coord].add(value)
                    except(KeyError):
                        break
        
        self.initdomains = copy.deepcopy(self.domains)

    #Print puzzle in vaguely grid shape
    def show(self):
        global coordinates
        row = ""
        for i, coord in enumerate(coordinates):
            if i == 0:
                row += self.board[coord] + " "

            elif coord[0] != coordinates[i-1][0]:
                print(row)
                row = self.board[coord] + ' '
                
            elif coord == "I9":
                row += self.board[coord]
                print(row)

            else:
                row += self.board[coord] + " "

    #Make the Domains Arc Consistent
    def AC3(self):
        arcs = set()
        for coord in self.coordinates:
            if self.board[coord] != "0":
                pass
            else:
                for ele in self.rows[coord[0]][1]:
                    arcs.add((coord,ele))
                for ele in self.cols[coord[1]][1]:
                    arcs.add((coord,ele))
                for ele in self.boxs[self.boxs[coord]][1]:
                    arcs.add((coord,ele))
        
        while(True):
            if len(arcs) != 0:
                arc = arcs.pop()
                if revise(self, arc):
                    if len(self.domains[arc[0]]) == 0:
                        return False
                    for ele in self.rows[arc[0][0]][1]:
                        if ele != arc[0]:
                            arcs.add((ele,arc[0]))
                    for ele in self.cols[arc[0][1]][1]:
                        if ele != arc[0]:
                            arcs.add((ele,arc[0]))
                    for ele in self.boxs[self.boxs[arc[0]]][1]:
                        if ele != arc[0]:
                            arcs.add((ele,arc[0]))
                else:
                    pass
                
            else:
                return True

    #Maintaining Arc Consistency
    #Makes Selection of Arcs Arc Consistent
    def MAC(self, arcs):

        while(True):
            if len(arcs) != 0:
                arc = arcs.pop()
                if revise(self, arc):
                    if len(self.domains[arc[0]]) == 0:
                        return False
                    for ele in self.rows[arc[0][0]][1]:
                        if ele != arc[0]:
                            arcs.add((ele,arc[0]))
                    for ele in self.cols[arc[0][1]][1]:
                        if ele != arc[0]:
                            arcs.add((ele,arc[0]))
                    for ele in self.boxs[self.boxs[arc[0]]][1]:
                        if ele != arc[0]:
                            arcs.add((ele,arc[0]))
                else:
                    pass
                
            else:
                return True

    #Check if all domains are 1, if so puzzle is solved
    def isSolved(self):
        for coord in self.coordinates:
            if len(self.domains[coord]) > 1:
                return False
        return True
    
    #If Solved, Return the solution in string format
    def returnSolution(self):
        if self.isSolved():
            stringy = ""
            for coord in self.coordinates:
                a = self.domains[coord].pop()
                if type(a) == tuple:
                    stringy += a[1]
                    self.domains[coord].add(a[1])
                else:
                    stringy += a
                    self.domains[coord].add(a)
            return stringy
        else:
            return("Not Solved")

    def isAssigned(self, coord):
        if len(self.domains[coord]) == 1:
            return True
        else:
            return False
    
    #return PriorityQueue of unassigned variables, small domains first
    def unassigned(self):
        unassigned = PriorityQueue()
        for coord in coordinates:
            if self.isAssigned(coord):
                pass
            else:
                unassigned.put((len(self.domains[coord]), coord))
        return unassigned
    
    def neighbours(self, c):
        cNeighbours = self.rows[c[0]][1] + self.cols[c[1]][1] + self.boxs[self.boxs[c]][1]
        cNeighbours = list(set(cNeighbours))
        cNeighbours.remove(c)
        return cNeighbours



def revise(board, arc):
    newDomain = set()
    length = len(board.domains[arc[0]])
    while(True):
        if (len(board.domains[arc[0]]) != 0):
            value = board.domains[arc[0]].pop()
            if board.domains[arc[1]]=={value}:
                pass
            else:
                newDomain.add(value)
        else:
            board.domains[arc[0]] = newDomain
            break
    
    if length == len(board.domains[arc[0]]):
        return False
    else:
        return True


#Helper Functions to check if a value in a specific position conflicts with its row, column, or box
def rowConflict(board, number, coordinate):

    if number in board.rows[coordinate[0]][0]:
        return True
    
    return False

def colConflict(board, number, coordinate):

    if number in board.cols[coordinate[1]][0]:
        return True
    
    return False
    
def boxConflict(board,number,coordinate):

    if number in board.boxs[board.boxs[coordinate]][0]:

        return True
    return False

def conflict(board,number,coordinate):
    if colConflict(board,number,coordinate) or rowConflict(board,number,coordinate) or boxConflict(board,number,coordinate):
        return True
    else:
        return False

