import sys
import time

allDirs = {
    "north": [-1, 0],
    "east": [0, 1],
    "south": [1, 0],
    "west": [0, -1]
}
dirOpposites = {
    "north": "south",
    "east": "west",
    "south": "north",
    "west": "east"
}
pipes = {
    "-": ["east","west"],
    "|": ["north","south"],
    "L": ["north","east"],
    "J": ["north","west"],
    "7": ["south","west"],
    "F": ["east","south"],
    ".": [],
    "S": []
}

def solvepart1():
    #read in data
    data = fileRead("input.txt")
    grid = []
    for row in data:
        gridRow = list(row.strip())
        grid.append(gridRow)
    
    #locate S and find valid directions off of S
    startCoord = [0,0]
    stepperStarts = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (grid[i][j]=="S"):
                startCoord = [i,j]
                break
    for direction, dirCoord in allDirs.items():
        newCoord = [startCoord[0] + dirCoord[0], startCoord[1] + dirCoord[1]]
        if dirOpposites[direction] in pipes[grid[newCoord[0]][newCoord[1]]]:
            stepperStarts.append(newCoord)
    
    #step through loop until pipes meet
    stepper1 = stepperStarts[0]
    stepper2 = stepperStarts[1]
    stepper1prev = startCoord.copy()
    stepper2prev = startCoord.copy()
    stepcount = 1
    while(stepper1 != stepper2):

        newStepper1 = traverse(grid, stepper1prev, stepper1)
        stepper1prev = stepper1.copy()
        stepper1 = newStepper1.copy()

        newStepper2 = traverse(grid, stepper2prev, stepper2)
        stepper2prev = stepper2.copy()
        stepper2 = newStepper2.copy()

        stepcount = stepcount + 1
    print(stepcount)
    
def solvepart2():
    #read in data
    data = fileRead("input.txt")
    grid = []
    for row in data:
        gridRow = list(row.strip())
        grid.append(gridRow)

    #add space between each point in grid
    spacedGrid = [["+"]*((len(grid[0])*2)+1)]
    for i in range(len(grid)):
        spacedRow = []
        spacedRow.append("+")
        for j in range(len(grid[0])):
            spacedRow.append(grid[i][j])
            spacedRow.append("+")
        spacedGrid.append(spacedRow)
        spacedGrid.append(["+"]*((len(grid[0])*2)+1))
    
    #locate S and find valid directions off of S
    startCoord = [0,0]
    stepperStarts = []
    startDirs = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (grid[i][j]=="S"):
                startCoord = [i,j]
                break
    for direction, dirCoord in allDirs.items():
        newCoord = [startCoord[0] + dirCoord[0], startCoord[1] + dirCoord[1]]
        if dirOpposites[direction] in pipes[grid[newCoord[0]][newCoord[1]]]:
            stepperStarts.append(newCoord)
            startDirs.append(direction)
    
    #step through loop and build spaced grid
    stepper1 = stepperStarts[0]
    stepper1prev = startCoord.copy()
    pipeList = [spaced(startCoord), spaced(stepper1)]
    prevdir = []
    while(grid[stepper1[0]][stepper1[1]] != "S"):
        newStepper1, prevdir = spacedTraverse(grid, stepper1prev, stepper1)

        connector = spaced(stepper1)
        connector[0] = connector[0] + allDirs[prevdir][0]
        connector[1] = connector[1] + allDirs[prevdir][1]
        if prevdir in ["north", "south"]:
            spacedGrid[connector[0]][connector[1]] = "|"
        else:
            spacedGrid[connector[0]][connector[1]] = "-"

        stepper1prev = stepper1.copy()
        stepper1 = newStepper1.copy()

        pipeList.append(connector.copy())
        pipeList.append(spaced(stepper1))

    prevdir = startDirs[1]
    connector = spaced(stepper1)
    connector[0] = connector[0] + allDirs[prevdir][0]
    connector[1] = connector[1] + allDirs[prevdir][1]
    if prevdir in ["north", "south"]:
        spacedGrid[connector[0]][connector[1]] = "|"
    else:
        spacedGrid[connector[0]][connector[1]] = "-"
    pipeList.append(connector.copy())

    #print spaced grid nicely
    # print(pipeList)
    # for i in range(len(spacedGrid)):
    #     str = ""
    #     for j in range(len(spacedGrid[0])):
    #         if ([i,j] in pipeList):
    #             str = str + "*"
    #         else:
    #             str = str + "."
    #     print(str)
            

    #reursively check for enclosed spaces
    checkedSpaces = []
    sumEnclosed = 0
    sys.setrecursionlimit(100000)
    for i in range(len(spacedGrid)):
        for j in range(len(spacedGrid[0])):
            if ([i,j] not in checkedSpaces) and ([i,j] not in pipeList):
                print("area 1")
                enclosed, sumSpaces = flood(spacedGrid, pipeList, checkedSpaces, [i,j])
                if enclosed:
                    sumEnclosed = sumEnclosed + sumSpaces
                    print("enclosed: ", sumSpaces)
                print("open: ", sumSpaces) 
    print(sumEnclosed)
    

