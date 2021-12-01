with open("../input/day3.txt", 'r') as inputFile:
    data = inputFile.readlines()

def determineCount(slope):
    pos   = (0, 0)
    treeCount = 0
    while pos[1] < len(data):
        if pos != (0, 0):
            line = data[pos[1]].rstrip()
            char = line[pos[0] % len(line)]
            if char == "#":
                treeCount += 1
        pos = (pos[0] + slope[0], pos[1] + slope[1])
    return treeCount

# Part 1
print(determineCount((3, 1)))

# Part 2
counts = [
    determineCount((1, 1)),
    determineCount((3, 1)),
    determineCount((5, 1)),
    determineCount((7, 1)),
    determineCount((1, 2))
]

part2 = 1
for count in counts:
    part2 *= count
print(part2)