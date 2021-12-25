from shared import *

# Input data is in INPUT_DATA.
#INPUT_DATA = [int(x) for x in INPUT_DATA]

grid = squareGridFromChars(INPUT_DATA, isInts=False)
xRange = range(int(min([x.real for x in grid.keys()])), int(max([x.real for x in grid.keys()])) + 1)
yRange = range(int(min([x.imag for x in grid.keys()])), int(max([x.imag for x in grid.keys()])) + 1)

print(max(xRange))

east = set()
south = set()

for pos, val in grid.items():
    if val == '>':
        east.add(pos)
    elif val == 'v':
        south.add(pos)

# Part 1
def step(oldEast, oldSouth):
    newEast = set()
    newSouth = set()

    for pos in oldEast:
        newPos = pos + 1+0j
        if newPos.real > max(xRange):
            newPos = complex(0, pos.imag)

        if newPos not in oldEast and newPos not in oldSouth:
            newEast.add(newPos)
        else:
            newEast.add(pos)

    for pos in oldSouth:
        newPos = pos + 0+1j
        if newPos.imag > max(yRange):
            newPos = complex(pos.real, 0)

        if newPos not in newEast and newPos not in oldSouth and newPos not in newEast:
            newSouth.add(newPos)
        else:
            newSouth.add(pos)

    return newEast, newSouth, oldEast == newEast and oldSouth == newSouth

def printState(east, south):
    for y in yRange:
        for x in xRange:
            pos = complex(x, y)
            if pos in east:
                print('>', end='')
            elif pos in south:
                print('v', end='')
            else:
                print('.', end='')
        print()
    print()

#printState(east, south)
index   = 0
matches = False
while matches == False:
    east, south, matches = step(east, south)
    index += 1

    #printState(east, south)
    pass
print(index)
# Part 2