from collections import defaultdict
import math

with open("../input/day14.txt", 'r') as inputFile:
    data = inputFile.readlines()

reactions = {}
for line in data:
    input, output = line.split("=>")
    materials = input.split(",")

    count, outputType = output.lstrip().rstrip().split(" ")
    count             = int(count)

    reaction = {
        'count': count,
        'input': []
    }

    for material in materials:
        count, type = material.lstrip().rstrip().split(" ")
        count = int(count)
        reaction['input'].append((type, count))

    reactions[outputType] = reaction

def getMultiplier(x, base):
    return math.ceil(x/base)

def reduce(fuelAmount:int, reactions:dict):
    required = {
        'FUEL': fuelAmount
    }

    while any([required[chem] > 0 and chem != "ORE" for chem in required]):
        chem = [chem for chem in required if required[chem] > 0 and chem != "ORE"][0]
        chemCount = required[chem]

        outputCount = reactions[chem]['count']
        multiplier  = math.ceil(chemCount / outputCount)
        required[chem] -= outputCount * multiplier
        for mat, count in reactions[chem]['input']:
            if mat in required:
                required[mat] += count * multiplier
            else:
                required[mat] = count * multiplier
    return required

# Part 1
oreCount = reduce(1, reactions)['ORE']
print('Part1:', oreCount)

# Part 2
oneTril = 1000000000000
fuelMin = (oneTril // oreCount, 0)
fuelMax = (fuelMin[0] + 1, 0)
numIterations = 0
while True:
    numIterations += 1
    fuelMid  = (fuelMin[0] + fuelMax[0]) // 2
    oreCount = reduce(fuelMid, reactions)['ORE']

    if oreCount < oneTril:
        fuelMin = (fuelMid, oreCount)
        fuelMax = (fuelMax[0] * 2, 0)
    else:
        fuelMax = (fuelMid, oreCount)

    if fuelMin[0] == (fuelMax[0] - 1):
        break
print('Part2:', fuelMin[0])