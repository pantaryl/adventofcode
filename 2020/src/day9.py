from collections import defaultdict

with open("../input/day9.txt", 'r') as inputFile:
    data = [int(x) for x in inputFile.readlines()]

def calculateAllSums(data):
    sums = set()
    assert(len(data) == 25)
    for i in range(len(data)):
        for j in range(1, len(data)):
            if i == j: continue
            sums.add(data[i] + data[j])

    return sums

# Part 1
maxIndex = 0
for i in range(25, len(data)):
    sums = calculateAllSums(data[i-25:i])
    if data[i] not in sums:
        maxIndex = i
        print(data[i])
        break

# Part 2
currentStart = 0
while True:
    sum = 0
    for i in range(currentStart, maxIndex):
        sum += data[i]
        if sum == data[maxIndex]:
            print(data[currentStart] + data[i])
            break
        elif sum >= data[maxIndex]:
            break
    if sum == data[maxIndex]: break
    currentStart += 1