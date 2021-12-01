with open("../input/day25.txt", 'r') as inputFile:
    data = inputFile.readlines()

class Point():
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def distFrom(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y) + abs(other.z - self.z) + abs(other.w - self.w)

    def __repr__(self):
        return "({},{},{},{})".format(self.x, self.y, self.z, self.w)

def generateInput():
    coords = []
    for line in data:
        values = line.split(",")
        coords.append(Point(int(values[0]), int(values[1]), int(values[2]), int(values[3])))
    return coords
# Part 1
from collections import deque
part1 = generateInput()
numConstellations = 0
allPointsSeen = set()

while True:
    seen = set()
    stillLeft = deque()
    for point in part1:
        if point not in allPointsSeen:
            stillLeft.append(point)
            break

    while stillLeft:
        point = stillLeft.popleft()
        seen.add(point)
        allPointsSeen.add(point)
        for otherPoint in part1:
            if otherPoint not in allPointsSeen and otherPoint not in seen:
                if point.distFrom(otherPoint) <= 3:
                    stillLeft.append(otherPoint)

    if not seen:
        break
    numConstellations += 1

print("Part1:", numConstellations)