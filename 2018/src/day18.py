with open("../input/day18.txt", 'r') as inputFile:
    data = inputFile.readlines()

def generateInput(data):
    grid = {}
    for y in range(0, len(data)):
        line = data[y].rstrip()
        for x in range(len(line)):
            grid[(x, y)] = line[x]
    return grid

def getSurrounding(point):
    return [(point[0] - 1, point[1] - 1), (point[0], point[1] - 1), (point[0] + 1, point[1] - 1),
            (point[0] - 1, point[1]),                               (point[0] + 1, point[1]),
            (point[0] - 1, point[1] + 1), (point[0], point[1] + 1), (point[0] + 1, point[1] + 1)]

def simulate(numSteps, data):
    period = 0
    grid   = generateInput(data)
    changingScores = []
    scores = []
    for i in range(numSteps):
        nextGrid = grid.copy()
        for point in grid:
            surrounding = [neighbor for neighbor in getSurrounding(point) if neighbor in grid]
            if grid[point] == '.':
                if sum([1 for neighbor in surrounding if grid[neighbor] == '|']) >= 3:
                    nextGrid[point] = '|'
            elif grid[point] == '|':
                if sum([1 for neighbor in surrounding if grid[neighbor] == '#']) >= 3:
                    nextGrid[point] = '#'
            elif grid[point] == '#':
                if sum([1 for neighbor in surrounding if grid[neighbor] == '#']) == 0 or \
                   sum([1 for neighbor in surrounding if grid[neighbor] == '|']) == 0:
                    nextGrid[point] = '.'

        newScore = sum([1 for point in nextGrid if nextGrid[point] == '|']) * sum([1 for point in nextGrid if nextGrid[point] == '#'])
        oldScore = sum([1 for point in grid     if grid[point]     == '|']) * sum([1 for point in grid     if grid[point]     == '#'])
        changingScores.append(newScore - oldScore)
        scores.append(newScore)

        reveredScores = list(reversed(changingScores))[2:]
        if changingScores[-1] in reveredScores and changingScores[-2] in reveredScores and (reveredScores.index(changingScores[-2]) - reveredScores.index(changingScores[-1]) == 1):
            period = reveredScores.index(changingScores[-1]) + 2
            break

        grid = nextGrid
    return grid, i+1, scores[-(period+1):-1]

# Part 1
grid, _, __ = simulate(10, data)
print("Part1:", sum([1 for point in grid if grid[point] == '|']) * sum([1 for point in grid if grid[point] == '#']))

# Part 2
grid, i, scores = simulate(1000000000, data)
iterationsMore = 1000000000 - i
score = scores[iterationsMore % len(scores)]
print("Part2:", score)
