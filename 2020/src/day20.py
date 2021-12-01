from collections import defaultdict
from helpers import memoize
from copy import deepcopy
from enum import Enum
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

class Dir(Enum):
    Top = 0
    Right = 1
    Bottom = 2
    Left   = 3

tiles = defaultdict(dict)

id = None
tile = []
tileDim = 0
for i in range(len(data)):
    line = data[i]
    if "Tile" in line:
        id = line.split(" ")[1][:-1]
        y  = 0
    elif line == "" or line == "\n" or i + 1 == len(data):
        if i + 1 == len(data) and line != "": tile.append(line)
        tiles[id][Dir.Top] = tile[0]
        tiles[id][Dir.Right] = "".join([x[-1] for x in tile])
        tiles[id][Dir.Bottom] = tile[-1]
        tiles[id][Dir.Left] = "".join([x[0] for x in tile])
        tiles[id]['all'] = tile
        tile = []
        id = None
        continue
    else:
        assert(tileDim == 0 or tileDim == len(line))
        tileDim = len(line)
        tile.append(line)

def rotateTile(tile, turnsCw):
    newTile = deepcopy(tile)
    for i in range(turnsCw):
        temp                = newTile[Dir.Left]
        newTile[Dir.Left]   = newTile[Dir.Bottom]
        newTile[Dir.Bottom] = newTile[Dir.Right][::-1]
        newTile[Dir.Right]  = newTile[Dir.Top]
        newTile[Dir.Top]    = temp[::-1]
    return newTile

def flipTile(tile, aroundVertAxis):
    newTile = deepcopy(tile)
    if aroundVertAxis is not None:
        if aroundVertAxis:
            newTile[Dir.Top]    = newTile[Dir.Top][::-1]
            newTile[Dir.Bottom] = newTile[Dir.Bottom][::-1]

            temp                = newTile[Dir.Left]
            newTile[Dir.Left]   = newTile[Dir.Right]
            newTile[Dir.Right]  = temp
        else:
            temp                = newTile[Dir.Top]
            newTile[Dir.Top]    = newTile[Dir.Bottom]
            newTile[Dir.Bottom] = temp

            newTile[Dir.Left]   = newTile[Dir.Left][::-1]
            newTile[Dir.Right]  = newTile[Dir.Right][::-1]
    return newTile

matchingDir = {
    Dir.Top: Dir.Bottom,
    Dir.Bottom: Dir.Top,
    Dir.Left: Dir.Right,
    Dir.Right: Dir.Left,
}

numTiles = len(tiles.keys())
mapDim   = int(numTiles**(0.5))

def outOfBounds(loc: complex, dim: int):
    return loc.real < 0 or loc.real >= dim or loc.imag < 0 or loc.imag >= dim

def checkNeighbors(idByLocation, tileById, myTile, myLoc):
    for neighbor in [(Dir.Left, complex(-1, 0)), (Dir.Top, complex(0, -1)), (Dir.Right, complex(1, 0)), (Dir.Bottom, complex(0, 1))]:
        neighborDir = neighbor[0]
        neighborLoc = myLoc + neighbor[1]
        if neighborLoc in idByLocation:
            neighborId   = idByLocation[neighborLoc]
            neighborTile = tileById[neighborId]
            if myTile[neighborDir] != neighborTile[matchingDir[neighborDir]]:
                return False
    return True

