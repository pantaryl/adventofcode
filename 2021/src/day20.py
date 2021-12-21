from shared import *

# Input data is in INPUT_DATA.
# INPUT_DATA = [int(x) for x in INPUT_DATA]

enhancement = [x for x in INPUT_DATA[0]]
grid = squareGridFromChars(INPUT_DATA[2:], isInts=False, toSetOnValue='#')

# Part 1
def step(theGrid: set, on):
    newGrid = set()

    minX = int(min([x.real for x in theGrid]))
    maxX = int(max([x.real for x in theGrid]))
    minY = int(min([x.imag for x in theGrid]))
    maxY = int(max([x.imag for x in theGrid]))

    for y in range(minY - 2, maxY + 3):
        for x in range(minX - 2, maxX + 3):
            pos = complex(x, y)
            neighbors = [ pos + -1-1j, pos + 0-1j, pos + 1-1j,
                          pos + -1+0j, pos + 0+0j, pos + 1+0j,
                          pos + -1+1j, pos + 0+1j, pos + 1+1j]

            strVal = "".join(['1' if (pos in theGrid) == on else '0' for pos in neighbors])
            index = int(strVal, 2)

            if (enhancement[index] == '#') != on:
                newGrid.add(pos)

    return newGrid

def printGrid(theGrid):
    minX = int(min([x.real for x in theGrid]))
    maxX = int(max([x.real for x in theGrid]))
    minY = int(min([x.imag for x in theGrid]))
    maxY = int(max([x.imag for x in theGrid]))

    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            print('#' if complex(x, y) in theGrid else '.', end='')
        print()
    print()

for i in range(50):
    if enhancement[0] != enhancement[-1] and enhancement[0] == '#':
        on = i % 2 == 0
    else:
        on = False
    grid = step(grid, on)

    if i == 1: print(len(grid))
print(len(grid))

# Part 2
