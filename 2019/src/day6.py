with open("../input/day6.txt", 'r') as inputFile:
    data = inputFile.readlines()

class Object:
    def __init__(self, name: str):
        self.name     = name
        self.parent   = None
        self.children = set()

orbits = { 'COM' : Object('COM') }

# Part 1
for line in data:
    orbiteeName, orbiterName = line.rstrip().lstrip().split(')')

    orbitee, orbiter = None, None
    if orbiteeName in orbits:
        orbitee = orbits[orbiteeName]
    else:
        orbitee = Object(orbiteeName)
        orbits[orbiteeName] = orbitee

    if orbiterName in orbits:
        orbiter = orbits[orbiterName]
    else:
        orbiter = Object(orbiterName)
        orbits[orbiterName] = orbiter

    orbitee.children.add(orbiter)
    orbiter.parent = orbitee

def getPath(obj: Object):
    path = []
    currObj = obj.parent
    while currObj:
        path.append(currObj)
        currObj = currObj.parent
    return path

def determineOrbits(obj: Object):
    return len(getPath((obj)))

print(sum([determineOrbits(x) for _, x in orbits.items()]))

# Part 2
YOU = orbits['YOU']
SAN = orbits['SAN']

youPath = getPath(YOU)
sanPath = getPath(SAN)

similarOrbits = set(youPath).intersection(sanPath)
distance, furthestPoint = max([(determineOrbits(x), x) for x in similarOrbits])

def getDistanceBetweenPoints(start: Object, end: Object):
    count = 0
    while True:
        count += 1
        start  = start.parent
        if start == end:
            break
    return count

YOUORBIT = YOU.parent
SANORBIT = SAN.parent

print(getDistanceBetweenPoints(YOUORBIT, furthestPoint) + getDistanceBetweenPoints(SANORBIT, furthestPoint))