# takes in the grid and current step and previous step as coordinates, and returns coordinates of next step
def traverse(grid, prevStep, currStep):
    pipe = grid[currStep[0]][currStep[1]]
    prevdircoords = [ ( prevStep[0]-currStep[0] ), ( prevStep[1]-currStep[1] ) ]
    prevdir = list(allDirs.keys())[list(allDirs.values()).index(prevdircoords)]
    validDirs = pipes[pipe].copy()
    validDirs.remove(prevdir)
    nextDir = allDirs[validDirs[0]].copy()
    nextStep = currStep.copy()
    nextStep[0] = nextStep[0]+nextDir[0]
    nextStep[1] = nextStep[1]+nextDir[1]
    return nextStep

#steps through grid, and help build spaced grid
def spacedTraverse(grid, prevStep, currStep):
    pipe = grid[currStep[0]][currStep[1]]
    prevdircoords = [ ( prevStep[0]-currStep[0] ), ( prevStep[1]-currStep[1] ) ]
    prevdir = list(allDirs.keys())[list(allDirs.values()).index(prevdircoords)]
    validDirs = pipes[pipe].copy()
    validDirs.remove(prevdir)
    nextDir = allDirs[validDirs[0]].copy()
    nextStep = currStep.copy()
    nextStep[0] = nextStep[0]+nextDir[0]
    nextStep[1] = nextStep[1]+nextDir[1]
    return nextStep, prevdir

#takes in a coordinate and returns the spaced version of it
def spaced(coord):
    return [(coord[0]*2)+1,(coord[1]*2)+1]

#check if a location is fully within the pipe by recurseively checking all adjacent spaces, returns whether space is in pipe and how much space it covered
def flood(grid, pipeList, checkedSpaces, target):
    print("checked space: ", target)
    if (target in pipeList) or (target in checkedSpaces):
        return True, 0 #location is invalid (pipe or already checked)
    elif ( target[0] < 0 ) or ( target[0] >= len(grid) ) or ( target[1] < 0 ) or ( target[1] >= len(grid[0]) ):
        return False, 0 #location is off of grid (area is not enclosed)
    else:
        checkedSpaces.append(target)
        sumSpaces = 0;
        enclosed = True

        for dirCoord in allDirs.values():
            newTarget = target.copy()
            newTarget[0] = newTarget[0] + dirCoord[0]
            newTarget[1] = newTarget[1] + dirCoord[1]
            newEnclosed, numSpaces = flood(grid, pipeList, checkedSpaces, newTarget)
            sumSpaces = sumSpaces + numSpaces
            enclosed = enclosed and newEnclosed

        if ( grid[target[0]][target[1]] != "+"):
            return enclosed, sumSpaces + 1 #location is open and not open space
        else:
            return enclosed, sumSpaces #loation is open and open space

def fileRead(name):
    data = []
    f = open(name, "r")
    for line in f:
        data.append(line);
    return data


solvepart2()