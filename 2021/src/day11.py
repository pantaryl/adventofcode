from shared import *

# Input data is in INPUT_DATA.
#INPUT_DATA = [int(x) for x in INPUT_DATA]
orig_grid = squareGridFromChars(INPUT_DATA, isInts=True)

# Part 1
def step(grid):
    seen    = set()
    flashes = []
    for pos, val in grid.items():
        val += 1
        grid[pos] = val
        if val > 9 and pos not in seen:
            flashes.append(pos)
            seen.add(pos)

    while flashes:
        pos = flashes.pop(0)
        for neighbor in getAllSquareNeighbors():
            newNeighbor = pos + neighbor
            if newNeighbor in grid and newNeighbor not in seen:
                grid[newNeighbor] += 1
                if grid[newNeighbor] > 9:
                    seen.add(newNeighbor)
                    flashes.append(newNeighbor)

    for pos in list(seen):
        grid[pos] = 0

    return len(seen), all([True if val == 0 else False for _, val in grid.items()])

grid = deepcopy(orig_grid)
print(sum([step(grid)[0] for i in range(100)]))

# Part 2
currentStep = 101
while True:
    _, allFlash = step(grid)
    if allFlash:
        print(currentStep)
        break
    currentStep += 1