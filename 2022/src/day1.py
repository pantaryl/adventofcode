from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [int(x) if x else -1 for x in INPUT_DATA]

# Part 1
elves = []
currentSum = 0
for data in INPUT_DATA:
    if data == -1:
        elves.append(currentSum)
        currentSum = 0
        continue
    currentSum += data

elves.append(currentSum)

print(max(elves))

# Part 2
elves.sort(reverse=True)
print(sum(elves[:3]))