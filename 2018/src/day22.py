import networkx
from collections import defaultdict

with open("../input/day22.txt", 'r') as inputFile:
    data = inputFile.readlines()

class Region():
    def __init__(self, index=0, depth=0):
        self.index = index
        self.depth = depth
        self.erosionLevel = (index + depth) % 20183
        if self.erosionLevel % 3 == 0:
            self.type = '.'
            self.risk = 0
        elif self.erosionLevel % 3 == 1:
            self.type = '='
            self.risk = 1
        else:
            self.type = '|'
            self.risk = 2

for line in data:
    if 'depth' in line:
        depth = int(line.rstrip().split(" ")[1])
    elif 'target' in line:
        target = line.rstrip().split(" ")[1].split(",")
        x = int(target[0])
        y = int(target[1])
        target = x + y*1j

width = int(target.real) * 10

grid = defaultdict(Region)
grid[0] = Region(index=0, depth=depth)

for y in range(depth+1):
    grid[0+y*1j] = Region(y * 48271, depth)
for x in range(width+1):
    grid[x+0j] = Region(x * 16807, depth)

for y in range(1, depth+1):
    for x in range(1, width+1):
        grid[x+y*1j] = Region(grid[(x-1)+y*1j].erosionLevel * grid[x+(y-1)*1j].erosionLevel, depth)

grid[target] = Region(0, depth)

# Part 1
riskLevel = 0
for y in range(0, int(target.imag)+1):
    for x in range(0, int(target.real)+1):
        riskLevel += grid[x+y*1j].risk
print("Part1:", riskLevel)

# Part 2
# Neither  = 0
# Torch    = 1
# Climbing = 2
def dijkstra(grid, edges, target):
    graph = networkx.Graph()
    validItems = [ [1, 2], [0, 2], [0, 1] ]
    for y in range(edges[1]):
        for x in range(edges[0]):
            pos = x+y*1j
            items = validItems[grid[pos].risk]
            graph.add_edge((pos, items[0]), (pos, items[1]), weight=7)
            for dir in [-1+0j, 1+0j, -1j, 1j]:
                newPos = pos+dir
                if newPos in grid:
                    newItems = validItems[grid[newPos].risk]
                    for item in set(items).intersection(set(newItems)):
                        graph.add_edge((pos, item), (newPos, item), weight=1)

    return networkx.dijkstra_path_length(graph, (0, 1), (target, 1))
print("Part2:", dijkstra(grid, (width+1, depth+1), target))