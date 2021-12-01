with open("../input/day1.txt", 'r') as inputFile:
    data = inputFile.readlines()

# Part 1
value = 0
for item in data:
    value += int(item)
print(value)

# Part 2
value = 0
seenValues = { 0: None, }
needsBreak = False
while needsBreak is False:
    for item in data:
        value += int(item)
        if value in seenValues:
            needsBreak = True
            break
        seenValues[value] = None

print(value)