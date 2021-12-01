from collections import defaultdict
with open("../input/day1.txt", 'r') as inputFile:
    data = [int(x) for x in inputFile.readlines()]

sums = defaultdict(list)

# Part 1
for first in data:
    for second in data[1:]:
        if first == second: continue
        sums[first+second].append((first, second))

assert(len(sums[2020]) == 2)
print(sums[2020][0][0] * sums[2020][0][1])

# Part 2
for first in data:
    if len(sums[2020 - first]) > 0:
        print(first * sums[2020 - first][0][0] * sums[2020 - first][0][1])
        break