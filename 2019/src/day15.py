from collections import defaultdict, deque
from enum import Enum
from intcode import Intcode

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
            Direction.W: Point(x=1,  y=0),
            Direction.E: Point(x=-1, y=0),
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
    UNKNOWN = 0
    WALL    = 1
    EMPTY   = 2
    OXYGEN  = 3

with open("../input/day15.txt", 'r') as inputFile:
    splitData = inputFile.read().split(",")
    data = [int(x) for x in splitData]

runner = Intcode(verbose=False)
runner.initProgram(data, stallOnOutput=True)
runner.runProgram()
grid = defaultdict(int)

currentPos = Point(0, 0)
currentDir = Direction.N
currentHis = deque([currentPos])
grid[Point.Create(currentPos)] = GridType.EMPTY.value

visited = set()
stack = deque()
stack.appendleft((Point(-1, 0), deque([currentPos])))
stack.appendleft((Point(1, 0), deque([currentPos])))
stack.appendleft((Point(0, -1), deque([currentPos])))
stack.appendleft((Point(0, 1), deque([currentPos])))

finalHist = None

while stack:
    vertex : Point
    history : deque
    vertex, history = stack.popleft()

    #print(f"Visiting {vertex}!")

    if len(currentHis) == 0:
        print()

    if currentPos.getManhattanDist(vertex) > 1 and len(currentHis) > 0:
        moveBack = currentHis.pop()
        assert(moveBack == currentPos)
        while True:
            if len(currentHis) == 0:
                print()
            moveBack = currentHis[-1]
            runner.runProgram(inputStream=[currentPos.getDirToPoint(moveBack).value])
            assert(runner.readOutput and runner.retVal == 1)
            currentPos = moveBack
            runner.runProgram()
            if moveBack in history:
                break
            else:
                currentHis.pop()

    assert(currentPos.getManhattanDist(vertex) <= 1)

    if grid[vertex] == GridType.OXYGEN.value:
        finalHist = deque(currentHis + deque([vertex]))

    if vertex not in visited:
        dir = currentPos.getDirToPoint(vertex)
        assert(runner.needsInput)
        runner.runProgram(inputStream=[dir.value])
        assert(runner.readOutput)

        if runner.retVal == 1 or runner.retVal == 2:
            if runner.retVal == 2:
                grid[Point.Create(vertex)] = GridType.OXYGEN.value
                finalHist = deque(currentHis + deque([vertex]))
            else:
                grid[Point.Create(vertex)] = GridType.EMPTY.value
            currentPos = vertex
            currentHis.append(vertex)
            surroundDir     = [Direction.N, Direction.S, Direction.W, Direction.E]
            undiscoveredPos = [(vertex.move(x), deque(currentHis)) if grid[vertex.move(x)] == GridType.UNKNOWN.value else None for x in surroundDir]
            [stack.appendleft(x) for x in undiscoveredPos if x is not None]
        elif runner.retVal == 0:
            grid[Point.Create(vertex)] = GridType.WALL.value
        visited.add(vertex)
        runner.runProgram()


print("Part1:", len(finalHist) - 1)

# Part 2
minX = min([point.x for point in grid.keys()])
maxX = max([point.x for point in grid.keys()])
minY = min([point.y for point in grid.keys()])
maxY = max([point.y for point in grid.keys()])

def printGrid(minutes: int, grid: defaultdict):
    print(f"Minutes: {minutes}")
    strings = [
        ' ',
        '#',
        '.',
        'O'
    ]
    for y in range(minY, maxY+1):
        for x in range(minX, maxX+1):
            print(strings[grid[Point(x, y)]], end='')
        print()
    print()
    print()

oxyStart = finalHist[-1]
explored = set()
queue    = deque()
queue.append(oxyStart)

minutes  = 0
nextIter = None
while queue:
    node = queue.popleft()
    if node not in explored:
        explored.add(node)

        surroundDir = [Direction.N, Direction.S, Direction.W, Direction.E]
        neighbors = [
            node.move(x) if grid[node.move(x)] == GridType.EMPTY.value else None for x in
            surroundDir]

        if nextIter and nextIter == node and any(neighbors) is False:
            #printGrid(minutes, grid)
            minutes += 1
            nextIter = None

        for neighbor in neighbors:
            if neighbor:
                if nextIter is None or nextIter == node:
                    if nextIter is not None:
                        minutes += 1
                    #print(nextIter)
                    #printGrid(minutes, grid)
                    nextIter = neighbor
                grid[neighbor] = GridType.OXYGEN.value
                queue.append(neighbor)

#printGrid(minutes, grid)
print("Part2", minutes)