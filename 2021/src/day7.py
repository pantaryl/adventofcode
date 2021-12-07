from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [int(x) for x in INPUT_DATA[0].split(",")]

minPos = min(INPUT_DATA)
maxPos = max(INPUT_DATA)

counts = []

# Part 1
for i in range(minPos, maxPos + 1):
    count = sum([abs(crab - i) for crab in INPUT_DATA])
    counts.append(count)

print(min(counts))

# Part 2
counts = []
for i in range(minPos, maxPos + 1):
    count = sum([(abs(crab - i) * (abs(crab - i) + 1)) // 2 for crab in INPUT_DATA])
    counts.append(count)

print(min(counts))