from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x.split('-') for x in INPUT_DATA]

def isSmallCave(cave: str):
    return cave.lower() == cave

small = set()
cave = defaultdict(set)
# Part 1
for line in INPUT_DATA:
    start, end = line
    cave[start].add(end)
    cave[end].add(start)

    if isSmallCave(start):
        small.add(start)
    if isSmallCave(end):
        small.add(end)

def solve(currentPath: list, paths: list, part2 = False) -> list:
    neighbors = list(cave[currentPath[-1]])
    for neighbor in neighbors:
        if neighbor == "end":
            paths.append(currentPath + [neighbor])
        elif neighbor == 'start':
            pass
        elif neighbor not in currentPath or isSmallCave(neighbor) == False:
            solve(currentPath + [neighbor], paths, part2=part2)
        elif part2 and isSmallCave(neighbor):
            if all([True if currentPath.count(x) <= 1 else False for x in list(small)]):
                # No current duplicate rooms, let's try one.
                solve(currentPath + [neighbor], paths, part2=part2)

    return paths

paths = solve(['start'], [])
print(len(paths))

# Part 2
paths = solve(['start'], [], part2=True)
print(len(paths))