from collections import defaultdict, deque
from copy import deepcopy

with open("../input/day20.txt", 'r') as inputFile:
    data = [x.rstrip('\n') for x in inputFile.readlines()]

def _isPortal(char: str):
    return "A" <= char <= "Z" if char else False

def _isSpace(char: str):
    return char == '.' if char else False

portals = defaultdict(list)
grid = {}
for y in range(len(data)):
    line = data[y]
    x = 0
    while x < len(line):
        char     = line[x]
        teleport = None
        if _isPortal(char):
            left     = line[x-1] if x-1 >= 0 else None
            right    = line[x+1] if x+1 < len(line) else None
            top      = data[y-1][x] if y-1 >= 0 and x < len(data[y-1]) else None
            bottom   = data[y+1][x] if y+1 < len(data) and x < len(data[y+1]) else None
            if _isPortal(right):
                grid[(x, y)] = (' ', None, False)
                portal = ''.join([char, right])
                if _isSpace(left):
                    portals[portal].append((x - 1, y))
                    grid[(x - 1, y)] = ('.', portal, x < len(line) // 2)
                    x += 2
                else:
                    portals[portal].append((x +2, y))
                    grid[(x + 1, y)] = (' ', None, False)
                    grid[(x + 2, y)] = ('.', portal, x > len(line) // 2)
                    x += 3
            elif _isPortal(bottom):
                grid[(x, y)] = (' ', None, False)
                portal = ''.join([char, bottom])
                if _isSpace(top):
                    portals[portal].append((x, y - 1))
                    grid[(x, y - 1)] = ('.', portal, y < len(data) // 2)
                else:
                    portals[portal].append((x, y + 2))
                    grid[(x, y + 1)] = (' ', None, False)
                    grid[(x, y + 2)] = ('.', portal, y > len(data) // 2)
                x += 1
            else:
                grid[(x, y)] = (' ', None, False)
                x += 1
        elif (x, y) not in grid:
            grid[(x, y)] = (char, None, False)
            x += 1
        else:
            x += 1

def memoize(f):
    memo = {}
    def helper(*args):
        if x not in memo:
            memo[tuple(args)] = f(*args)
        return memo[tuple(args)]
    return helper

@memoize
def getImmediateAdj(x, y):
    return [((x + newX, y + newY), 0) for newX, newY in [(-1, 0), (1, 0), (0, -1), (0, 1)] if grid[(x + newX, y + newY)][0] == '.']

def getAdj(x, y, lastPortal, visited, currentLevel, ignoreLevel=False):
    adj = [pos for pos in getImmediateAdj(x, y) if pos[0] not in visited[currentLevel]]
    char, portal, isInner = grid[(x, y)]
    if portal and portal != lastPortal:
        if portal == 'AA' or portal == 'ZZ':
            if ignoreLevel or currentLevel == 0:
                [adj.append((pos, 1 if isInner else -1)) for pos in portals[portal] if pos != (x, y) and pos not in visited[currentLevel]]
        elif portal:
            if ignoreLevel or (isInner and currentLevel < maxLevel) or (isInner is False and currentLevel > 0):
                [adj.append((pos, 1 if isInner else -1)) for pos in portals[portal] if pos != (x, y) and pos not in visited[currentLevel]]
    return adj


assert(len(portals['AA']) == 1)
start = portals['AA'][0]
def dfs(ignoreLevel=False):
    def iterativeFind(ignoreLevel=False):
        finalPaths = []
        stack   = deque([(start, defaultdict(set), deque(), 0, 0)])
        while stack:
            pos, visited, path, currentLevel, lastLevel = stack.pop()
            lastPortal = path[-1][1][1] if path else None
            visited[currentLevel].add(pos)
            path.append((pos, grid[pos], currentLevel))

            if grid[pos][1] == 'ZZ' and currentLevel == 0:
                finalPaths.append(path)
            else:
                adjLocs = getAdj(pos[0], pos[1], lastPortal, visited, currentLevel, ignoreLevel)
                for adj, level in adjLocs:
                    newVisisted = deepcopy(visited)
                    if ignoreLevel is False and level != 0:
                        newVisisted[currentLevel] = set()
                    stack.append((adj, newVisisted, deque(path), currentLevel + level if ignoreLevel is False else 0, currentLevel))

        minPath = min(finalPaths, key=lambda x: len(x))
        return minPath

    path = iterativeFind(ignoreLevel)
    return len(path) - 1

maxLevel = 0
print("Part1:", dfs(ignoreLevel=True))

maxLevel = 20
while True:
    try:
        dist = dfs(ignoreLevel=False)
        print("Part2:", dist, "MaxDepth:", maxLevel)
        break
    except:
        maxLevel += 1

