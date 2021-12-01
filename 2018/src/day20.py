with open("../input/day20.txt", 'r') as inputFile:
    data = inputFile.read()

dir = {
    "N": -1j,
    "S":  1j,
    "E":   1,
    "W":  -1
}

grid = { 0: 0 }
distance = 0
loc = 0
stack = []

for char in data[1:-1]:
    if char is '(':
        stack.append((distance, loc))
    elif char is ')':
        distance, loc = stack.pop()
    elif char is '|':
        distance, loc = stack[-1]
    else:
        loc += dir[char]
        distance += 1
        if loc not in grid or distance < grid[loc]:
            grid[loc] = distance

# Part 1
print("Part1:", max(grid.values()))

# Part 2
print("Part2:", sum([1 for x in grid.values() if x >= 1000]))