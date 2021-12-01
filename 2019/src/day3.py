import operator

with open("../input/day3.txt", 'r') as inputFile:
    data = inputFile.readlines()

assert(len(data) == 2)
wire1 = data[0].split(",")
wire2 = data[1].split(",")

startingLoc = (0, 0)
grid = {}
grid[startingLoc] = ('o', 'Start', { 'Wire1': 0, 'Wire2': 0 } )

def calcManhattanDist(loc: tuple, other: tuple):
    return abs(loc[0] - other[0]) + abs(loc[1] - other[1])

def calcSteps(grid: dict, loc: tuple):
    stepData: dict
    stepData = grid[loc][2]
    return sum(stepData.values())

def checkLoc(grid: dict, loc: tuple, id: str):
    if loc in grid:
        type, gridId, steps = grid[loc]
        if type == 'o':
            return -1
        elif gridId != id:
            return 1
    return 0

directions = {
    'R': ( (1,  0), "-" ),
    'L': ( (-1, 0), '-' ),
    'U': ( (0,  1), '|' ),
    'D': ( (0, -1), '|' ),
}

intersections = set()

def runWire(grid: dict, wire: list, intersections: set, startingLoc: tuple, id: str):
    currentLoc = startingLoc
    steps = 0
    for direction in wire:
        cardinal = direction[0]
        count    = int(direction[1:])

        dirData = directions[cardinal]
        for i in range(count):
            steps += 1
            newLoc = tuple(map(operator.add, currentLoc, dirData[0]))
            results = checkLoc(grid, newLoc, id)
            if results == 1:
                existingStepData = grid[newLoc][2]
                grid[newLoc] = ('X', 'Cross', existingStepData)
                grid[newLoc][2][id] = steps
                intersections.add(newLoc)
            elif results == 0:
                grid[newLoc] = (dirData[1], id, {})
                grid[newLoc][2][id] = steps
            currentLoc = newLoc

runWire(grid, wire1, intersections, startingLoc, "Wire1")
runWire(grid, wire2, intersections, startingLoc, "Wire2")

minDist  = 999999999999999
minSteps = 999999999999999
for intersection in intersections:
    minDist  = min(minDist,  calcManhattanDist(startingLoc, intersection))
    minSteps = min(minSteps, calcSteps(grid, intersection))

# Part 1
print(minDist)

# Part 2
print(minSteps)