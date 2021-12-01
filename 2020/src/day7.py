from collections import defaultdict

with open("../input/day7.txt", 'r') as inputFile:
    data = inputFile.readlines()

bagContains    = {}
whatContainsMe = defaultdict(list)

for line in data:
    line = line.rstrip()
    first, second = line.split(" contain ")

    bagId = " ".join(first.split(" ")[:2])

    contains = {}
    types = second.split(", ")
    for type in types:
        split = type.split(" ")
        count = int(split[0]) if split[0] != "no" else 0
        if count > 0:
            subBagId = " ".join(split[1:3])
            contains[subBagId] = count

            whatContainsMe[subBagId].append(bagId)
    bagContains[bagId] = contains

# Part 1
seen  = set()
stack = [ 'shiny gold' ]
count = -1
while len(stack) > 0:
    value  = stack.pop()
    if value in seen: continue
    seen.add(value)
    count += 1

    stack.extend(whatContainsMe[value])

print(count)

# Part 2
stack = [ 'shiny gold' ]
count = -1
while len(stack) > 0:
    value  = stack.pop()
    count += 1

    for bagId, num in bagContains[value].items():
        for i in range(0, num):
            stack.append(bagId)

print(count)