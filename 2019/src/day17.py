from collections import defaultdict, deque
from enum import Enum
from intcode import Intcode

with open("../input/day17.txt", 'r') as inputFile:
    splitData = inputFile.read().split(",")
    data = [int(x) for x in splitData]



class Direction(Enum):
    N  = 1
    S  = 2
    W  = 3
    E  = 4

    def getOpposite(self):
        opposite = [
            Direction.S,
            Direction.N,
            Direction.E,
            Direction.W,
        ]
        return opposite[self.value - 1]

    def getNext(self):
        nextVal = [
            Direction.E,
            Direction.W,
            Direction.N,
            Direction.S
        ]
        return nextVal[self.value - 1]

class Point:
    x: int
    y: int

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    @classmethod
    def Create(cls, point):
        return Point(point.x, point.y)

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
            Direction.S: Point(x=0,  y=1),
            Direction.W: Point(x=-1, y=0),
            Direction.E: Point(x=1,  y=0),
        }
        return self + movement[dir]

    def getAllSurroundingPos(self):
        return [self.move(x) for x in (Direction.N, Direction.S, Direction.W, Direction.E)]

    def getDirToPoint(self, other):
        if self.x < other.x:
            return Direction.W
        elif self.x > other.x:
            return Direction.E
        elif self.y < other.y:
            return Direction.S
        else:
            return Direction.N

    def getManhattanDist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

class GridType(Enum):
    UNKNOWN  = 0
    SCAFFOLD = 1
    EMPTY    = 2
    ROBOT    = 3

runner = Intcode(verbose=False)
runner.initProgram(data, stallOnOutput=True)
runner.runProgram()

grid     = {}
startPos = Point(0, 0)

currentX = 0
currentY = 0

while runner.eop is False:
    assert(runner.readOutput)
    output = runner.retVal
    if output == 35:
        grid[Point.Create(startPos)] = GridType.SCAFFOLD.value
        startPos = startPos.move(Direction.E)
    elif output == 46:
        grid[Point.Create(startPos)] = GridType.EMPTY.value
        startPos = startPos.move(Direction.E)
    elif output == 10:
        startPos = Point(0, startPos.y + 1)
    else:
        grid[Point.Create(startPos)] = GridType.ROBOT.value
        startPos = startPos.move(Direction.E)
    runner.runProgram()

minX = min([point.x for point in grid.keys()])
maxX = max([point.x for point in grid.keys()])
minY = min([point.y for point in grid.keys()])
maxY = max([point.y for point in grid.keys()])

def printGrid(grid: defaultdict):
    strings = [
        ' ',
        '#',
        '.',
        'X'
    ]
    for y in range(minY, maxY+1):
        for x in range(minX, maxX+1):
            print(strings[grid[Point(x, y)]], end='')
        print()
    print()
    print()

# Part 1
intersections = set()
pos: Point
type: GridType
for pos, type in grid.items():
    if type == GridType.SCAFFOLD.value or type == GridType.ROBOT.value:
        surrounding = pos.getAllSurroundingPos()
        if all([True if x in grid and (grid[x] == GridType.SCAFFOLD.value or grid[x] == GridType.ROBOT.value) else False for x in surrounding]):
            intersections.add(pos)

print("Part1:", sum([pos.x * pos.y for pos in intersections]))
printGrid(grid)

# Part 2
# NOTE: This is not a generic solver.
part2 = list(data)
part2[0] = 2

A = "L,12,L,10,R,8,L,12\n"
B = "L,10,R,12,R,8\n"
C = "R,8,R,10,R,12\n"
Main = "A,C,A,C,B,B,C,A,C,B\n"

inputStream = [ord(x) for x in Main] + [ord(x) for x in A] + [ord(x) for x in B] + [ord(x) for x in C] + [ord('n'), ord('\n')]
runner.initProgram(program=part2, inputStream=inputStream)
runner.runProgram()
assert(runner.eop)
print("Part2:", runner.retVal)