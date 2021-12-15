from shared import *
import sys, heapq

# Input data is in INPUT_DATA.
# INPUT_DATA = [int(x) for x in INPUT_DATA]
grid = squareGridFromChars(INPUT_DATA, isInts=True)

begin = complex(0, 0)
end   = complex(len(INPUT_DATA[0]) - 1, len(INPUT_DATA) - 1)

# Part 1
def aStar(start, goal, fullGrid):
    def reconstructPath(path, current):
        totalPath = deque([ current ])
        while current in path:
            current = path[current]
            totalPath.appendleft(current)
        return totalPath

    discovered = [(0, OrderedComplex(start))]
    heapq.heapify(discovered)
    path       = {}
    gScore     = defaultdict(lambda: sys.maxsize)
    gScore[start] = 0

    while discovered:
        current = heapq.heappop(discovered)[1]
        if current == goal:
            return reconstructPath(path, current)

        for neighbor in getOrthogonalSquareNeighbors():
            neighborPos = current + neighbor
            if neighborPos in fullGrid:
                tentativeGScore = gScore[current] + fullGrid[neighborPos]
                if tentativeGScore < gScore[neighborPos]:
                    # This path to neighbor is better than any previous one.
                    path[neighborPos] = current
                    gScore[neighborPos] = tentativeGScore
                    priority = (tentativeGScore, OrderedComplex(neighborPos))
                    if priority not in discovered:
                        heapq.heappush(discovered, priority)

    return None

print(sum([grid[x] for x in aStar(begin, end, grid) if x != begin]))

# Part 2
# Got to make our bigger grid
totalGrid = {}
for y in range(0, 5):
    for x in range(0, 5):
        multiplier = y + x
        gridPos = complex(x, y) * (end.real + 1)
        for pos in grid.keys():
            newVal = grid[pos] + multiplier
            newVal = newVal if newVal < 10 else newVal - 9

            newPos = pos + gridPos
            totalGrid[newPos] = newVal

end = complex(len(INPUT_DATA[0]) * 5 - 1, len(INPUT_DATA) * 5 - 1)
print(sum([totalGrid[x] for x in aStar(complex(0, 0), end, totalGrid) if x != complex(0, 0)]))