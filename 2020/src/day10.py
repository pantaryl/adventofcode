from collections import defaultdict
from helpers import memoize

with open("../input/day10.txt", 'r') as inputFile:
    data = [int(x) for x in inputFile.readlines()]

data = sorted(data)
maxJolt = data[-1] + 3

data.insert(0, 0)
data.append(maxJolt)

# Part 1
one_jolt   = 0
three_jolt = 0

for i in range(1, len(data)):
    jolt_diff = data[i] - data[i-1]
    if jolt_diff == 1:
        one_jolt += 1
    elif jolt_diff == 3:
        three_jolt += 1

print(one_jolt * three_jolt)

# Part 2
@memoize
def getPossibilities(joltIdx: int):
    thisSum = 0

    if joltIdx == len(data) - 1:
        return 1

    for i in range(joltIdx + 1, len(data)):
        if data[i] - data[joltIdx] <= 3:
            newSum   = getPossibilities(i)
            thisSum += newSum
        else:
            break

    return thisSum

part2 = getPossibilities(0)
print(part2)