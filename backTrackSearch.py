from queue import Queue, PriorityQueue
import copy


def backTrackSearch(board):
    while(True):

        #Build variable priority based on minimum value heuristic
        backtrackVariables = board.unassigned()
        if board.isSolved():
            return True
        if backtrackVariables.empty():
            break
        var = backtrackVariables.get()
        domain = list(board.domains[var[1]])
        domains = copy.deepcopy(board.domains)

        #Build Value Priority of chosen variable based on least constraining value
        neighbours = board.neighbours(var[1])
        valueScores = PriorityQueue()
        for value in domain:
            valueScore = 0
            for neighbour in neighbours:
                if value in board.domains[neighbour]:
                    valueScore += 1
            valueScores.put((valueScore, value))

        #Recursively Call backTrackSearch Until you reach the end of a branch
        while(True):
            if valueScores.empty() == False:
                value = valueScores.get()
                board.domains[var[1]] = {value[1]}
                check = []
                for neighbour in neighbours:
                    check.append(board.domains[neighbour] == board.domains[var[1]])
                if any(check):
                    pass
                else:
                    arcs = set()
                    for neighbour in neighbours:
                        arcs.add((neighbour, var[1]))
                    if board.MAC(arcs):
                        result = backTrackSearch(board)
                        if result:
                            return result
                        else:
                            board.domains = domains
                    else:
                        board.domains = domains
            else:
                break
        return False