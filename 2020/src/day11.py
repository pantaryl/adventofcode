from collections import defaultdict
from helpers import memoize
from copy import deepcopy

with open("../input/day11.txt", 'r') as inputFile:
    data = [x.rstrip() for x in inputFile.readlines()]
    #data = [int(x) for x in data]

map = {}
yMax = len(data)
xMax = len(data[0])
for y in range(yMax):
    line = data[y]
    for x in range(xMax):
        map[(x, y)] = line[x]

def anyAdjacentOccupied(x, y, oldMap) -> bool:
    for xVals in [-1, 0, 1]:
        for yVals in [-1, 0, 1]:
            if xVals == 0 and yVals == 0: continue
            if (xVals+x, yVals+y) in oldMap and oldMap[(xVals+x, yVals+y)] == "#":
                return True

    return False

def alsoOccupied(x, y, oldMap) -> bool:
    count = 0

    for xVals in [-1, 0, 1]:
        for yVals in [-1, 0, 1]:
            if xVals == 0 and yVals == 0: continue
            if (xVals+x, yVals+y) in oldMap and oldMap[(xVals+x, yVals+y)] == "#":
                count += 1

    return count >= 4

def printMap(map):
    for y in range(yMax):
        for x in range(xMax):
            print(map[(x, y)], end='')
        print()

# Part 1
oldMap = deepcopy(map)
for i in range(5000):
    changed = False
    newMap  = deepcopy(oldMap)
    for x in range(xMax):
        for y in range(yMax):
            if oldMap[(x, y)] == "L" and anyAdjacentOccupied(x, y, oldMap) is False:
                newMap[(x, y)] = "#"
                changed = True
            elif oldMap[(x, y)] == "#" and alsoOccupied(x, y, oldMap):
                newMap[(x, y)] = "L"
                changed = True

    if changed is False:
        occupied = 0
        for _, value in newMap.items():
            occupied += 1 if value == "#" else 0
        print(occupied)
        break
    else:
        oldMap = newMap
        #printMap(oldMap)
        #print()
        #print()


# Part 2
def anyAdjacentOccupied2(x, y, oldMap) -> bool:
    slopes = [(-1, -1), (-1, 0), (-1, 1),
              (0,  -1),          (0,  1),
              (1,  -1), (1,  0), (1,  1)]
    for slope in slopes:
        currentXY = (x + slope[0], y + slope[1])
        while currentXY in oldMap:
            if oldMap[currentXY] == "L":
                break
            elif oldMap[currentXY] == "#":
                return True
            currentXY = (currentXY[0] + slope[0], currentXY[1] + slope[1])

    return False

def alsoOccupied2(x, y, oldMap) -> bool:
    count = 0
    slopes = [(-1, -1), (-1, 0), (-1, 1),
              (0,  -1),          (0,  1),
              (1,  -1), (1,  0), (1,  1)]
    for slope in slopes:
        currentXY = (x + slope[0], y + slope[1])
        while currentXY in oldMap:
            if oldMap[currentXY] == "L":
                break
            elif oldMap[currentXY] == "#":
                count += 1
                break
            currentXY = (currentXY[0] + slope[0], currentXY[1] + slope[1])

    return count >= 5

oldMap = deepcopy(map)
for i in range(500000):
    changed = False
    newMap  = deepcopy(oldMap)
    for x in range(xMax):
        for y in range(yMax):
            if oldMap[(x, y)] == "L" and anyAdjacentOccupied2(x, y, oldMap) is False:
                newMap[(x, y)] = "#"
                changed = True
            elif oldMap[(x, y)] == "#" and alsoOccupied2(x, y, oldMap):
                newMap[(x, y)] = "L"
                changed = True

    if changed is False:
        occupied = 0
        for _, value in newMap.items():
            occupied += 1 if value == "#" else 0
        print(occupied)
        break
    else:
        oldMap = newMap
        #printMap(oldMap)
        #print()
        #print()
        #input()