part1 = None
for id, edges in tiles.items():
    for rotateMe in [0, 1, 2, 3]:
        for flipMe in [None, True, False]:
            myTile        = rotateTile(tiles[id], rotateMe)
            myTile        = flipTile(myTile, flipMe)
            tileById      = {id: myTile}
            finalOpsById  = {id: {'rot': rotateMe, 'flip': flipMe}}
            locationsById = {id: complex(0, 0)}
            idByLocation =  {complex(0, 0): id}

            earlyOut = False
            for x in range(0, mapDim):
                for y in range(0, mapDim):
                    neighborLoc = locationsById[id] + complex(x, y)
                    if neighborLoc not in idByLocation and not outOfBounds(neighborLoc, mapDim):
                        for otherId, otherEdges in tiles.items():
                            if otherId in tileById: continue
                            for rotate in [0, 1, 2, 3]:
                                for flip in [None, True, False]:
                                    newTile = rotateTile(tiles[otherId], rotate)
                                    newTile = flipTile(newTile, flip)
                                    if checkNeighbors(idByLocation, tileById, newTile, neighborLoc):
                                        tileById[otherId] = newTile
                                        locationsById[otherId] = neighborLoc
                                        idByLocation[neighborLoc] = otherId
                                        finalOpsById[otherId] = {'rot': rotate, 'flip': flip}
                                        break
                                    if otherId in tileById: break
                                if otherId in tileById: break
                            if otherId in tileById: break
                        if neighborLoc not in idByLocation and not outOfBounds(neighborLoc, mapDim):
                            earlyOut = True
                            break
                if earlyOut: break
            if earlyOut: continue

            print(f"{len(idByLocation.keys())}, {len(tiles.keys())}")
            if len(idByLocation.keys()) == len(tiles.keys()):
                topLeft     = int(idByLocation[complex(0, 0)])
                topRight    = int(idByLocation[complex(mapDim - 1, 0)])
                bottomLeft  = int(idByLocation[complex(0, mapDim - 1)])
                bottomRight = int(idByLocation[complex(mapDim - 1, mapDim - 1)])
                print(topLeft * topRight * bottomLeft * bottomRight)
                part1 = (idByLocation, finalOpsById)
                break
        if part1: break
    if part1: break

idByLocation, finalOpsById = part1
# Uncomment these to checkpoint so you don't have to run the long logic above.
#print(f"idByLocation: {idByLocation}")
#print(f"finalOpsById: {finalOpsById}")

finalImage = defaultdict(str)

tileDim -= 2
finalMapDim = tileDim * mapDim

for y in range(mapDim):
    for x in range(mapDim):
        loc      = complex(x, y)
        id       = idByLocation[loc]
        tile     = tiles[id]
        finalOps = finalOpsById[id]

        newImage = {}
        for tileY, line in enumerate(tile['all'][1:-1]):
            if tileY >= tileDim: continue
            for tileX, char in enumerate(line[1:-1]):
                if tileX >= tileDim: continue

                currentX = tileX
                currentY = tileY
                for i in range(0, finalOps['rot']):
                    temp     = currentX
                    currentX = tileDim - currentY - 1
                    currentY = temp

                newImage[complex(currentX, currentY)] = char

        tileOffset = (x * tileDim, y * tileDim)
        for tileY in range(0, tileDim):
            for tileX in range(0, tileDim):
                pos = {
                    None: complex(tileX, tileY),
                    True: complex(tileDim - tileX - 1, tileY),
                    False: complex(tileX, tileDim - tileY - 1)
                }[finalOps['flip']]
                char = newImage[pos]
                finalImage[tileOffset[1] + tileY] += char

posToCheck = [
    (18, 0),
    (0,  1),
    (5,  1),
    (6,  1),
    (11, 1),
    (12, 1),
    (17, 1),
    (18, 1),
    (19, 1),
    (1,  2),
    (4,  2),
    (7,  2),
    (10, 2),
    (13, 2),
    (16, 2),
]

count = 0
for rotate in [0, 1, 2, 3]:
    for flip in [None, True, False]:
        workingImage = deepcopy(finalImage)
        count        = 0
        for y in range(finalMapDim):
            for x in range(finalMapDim):
                currentX = x
                currentY = y
                for i in range(rotate):
                    temp = currentX
                    currentX = finalMapDim - currentY - 1
                    currentY = temp

                pos = {
                    None: (currentX, currentY),
                    True: (finalMapDim - currentX - 1, currentY),
                    False: (currentX, finalMapDim - currentY- 1)
                }[flip]

                workingImage[pos[1]] = workingImage[pos[1]][0:pos[0]] + finalImage[y][x] + workingImage[pos[1]][pos[0]+1:]

        for x in range(finalMapDim - 20):
            for y in range(finalMapDim - 3):
                for newX, newY in posToCheck:
                    if x+newX >= len(workingImage[y+newY]):
                        print()
                if all([True if workingImage[y+newY][x+newX] == '#' else False for newX, newY in posToCheck]):
                    count += 1
                    for newX, newY in posToCheck:
                        workingImage[y+newY] = workingImage[y+newY][0:x+newX] + 'O' + workingImage[y+newY][x+newX+1:]

        if count > 0:
            safeSpaces = 0
            for line in workingImage.values():
                safeSpaces += line.count('#')
            print(safeSpaces)
            print()
            for line in workingImage.values():
                print(line)
            break
    if count > 0: break
