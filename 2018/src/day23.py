import re

with open("../input/day23.txt", 'r') as inputFile:
    data = inputFile.readlines()

class Point():
    def __init__(self, x, y, z, radius=0):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y, self.z+other.z)

    def __mul__(self, other):
        assert(isinstance(other, int))
        return Point(self.x*other, self.y*other, self.z*other)

    def __repr__(self):
        return "(<{},{},{}> - {})".format(self.x, self.y, self.z, self.radius)

nanobots = []
for line in data:
    values = re.findall(r'(-?\d+)', line)
    nanobots.append(Point(int(values[0]), int(values[1]), int(values[2]), int(values[3])))

sortedList = sorted(nanobots, key=lambda x: x.radius)
strongestNanobot = sortedList[-1]

# Part 1
def pointInSphere(center, point):
    return (abs(center.x - point.x) + abs(center.y - point.y) + abs(center.z - point.z)) <= center.radius

numInRange = 0
for bot in sortedList:
    if pointInSphere(strongestNanobot, bot): numInRange += 1
print("Part1:", numInRange)

# Part 2
def inRange(pos, bots):
    return sum([1 if pointInSphere(bot, pos) else 0 for bot in bots])

MovementDir = \
[
    Point(0, 0, -1),
    Point(0, -1, 0),
    Point(-1, 0, 0),
    Point(0, 0, 1),
    Point(0, 1, 0),
    Point(1, 0, 0),
]
currentPos     = Point(0, 0, 0)
numBotsInRange = inRange(currentPos, nanobots)
currentDir     = 1

loopCnt   = 0
currScale = 1
swapCnt   = 0

while loopCnt < 15000:
    nextPos = currentPos + MovementDir[currentDir]*currScale
    nextBotsInRange = inRange(nextPos, nanobots)
    if nextBotsInRange < numBotsInRange:
        if currScale == 1:
            currentDir = (currentDir+1) % len(MovementDir)
            swapCnt += 1
            if swapCnt > 15:
                break
        else:
            currScale //= 2
            swapCnt = 0
    else:
        currentPos = nextPos
        numBotsInRange = nextBotsInRange
        currScale *= 2
        swapCnt = 0
    loopCnt += 1
print("Part2:", "NumBots:", numBotsInRange, "CurrentPos:", currentPos, "Score:", abs(currentPos.x)+abs(currentPos.y)+abs(currentPos.z))