from intcode import Intcode

with open("../input/day5.txt", 'r') as inputFile:
    data = [int(x) for x in inputFile.read().split(",")]

runner = Intcode(verbose=False)

# Part1
runner.initProgram(list(data), inputStream=[1])
print("Part1:", runner.runProgram())

# Part2
runner.initProgram(list(data), inputStream=[5])
print("Part2:", runner.runProgram(list(data)))