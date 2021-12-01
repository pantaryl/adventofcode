from typing import NamedTuple
from collections import deque

VERBOSE = False

with open("../input/day15.txt", 'r') as inputFile:
    data = inputFile.readlines()

class Point(NamedTuple('Point', [('x', int), ('y', int)])):
    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    #def __eq__(self, other):
    #    return super.__eq__(other) and isinstance(other, Point) and (self.x == other.x) and (self.y == other.y)

    @property
    def neighbors(self):
        return [self + dir for dir in [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]]

    def readingOrder(self):
        return self.y, self.x

class Unit:
    def __init__(self, type, point, damage):
        self.type = type
        self.point = point
        self.hp   = 200
        self.dmg  = damage

    def pos(self):
        return self.point

    def isAlive(self):
        return self.hp > 0

    def takeDamage(self, damage):
        if self.isAlive(): self.hp -= damage

    def __repr__(self):
        return "{:s} - {:s} {:d}".format(self.type, str(self.point), self.hp)

class Grid(dict):
    def __init__(self, lines, elfPower=3):
        super().__init__()
        self.units = []
        self.elves = []
        self.goblins = []
        global VERBOSE

        for y, line in enumerate(lines):
            line = line.rstrip()
            for x, char in enumerate(line):
                # Points in the grid are true if they are walls.
                self[Point(x, y)] = char == "#"

                if char in 'EG':
                    self.units.append(Unit(char, Point(x, y), elfPower if char == 'E' else 3))
                    if char == 'E':
                        self.elves.append(self.units[-1])
                    elif char == 'G':
                        self.goblins.append(self.units[-1])
                    if VERBOSE: print(self.units[-1])

    def findClosest(self, origUnit, start, targets):
        excludedPoints = set()
        for unit in self.units:
            if unit != origUnit and unit.isAlive():
                excludedPoints.add(unit.pos())
        for point in self:
            if self[point]:
                excludedPoints.add(point)

        if start not in self:
            return [], None

        seen = set()
        queue = deque([(start, 0)])
        foundDist = None
        closest = []

        while queue:
            point, distance = queue.popleft()
            if foundDist and distance > foundDist:
                return closest, foundDist
            if point in seen or point in excludedPoints:
                continue
            seen.add(point)
            if point in targets:
                foundDist = distance
                closest.append(point)
            for neighbor in point.neighbors:
                if neighbor not in seen:
                    queue.append((neighbor, distance + 1))
        return closest, foundDist

    def __repr__(self):
        elves      = [e for e in self.units if e.type == 'E' and e.isAlive()]
        elvesPos   = [e.pos() for e in elves]
        goblins    = [g for g in self.units if g.type == 'G' and g.isAlive()]
        goblinsPos = [g.pos() for g in goblins]
        ordered = sorted(self.keys(), key=lambda x:x.readingOrder())
        line = ''
        units = []
        for i in range(len(ordered)):
            point = ordered[i]
            if i > 0 and point.y > ordered[i-1].y:
                line += '   '
                for unit in units:
                    line += unit.type + "({:d}), ".format(unit.hp)
                line += '\n'
                units = []
            if point in elvesPos:
                units.append(elves[elvesPos.index(point)])
                line += 'E'
            elif point in goblinsPos:
                units.append(goblins[goblinsPos.index(point)])
                line += 'G'
            elif self[point]:
                line += '#'
            else:
                line += '.'
        return line + '\n'



def play(data, noElvesDie, elfPower=3):
    global VERBOSE
    cave = Grid(data, elfPower=elfPower)
    if VERBOSE: print("Round {:d}:\n{:s}".format(0, str(cave)))
    round = 1
    while True:
        orderedUnits = sorted(cave.units, key=lambda x: x.pos().readingOrder())

        for unit in orderedUnits:
            if unit.isAlive() == False: continue

            # Get all of the units on the opposite team.
            enemies = [x for x in cave.units if x.type != unit.type and x.isAlive()]

            # Get all of the cells next to our current unit.
            neighbors = unit.pos().neighbors

            # Determine if any enemies are already in range.
            enemiesInRange = [x for x in enemies if x.pos() in neighbors]

            # If there are no enemies in range, we want to move this unit towards an enemy.
            if len(enemiesInRange) == 0:
                # Determine all of the open spaces next to each enemy.
                surroundingSpaces = []
                for enemy in enemies:
                    surroundingSpaces.extend(enemy.pos().neighbors)
                surroundingSpaces = [space for space in surroundingSpaces if cave[space] == False]

                closestTargets, distance = cave.findClosest(unit, unit.pos(), surroundingSpaces)

                if len(closestTargets) > 0:
                    # Choose the closest by reading order
                    choice = min(closestTargets, key=lambda x: x.readingOrder())

                    for point in sorted(neighbors, key=lambda x: x.readingOrder()):
                        _, nextDist = cave.findClosest(unit, point, [choice])
                        if nextDist == distance - 1:
                            unit.point = point
                            break

                # Update enemies in range if they have changed.
                neighbors = unit.pos().neighbors
                enemiesInRange = [x for x in enemies if x.pos() in neighbors]

            if len(enemiesInRange) > 0:
                # Find the one with the lowest health.
                lowestHealth = min(enemiesInRange, key=lambda x: (x.hp, x.pos().readingOrder()))
                lowestHealth.takeDamage(unit.dmg)

                if noElvesDie and lowestHealth.type == 'E' and not lowestHealth.isAlive():
                    return False, 0, 0

                # Check to see if there is only one unit type left alive.
                alive = set(e.type for e in cave.units if e.isAlive())
                if len(alive) == 1:
                    # Handle edge case when last enemy dies at end of turn
                    if unit == orderedUnits[-1]:
                        round += 1
                    if VERBOSE: print("Round {:d}:\n{:s}".format(round, str(cave)))
                    return True, round-1, sum(e.hp for e in cave.units if e.isAlive())
        if VERBOSE: print("Round {:d}:\n{:s}".format(round, str(cave)))
        round += 1

# Part 1
_, round, hpLeft = play(data, False)
print("Part1:", round * hpLeft)

# Part 2
power = 3
while True:
    noElvesDied, round, hpLeft = play(data, True, power)
    if noElvesDied:
        print("Part2:", round * hpLeft)
        break
    power+=1