with open("../input/day16.txt", 'r') as inputFile:
    data = [int(x) for x in inputFile.read()]

phaseLen = len(data)

def getDigit(number: int, index: int):
    return number // 10**index % 10

def getPhasePattern(currentIdx: int, startIdx: int):
    indexInPattern = ((currentIdx + 1) % (4 * (startIdx + 1))) // (startIdx + 1)
    return [0, 1, 0, -1][indexInPattern]

def runPhaseIndex(data: list, dataLen: int, startIdx: int):
    digit = getDigit(abs(sum(map(lambda x: data[x] * getPhasePattern(x, startIdx), range(dataLen)))), 0)
    return digit

def runPhases(data: list, numPhases: int):
    tempData  = data
    dataLen   = len(tempData)
    for i in range(numPhases):
        tempData  = list(map(lambda x: runPhaseIndex(tempData, dataLen, x), range(dataLen)))
    return tempData

part1 = runPhases(data, 100)
print("Part1:", "".join([str(x) for x in part1[:8]]))

# Part 2:
def runPhasesQuick(data: list, numPhases: int):
    dataLen = len(data)
    newData = [0] * dataLen
    for i in range(numPhases):
        newData[dataLen - 1] = data[dataLen - 1]
        for idx in range(dataLen - 2, dataLen // 2, -1):
            result = data[idx] + newData[idx + 1]
            newData[idx] = result % 10
        data = newData
        newData = [0] * dataLen
    return data

part2 = data * 10000
part2 = runPhasesQuick(part2, 100)
offset = int("".join([str(x) for x in data[:7]]))
print("Part2:", "".join([str(x) for x in part2[offset:offset+8]]))