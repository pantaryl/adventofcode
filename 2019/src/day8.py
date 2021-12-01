with open("../input/day8.txt", 'r') as inputFile:
    data = inputFile.read()

layerDims = (25, 6)
numPixelsPerLayer = (layerDims[0] * layerDims[1])
numValues = len(data)
layers    = []
currentIdx = 0

# Part 1:
while currentIdx < numValues:
    layers.append([])
    for x in range(layerDims[0]):
        if currentIdx >= numValues: break
        for y in range(layerDims[1]):
            layers[-1].append(data[currentIdx])
            currentIdx += 1
            if currentIdx >= numValues: break

_, fewestZeros = min([(x.count('0'), x) for x in layers])
answer = fewestZeros.count('1') * fewestZeros.count('2')
print("Part1: ", answer)

# Part 2:
print("Part2:")
finalImage = ['2'] * numPixelsPerLayer
for layer in layers:
    for i in range(len(layer)):
        if finalImage[i] == '2':
            finalImage[i] = layer[i]

for y in range(layerDims[1]):
    for x in range(layerDims[0]):
        value = finalImage[y * layerDims[0] + x]
        print("░" if value == '0' else '▓', end='')
    print()
