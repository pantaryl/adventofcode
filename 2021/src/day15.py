from shared import *

# Input data is in INPUT_DATA.
# INPUT_DATA = [int(x) for x in INPUT_DATA]
grid = squareGridFromChars(INPUT_DATA, isInts=True)

begin = OrderedComplex(0, 0)
end   = OrderedComplex(len(INPUT_DATA[0]) - 1, len(INPUT_DATA) - 1)

# Part 1
heuristic = lambda x: 0
def adjFunc(data):
    grid, current = data
    return [current + neighbor for neighbor in getOrthogonalSquareNeighbors() if current + neighbor in grid]
scoreFunc = lambda grid, pos, neighbor: grid[pos]

print(sum([grid[x] for x in aStar(grid, begin, end, heuristic, adjFunc, scoreFunc) if x != begin]))

# Part 2
# Got to make our bigger grid
totalGrid = {}
for y in range(0, 5):
    for x in range(0, 5):
        multiplier = y + x
        gridPos = OrderedComplex(x, y) * (end.real + 1)
        for pos in grid.keys():
            newVal = grid[pos] + multiplier
            newVal = newVal if newVal < 10 else newVal - 9

            newPos = pos + gridPos
            totalGrid[newPos] = newVal

end = OrderedComplex(len(INPUT_DATA[0]) * 5 - 1, len(INPUT_DATA) * 5 - 1)
print(sum([totalGrid[x] for x in aStar(totalGrid, begin, end, heuristic, adjFunc, scoreFunc) if x != begin]))