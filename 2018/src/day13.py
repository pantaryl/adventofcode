with open("../input/day13.txt.txt", 'r') as inputFile:
    data = inputFile.readlines()

from collections import defaultdict
from enum import Enum

class RailType(Enum):
    HORIZ        = 0
    VERT         = 1
    LEFTUP       = 2
    RIGHTUP      = 3
    INTERSECTION = 4
    EMPTY        = 5

    def __int__(self):
        return self.value

class CartDir(Enum):
    LEFT  = 0
    RIGHT = 1
    UP    = 2
    DOWN  = 3

    def __int__(self):
        return self.value

    def movementVector(self):
        return [(-1, 0), (1, 0), (0, -1), (0, 1)][self.value]

RailTypes = "-|\\/+ "
CartDirTypes = '<>^v'
def determineCarType(char):
    return CartDir(CartDirTypes.index(char))

CartId = 0

class Cart():
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.dir = determineCarType(char)
        self.turnIdx = 0
        global CartId
        self.cartId = CartId + 1
        CartId += 1

    def setNextLoc(self, x, y, newDir, grid):
        grid[self.y][self.x].removeCar(self)
        self.x = x
        self.y = y
        self.dir = newDir
        grid[y][x].addCar(self)

    def determineNextDir(self, currRail):
        if currRail.type == RailType.INTERSECTION:
            if self.dir == CartDir.RIGHT:
                dirs = [ CartDir.UP, CartDir.RIGHT, CartDir.DOWN ]
            elif self.dir == CartDir.LEFT:
                dirs = [ CartDir.DOWN, CartDir.LEFT, CartDir.UP ]
            elif self.dir == CartDir.UP:
                dirs = [ CartDir.LEFT, CartDir.UP, CartDir.RIGHT]
            elif self.dir == CartDir.DOWN:
                dirs = [ CartDir.RIGHT, CartDir.DOWN, CartDir.LEFT]
            turnIdx = self.turnIdx
            self.turnIdx = (self.turnIdx + 1) % 3
            return dirs[turnIdx]
        elif currRail.type == RailType.RIGHTUP:
            if self.dir == CartDir.LEFT:
                return CartDir.DOWN
            elif self.dir == CartDir.RIGHT:
                return CartDir.UP
            elif self.dir == CartDir.DOWN:
                return CartDir.LEFT
            else:
                assert(self.dir == CartDir.UP)
                return CartDir.RIGHT
        elif currRail.type == RailType.LEFTUP:
            if self.dir == CartDir.LEFT:
                return CartDir.UP
            elif self.dir == CartDir.RIGHT:
                return CartDir.DOWN
            elif self.dir == CartDir.DOWN:
                return CartDir.RIGHT
            else:
                assert(self.dir == CartDir.UP)
                return CartDir.LEFT
        else:
            return self.dir

    def move(self, grid):
        moveDir = self.determineNextDir(grid[self.y][self.x])
        vector  = moveDir.movementVector()
        self.setNextLoc(self.x + vector[0], self.y + vector[1], moveDir, grid)

    def __repr__(self):
        return "{:d}, {:d} - {}".format(self.x, self.y, self.dir)

class Rail():
    def __init__(self, x, y, char, cars=None):
        self.x = x
        self.y = y
        self.type = determineRailType(char, cars is not None)
        self.cars = cars if cars else []

    def hasCar(self):
        return len(self.cars) > 0

    def removeCar(self, car):
        self.cars.remove(car)

    def addCar(self, car):
        self.cars.append(car)

    def __repr__(self):
        if len(self.cars) > 1:
            return "X"
        elif len(self.cars) > 0:
            return CartDirTypes[int(self.cars[0].dir)]
        else:
            return RailTypes[int(self.type)]

def determineRailType(char, cart):
    if cart:
        types = [0, 0, 1, 1]
        index = types[CartDirTypes.index(char)]
    else:
        index = RailTypes.index(char) if char in RailTypes else RailType.EMPTY
    return RailType(index)

def init():
    railgrid = defaultdict(dict)
    carts    = []

    for y in range(len(data)):
        line = data[y].rstrip('\n')
        for x in range(len(line)):
            if line[x] in CartDirTypes:
                carts.append(Cart(x, y, line[x]))
                railgrid[y][x] = Rail(x, y, line[x], [carts[-1]])
            else:
                railgrid[y][x] = Rail(x, y, line[x])

    gridX = max([max(railgrid[y].keys()) for y in railgrid]) + 1
    gridY = max(railgrid.keys()) + 1

    for y in range(gridY):
        for x in range(gridX):
            if x not in railgrid[y]:
                railgrid[y][x] = Rail(x, y, ' ')

    return railgrid, carts

def printGrid(grid):
    for y in range(len(grid.keys())):
        for x in range(len(grid[y].keys())):
            print(grid[y][x], end='')
        print()
    print()

def step(grid, carts, needCollision, needRemoval):
    carts.sort(key=lambda x:(x.y, x.x))
    for cart in list(carts):
        if cart not in carts: continue
        cart.move(grid)
        if needCollision and str(grid[cart.y][cart.x]) == 'X':
            return (cart.x, cart.y)
        elif needRemoval and str(grid[cart.y][cart.x]) == 'X':
            for car in list(grid[cart.y][cart.x].cars):
                carts.remove(car)
                grid[cart.y][cart.x].removeCar(car)
    return None

# Part 1
grid, carts = init()
printGrid(grid)
while True:
    collision = step(grid, carts, True, False)
    if collision:
        print("Part1:", collision)
        break

# Part 2
grid, carts = init()
while True:
    stopNext = False
    if len(carts) == 1:
        print("Part2:", (carts[0].x, carts[0].y))
        break
    collision = step(grid, carts, False, True)