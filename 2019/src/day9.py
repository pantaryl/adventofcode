from intcode import Intcode

with open("../input/day9.txt", 'r') as inputFile:
    splitData = inputFile.read().split(",")
    data = [int(x) for x in splitData]

data.extend([0] * 100000)

# Part 1
runner = Intcode(verbose=False)
runner.initProgram(list(data), inputStream=[1])
runner.runProgram()
print("Part1:", runner.retVal)

# Part 2
runner.initProgram(list(data), inputStream=[2])
runner.runProgram()
print("Part2:", runner.retVal)