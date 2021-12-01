from intcode import Intcode
from collections import defaultdict, namedtuple
from typing import NamedTuple
from enum import Enum

class Direction(Enum):
    N  = 0
    E  = 1
    S  = 2
    W  = 3

    def getNextDir(self, rotation: int):
        left90  = 0
        right90 = 1

        if left90 == rotation:
            if self == Direction.N:
                return Direction.E
            elif self == Direction.E:
                return Direction.S
            elif self == Direction.S:
                return Direction.W
            elif self == Direction.W:
                return Direction.N
        else:
            assert(right90 == rotation)
            if self == Direction.N:
                return Direction.W
            elif self == Direction.W:
                return Direction.S
            elif self == Direction.S:
                return Direction.E
            elif self == Direction.E:
                return Direction.N

class Point():
    x: int
    y: int

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(x=(self.x+other.x), y=(self.y+other.y))

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def move(self, dir: Direction):
        movement = {
            Direction.N: Point(x=0,  y=-1),
            Direction.E: Point(x=-1, y=0),
            Direction.S: Point(x=0,  y=1),
            Direction.W: Point(x=1,  y=0)
        }
        return self + movement[dir]

with open("../input/day11.txt", 'r') as inputFile:
    splitData = inputFile.read().split(",")
    data = [int(x) for x in splitData]


class Panel():
    type: int
    count: int

    def __init__(self, type=0):
        self.type = type
        self.count = 0

    def __repr__(self):
        return f"Panel(type={self.type}, count={self.count})"

def paint(data: list, grid: defaultdict):
    runner = Intcode(verbose=False)

    currentPos = Point(x=0, y=0)
    currentDir = Direction.N
    runner.initProgram(list(data), stallOnOutput=True)
    runner.runProgram()
    while runner.eop is False:
        if runner.needsInput:
            runner.runProgram(inputStream=[grid[currentPos].type])

        paint = None
        dir   = None
        if runner.readOutput:
            paint = runner.retVal
            runner.runProgram()
        if runner.readOutput:
            dir = runner.retVal
            runner.runProgram()

        grid[currentPos].type   = paint
        grid[currentPos].count += 1
        currentDir = currentDir.getNextDir(dir)
        currentPos = currentPos.move(currentDir)

# Part 1
grid = defaultdict(Panel)
paint(data, grid)
print("Part1:", sum([1 if x.count > 0 else 0 for _, x in grid.items()]))

# Part 2
grid = defaultdict(Panel)
grid[Point(0, 0)] = Panel(type=1)
paint(data, grid)

minX = min([point.x for point in grid.keys()])
maxX = max([point.x for point in grid.keys()])
minY = min([point.y for point in grid.keys()])
maxY = max([point.y for point in grid.keys()])

print("Part2:")
for y in range(minY, maxY+1):
    for x in range(minX, maxX+1):
        value = grid[Point(x, y)].type
        print("░" if value == 0 else '▓', end='')
    print()