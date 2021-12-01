from collections import defaultdict
from enum import Enum
from typing import NamedTuple
import math

class Direction(Enum):
    N  = 0
    NE = 1
    E  = 2
    SE = 3
    S  = 4
    SW = 5
    W  = 6
    NW = 7

    def __lt__(self, other):
        return self.value < other.value

    @classmethod
    def getDirection(cls, x, y):
        if x == 0:
            if y > 0:
                return Direction.S
            else:
                return Direction.N
        elif y == 0:
            if x > 0:
                return Direction.E
            else:
                return Direction.W
        elif x > 0:
            if y > 0:
                return Direction.SE
            else:
                return Direction.NE
        elif x < 0:
            if y > 0:
                return Direction.SW
            else:
                return Direction.NW

class Point(NamedTuple):
    x: int
    y: int
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
class Slope(NamedTuple):
    eq:  str
    dir: Direction
    m: int
    def __eq__(self, other):
        return self.eq == other.eq and self.dir == other.dir and self.m == other.m

def calcManhattanDist(loc: Point, other: Point):
    return abs(loc.x - other.x) + abs(loc.y - other.y)

with open("../input/day10.txt", 'r') as inputFile:
    data = inputFile.readlines()

def genGrid(data: list):
    grid = {}
    for y in range(len(data)):
        line = data[y]
        for x in range(len(line)):
            if line[x] == '#':
                grid[Point(x=x, y=y)] = line[x]

    return grid

def getCounts(grid: dict) -> tuple:
    counts = {}
    seen   = defaultdict(dict)
    for pos, type in grid.items():
        seen[pos] = defaultdict(list)
        for otherPos, otherType in grid.items():
            if pos == otherPos:
                continue

            dx = otherPos.x - pos.x
            dy = otherPos.y - pos.y
            if dx == 0:
                eq = f'x = {otherPos.x}',
                m  = math.inf
            elif dy == 0:
                eq = f'y = {otherPos.y}'
                m  = otherPos.y
            else:
                m   = dy / dx
                b   = pos.y - (m * pos.x)
                eq = f'y = {m}x + {b}'
            dir = Direction.getDirection(x=(otherPos.x - pos.x), y=(otherPos.y - pos.y))
            slope = Slope(eq=eq, dir=dir, m=m)
            seen[pos][slope] = sorted(seen[pos][slope] + [ otherPos ], key=lambda x: calcManhattanDist(pos, x))
        counts[pos] = len(seen[pos].keys())
    return (max([(x, pos, seen[pos]) for pos, x in counts.items()]))

# Part 1
part1 = genGrid(data)
count, pos, seen = getCounts(part1)
print("Part1:", (count, pos))

# Part 2
slopes = sorted(seen.keys(), key=lambda x:(x.dir, x.m))
idx = 1
result = None
while True:
    if len(slopes) == 0:
        break
    tempSlopes = list(slopes)
    for slope in tempSlopes:
        pos = seen[slope].pop(0)
        if idx == 200:
            result = (idx, pos)
        # print(idx, pos)
        idx += 1
        if len(seen[slope]) == 0:
            slopes.remove(slope)
print("Part2:", result)