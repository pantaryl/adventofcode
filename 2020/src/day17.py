from collections import defaultdict
from helpers import memoize
from copy import deepcopy
import os
from math_utils import *

# Complex numbers in Python! == i + nj (x + ny), good for coordinates
# complex*+imaginary to rotate left/ccw, complex*-imaginary to rotate right/cw
# For example:
# Rotate CCW by 270 degrees:
#    val *= complex(0, 1) ** 3 [each power represents 90 degrees]

with open(f"../input/{os.path.splitext(os.path.basename(__file__))[0]}.txt", 'r') as inputFile:
    data = [x.rstrip() for x in inputFile.readlines()]
    #data = [int(x) for x in data]

map = defaultdict(lambda: defaultdict(lambda: "."))

for y in range(len(data)):
    for x in range(len(data[0])):
        map[0][complex(x, y)] = data[y][x]

# Part 1
def getNeighbors1(position, slice):
    return [
        (position + complex(-1, -1), slice),
        (position + complex(0,  -1), slice),
        (position + complex(1,  -1), slice),
        (position + complex(-1,  0), slice),
        (position + complex(1,   0), slice),
        (position + complex(-1,  1), slice),
        (position + complex(0,   1), slice),
        (position + complex(1,   1), slice),

        (position + complex(-1, -1), slice - 1),
        (position + complex(0,  -1), slice - 1),
        (position + complex(1,  -1), slice - 1),
        (position + complex(-1,  0), slice - 1),
        (position + complex(0,   0), slice - 1),
        (position + complex(1,   0), slice - 1),
        (position + complex(-1,  1), slice - 1),
        (position + complex(0,   1), slice - 1),
        (position + complex(1,   1), slice - 1),

        (position + complex(-1, -1), slice + 1),
        (position + complex(0,  -1), slice + 1),
        (position + complex(1,  -1), slice + 1),
        (position + complex(-1,  0), slice + 1),
        (position + complex(0,   0), slice + 1),
        (position + complex(1,   0), slice + 1),
        (position + complex(-1,  1), slice + 1),
        (position + complex(0,   1), slice + 1),
        (position + complex(1,   1), slice + 1),
    ]

def detActiveNeighbors1(map, pos, slice):
    neighbors = getNeighbors1(pos, slice)
    active = 0
    for neighbor in neighbors:
        if map[neighbor[1]][neighbor[0]] == '#': active += 1
    return active

def printMap1(map):
    for i in sorted(map.keys()):
        slice = map[i]

        print(f"Slice: {i}")
        sortedPos = sorted(slice.keys(), key=lambda x: (x.imag, x.real))
        lastY = sortedPos[0].imag
        for j in sortedPos:
            if j.imag != lastY: print()
            lastY = j.imag
            print(slice[j], end='')
        print()

def makeEmptySlice1(currentSlice):
    slice = defaultdict(lambda:".")
    for pos, cube in currentSlice.items():
        slice[pos] = '.'
    return slice

def addEdge1(map):
    slices = list(map.keys())
    for sliceIdx in slices:
        slice = map[sliceIdx]

        origPos = list(slice.keys())
        for pos in origPos:
            newPos = [
                pos + complex(-1, -1),
                pos + complex(-1,  0),
                pos + complex(-1,  1),
                pos + complex( 0, -1),
                pos + complex( 0,  0),
                pos + complex( 0,  1),
                pos + complex( 1, -1),
                pos + complex( 1,  0),
                pos + complex( 1,  1),
            ]
            for new in newPos:
                if new not in slice:
                    slice[new] = "."

def step1(oldMap):
    lowestSlice  = sorted(oldMap.keys())[0]
    largestSlice = sorted(oldMap.keys())[-1]

    oldMap[lowestSlice  - 1] = makeEmptySlice1(oldMap[lowestSlice])
    oldMap[largestSlice + 1] = makeEmptySlice1(oldMap[largestSlice])
    addEdge1(oldMap)
    oldMapCopy = deepcopy(oldMap)

    newMap     = deepcopy(oldMap)
    for slice, positions in oldMap.items():
        for pos, cube in oldMap[slice].items():
            activeNeighbors = detActiveNeighbors1(oldMapCopy, pos, slice)
            if cube == "." and activeNeighbors == 3:
                newMap[slice][pos] = '#'
            elif cube == "#" and (activeNeighbors < 2 or activeNeighbors > 3):
                newMap[slice][pos] = "."

    #printMap(newMap)
    return newMap

def countActive1(map):
    active = 0
    for _, positions in map.items():
        for __, cube in positions.items():
            if cube == '#': active += 1
    return active

oldMap = deepcopy(map)
for i in range(0, 7):
    #print(f"Step {i}")
    if i == 0:
        #printMap(oldMap)
        continue
    else:
        oldMap = step1(oldMap)
    #print()

print(countActive1(oldMap))

# Part 2
# Instead of building the full four-dimensional cube, just track the active spaces
# and check all of their neighbors.
active = set()
for y, yLine in enumerate(data):
    for x, xChar in enumerate(yLine):
        if xChar == '#': active.add((x, y, 0, 0))

for step in range(6):
    newActive  = set()
    posToCheck = set()

    for (x, y, z, w) in active:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    for dw in [-1, 0, 1]:
                        posToCheck.add((x + dx, y + dy, z + dz, w + dw))

    for (x, y, z, w) in posToCheck:
        neighborCount = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    for dw in [-1, 0, 1]:
                        if dx == dy == dz == dw == 0: continue
                        newPos = (x + dx, y + dy, z + dz, w + dw)
                        if newPos in active:
                            neighborCount += 1
        if (x, y, z, w) not in active and neighborCount == 3:
            newActive.add((x, y, z, w))
        if (x, y, z, w) in active and neighborCount in [2, 3]:
            newActive.add((x, y, z, w))

    active = newActive
print(len(active))
