######################################################################################
# It's important to note how much faster this runs when you use basic types, such as #
# List[List[str]] instead of Dict[int][int] = str, and tuple(int, int) instead of a  #
# custom class Point(x, y). Similarly, the concept of memoization should be          #
# remembered for the future, as it is extremely helpful in these situations!         #
# PyPy runs this faster than CPython, something else to consider!                    #
######################################################################################

from collections import deque

with open("../input/day18.txt", 'r') as inputFile:
    data = [x.rstrip() for x in inputFile.readlines()]

def _isKey(value: str): return 'a' <= value <= 'z'
def _isDoor(value: str): return 'A' <= value <= 'Z'
def _isWall(value: str): return value == '#'

def getGridAndBots(data: list):
    # Return a list[list[str]] for the grid,
    # and a list[tuple(int, int)] for the bots.
    grid = data
    bots = []
    for y, line in enumerate(grid):
        for x, line in enumerate(grid[y]):
            value = data[y][x]
            if value == '@':
                bots.append((y, x))
                value = '.'
            grid[y][x] = value
    return grid, bots

def reachableKeys(bots: list, grid: list, inventory: set):
    # Returns a dictionary containing all of the reachable keys by the current list of bots.
    reachable = {}
    for id, botPos in enumerate(bots):
        queue   = deque([ (botPos, 0) ])
        visited = set()

        while queue:
            currentPos, dist = queue.popleft()
            tile             = grid[currentPos[0]][currentPos[1]]

            if currentPos in visited: continue
            visited.add(currentPos)

            # If we've found one of the keys, we don't need to go any further on from this key.
            if _isKey(tile) and tile not in inventory:
                reachable[tile] = (currentPos, dist, id)
                continue

            # We can, however, keep looking if we haven't yet found a key.
            for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                newPos  = (currentPos[0] + direction[0], currentPos[1] + direction[1])
                newTile = grid[newPos[0]][newPos[1]]

                if _isWall(newTile) is False and (_isDoor(newTile) is False or newTile.lower() in inventory):
                    queue.append((newPos, dist + 1))
    return reachable

def distanceToAllKeys(grid: list, bots: list):
    # Memoization: https://en.wikipedia.org/wiki/Memoization
    # Cache the bots positions and the inventory at those positions so we can quickly
    # return for cases we've already seen.
    memo = {}
    def exploreRecursive(bots: list, inventory: set):
        #print(inventory)
        memoKey = (tuple(sorted(bots)), tuple(sorted(inventory)))
        if memoKey in memo:
            return memo[memoKey]

        distances = []
        for key, (pos, dist, id) in reachableKeys(bots, grid, inventory).items():
            # We need a new list of bots here because the recursive function will modify it.
            # Same with the inventory.
            newBots     = list(bots)
            newBots[id] = pos
            newInventory = set(inventory) | set(key)
            distances.append(dist + exploreRecursive(newBots, newInventory))
        minDistance = min(distances) if distances else 0
        memo[memoKey] = minDistance
        return minDistance
    minDistance = exploreRecursive(bots, set())
    return minDistance

# Part 1
data = [list(line) for line in data]
part1Grid, part1Bots = getGridAndBots(data)
assert(len(part1Bots) == 1)
origBot = part1Bots[0]
minDistance = distanceToAllKeys(part1Grid, part1Bots)
print("Part1:", minDistance)

# Part 2
# Mangle our input file data to replace the singular original bot (origBot)
# with four new ones, and some walls to separate them.
for direction in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
    newPos = (origBot[0] + direction[0], origBot[1] + direction[1])
    data[newPos[0]][newPos[1]] = '#'
for direction in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
    newPos = (origBot[0] + direction[0], origBot[1] + direction[1])
    data[newPos[0]][newPos[1]] = '@'
part2Grid, part2Bots = getGridAndBots(data)
minDistance = distanceToAllKeys(part2Grid, part2Bots)
print("Part2:", minDistance)
