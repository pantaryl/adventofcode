from collections import deque

with open("../input/day24.txt", 'r') as inputFile:
    data = [[x for x in line.rstrip()] for line in inputFile.readlines()]

grid = {}
for y in range(len(data)):
    line = data[y]
    for x in range(len(line)):
        char = line[x]
        grid[x + y*1j] = char

def makeEmptyGrid():
    newGrid = {}
    for y in range(5):
        for x in range(5):
            newGrid[x + y*1j] = '.'
    return newGrid

def getCountNeighbors(grid: dict, pos: complex, ignoreCenter: bool = False, aboveGrid: dict = None, belowGrid: dict = None):
    if ignoreCenter and pos == 2+2j:
        return 0
    count = 0
    for idx, neighbor in enumerate([1+0j, -1+0j, 0+1j, 0-1j]):
        neighborPos = pos + neighbor
        if ignoreCenter and neighborPos == 2+2j:
            continue
        if neighborPos in grid and grid[neighborPos] == '#':
            count += 1

    if pos == 1+2j:
        count += sum([1 if belowGrid[0+y*1j] == "#" else 0 for y in range(5)]) if belowGrid else 0
    elif pos == 3+2j:
        count += sum([1 if belowGrid[4+y*1j] == "#" else 0 for y in range(5)]) if belowGrid else 0
    elif pos == 2+1j:
        count += sum([1 if belowGrid[x+0j] == "#" else 0 for x in range(5)]) if belowGrid else 0
    elif pos == 2+3j:
        count += sum([1 if belowGrid[x+4j] == "#" else 0 for x in range(5)]) if belowGrid else 0

    if int(pos.real) == 0:
        count += sum([(1 if aboveGrid[1+2j] == "#" else 0)]) if aboveGrid else 0
    elif int(pos.real) == 4:
        count += sum([(1 if aboveGrid[3+2j] == "#" else 0)]) if aboveGrid else 0

    if int(pos.imag) == 0:
        count += (1 if aboveGrid[2+1j] == '#' else 0) if aboveGrid else 0
    elif int(pos.imag) == 4:
        count += (1 if aboveGrid[2+3j] == '#' else 0) if aboveGrid else 0
    return count

def makeHash(grid: dict):
    hash = 0
    for i in range(25):
        x = i % 5
        y = i // 5
        if grid[x + y*1j] == '#':
            hash += pow(2, i)
    return hash

def step(grid: dict, ignoreCenter: bool = False, aboveGrid: dict = None, belowGrid: dict = None):
    newGrid = {}
    for pos, type in grid.items():
        if type == '.':
            if 1 <= getCountNeighbors(grid, pos, ignoreCenter, aboveGrid, belowGrid) <= 2:
                newGrid[pos] = '#'
            else:
                newGrid[pos] = "."
        elif type == '#':
            if getCountNeighbors(grid, pos, ignoreCenter, aboveGrid, belowGrid) == 1:
                newGrid[pos] = '#'
            else:
                newGrid[pos] = "."
    return newGrid

def printGrid(grid: dict):
    for y in range(5):
        for x in range(5):
            print(grid[x + y*1j], end='')
        print()
    print()

# Part 1
seenCases  = set()
currentGrid = dict(grid)
currentHash = makeHash(currentGrid)
while currentHash not in seenCases:
    seenCases.add(currentHash)
    currentGrid = step(currentGrid)
    currentHash = makeHash(currentGrid)
print("Part1:", currentHash)

grids = [dict(grid)]
for stepIdx in range(200):
    grids = [makeEmptyGrid()] + grids
    grids.append(makeEmptyGrid())

    newGrids = []

    for idx in range(len(grids)):
        mainGrid  = grids[idx]
        aboveGrid = grids[idx - 1] if idx > 0              else None
        belowGrid = grids[idx + 1] if idx + 1 < len(grids) else None

        result = step(mainGrid, True, aboveGrid, belowGrid)
        newGrids.append(result)
    assert(len(newGrids) == len(grids))
    grids = newGrids

print("Part2:", sum([sum([1 if grid[x + y*1j] == '#' else 0 for x in range(5) for y in range(5)]) for grid in grids]))