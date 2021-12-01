from collections import defaultdict, deque
from helpers import memoize
from copy import deepcopy
from enum import Enum
import os
from math_utils import *
from helpers import *

# Complex numbers in Python! == i + nj (x + ny), good for coordinates
# complex*+imaginary to rotate left/ccw, complex*-imaginary to rotate right/cw
# For example:
# Rotate CCW by 270 degrees:
#    val *= complex(0, 1) ** 3 [each power represents 90 degrees]

with open(f"../input/{os.path.splitext(os.path.basename(__file__))[0]}.txt", 'r') as inputFile:
    data = [x.rstrip() for x in inputFile.readlines()]
    #data = [int(x) for x in data]

class Direction(Enum):
    East = 0
    Northeast = 1
    Northwest = 2
    West = 3
    Southwest = 4
    Southeast = 5

def addDir(current, add):
    return (current[0] + add[0],
            current[1] + add[1],
            current[2] + add[2])

CubeDirections = [
    (+1, -1, 0), # East
    (+1, 0, -1), # Northeast
    (0, +1, -1), # Northwest
    (-1, +1, 0), # West
    (-1, 0, +1), # Southwest
    (0, -1, +1), # SouthEast
]

grid = defaultdict(bool)
for line in data:
    pos     = (0, 0, 0)
    current: str
    current = deepcopy(line)
    while current:
        if current.startswith('e'):
            pos = addDir(pos, CubeDirections[Direction.East.value])
            current = current[1:]
        elif current.startswith('ne'):
            pos = addDir(pos, CubeDirections[Direction.Northeast.value])
            current = current[2:]
        elif current.startswith('nw'):
            pos = addDir(pos, CubeDirections[Direction.Northwest.value])
            current = current[2:]
        elif current.startswith('w'):
            pos = addDir(pos, CubeDirections[Direction.West.value])
            current = current[1:]
        elif current.startswith('sw'):
            pos = addDir(pos, CubeDirections[Direction.Southwest.value])
            current = current[2:]
        elif current.startswith('se'):
            pos = addDir(pos, CubeDirections[Direction.Southeast.value])
            current = current[2:]
        else:
            assert(False)

    grid[pos] = grid[pos] == False

print(sum([1 if value else 0 for _, value in grid.items()]))

def solve(grid: dict, steps: int):
    for i in range(steps):
        currentGrid = deepcopy(grid)
        for pos in list(grid.keys()):
            for j in range(len(CubeDirections)):
                newPos = addDir(pos, CubeDirections[j])
                if newPos not in grid:
                    grid[newPos] = False
        for pos, isBlack in grid.items():
            blackNeighbors = sum([1 if value in grid and grid[value] else 0 for value in [addDir(pos, CubeDirections[j]) for j in range(len(CubeDirections))]])

            if isBlack and (blackNeighbors == 0 or blackNeighbors > 2):
                currentGrid[pos] = False
            elif isBlack is False and blackNeighbors == 2:
                currentGrid[pos] = True

        grid = currentGrid
    return grid

results = solve(grid, 100)
print(sum([1 if value else 0 for _, value in results.items()]))