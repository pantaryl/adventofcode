import sys

with open("../input/day6.txt", 'r') as inputFile:
    data = inputFile.readlines()

class Base():
    def __init__(self, id, string):
        self.id = id

        data = string.rstrip().split(", ")
        self.x = int(data[0])
        self.y = int(data[1])

        self.claims = []

    def __lt__(self, other):
        return len(self.claims) < len(other.claims)

    def addClaim(self, point):
        self.claims.append(point)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.owners = {}

    def appendOwner(self, base):
        distance = self.determineDistance(base)
        if distance not in self.owners:
            self.owners[distance] = []
        self.owners[distance].append(base)

    @staticmethod
    def DetermineDistance(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def determineDistance(self, base):
        return Point.DetermineDistance(self.x, self.y, base.x, base.y)

    def getAbsoluteOwner(self):
        keys = list(self.owners.keys())
        if len(keys) == 1 and len(self.owners[keys[0]]) == 1:
            return self.owners[keys[0]]
        else:
            keys.sort()
            if len(keys) > 1:
                if len(self.owners[keys[0]]) == 1:
                    return self.owners[keys[0]][0]

        return None

id = 0
bases = []

minX, minY, maxX, maxY = sys.maxsize, sys.maxsize, 0, 0

for line in data:
    newBase = Base(id, line)
    bases.append(newBase)

    minX = min(minX, newBase.x)
    maxX = max(maxX, newBase.x)
    minY = min(minY, newBase.y)
    maxY = max(maxY, newBase.y)

# Part 1
qualifiedBases = list(bases)
points = {}
for x in range(minX, maxX+1):
    for y in range(minY, maxY+1):
        newPoint = Point(x, y)
        for base in bases:
            newPoint.appendOwner(base)

        keys = list(newPoint.owners.keys())
        if (x == minX or x == maxX or y == minY or y == maxY):
            disqualified = newPoint.getAbsoluteOwner()
            if disqualified and disqualified in qualifiedBases:
                qualifiedBases.remove(disqualified)

        owner = newPoint.getAbsoluteOwner()
        if owner:
            owner.addClaim(newPoint)
        points[(x, y)] = newPoint

qualifiedBases = [x for x in qualifiedBases if len(x.claims) > 0]
qualifiedBases.sort(reverse=True)
print(len(qualifiedBases[0].claims))

# Part 2
maxDistance = 10000

points = []
for x in range(minX, maxX+1):
    for y in range(minY, maxY+1):
        totalDistance = 0
        for base in bases:
            totalDistance += Point.DetermineDistance(x, y, base.x, base.y)
        if totalDistance < maxDistance:
            points.append(1)

print(sum(points))