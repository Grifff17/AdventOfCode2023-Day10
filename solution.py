
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

def fileRead(name):
    data = []
    f = open(name, "r")
    for line in f:
        data.append(line);
    return data

solvepart1()