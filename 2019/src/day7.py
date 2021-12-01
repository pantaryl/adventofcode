from intcode import Intcode
from itertools import permutations

with open("../input/day7.txt", 'r') as inputFile:
    data = [int(x) for x in inputFile.read().split(",")]

runners      = [ Intcode(), Intcode(), Intcode(), Intcode(), Intcode() ]
combinations = permutations([0, 1, 2, 3, 4])
prevOutput   = 0
maxOutput    = 0

# Part1
for combination in combinations:
    for i in range(len(runners)):
        runners[i].initProgram(list(data), inputStream=[combination[i]])
        
    prevOutput = 0
    for i in range(len(runners)):
        prevOutput = runners[i].runProgram(inputStream=[prevOutput])
    maxOutput = max(maxOutput, prevOutput)
print("Part1:", maxOutput)

# Part2
combinations = permutations([5, 6, 7, 8, 9])
maxOutput    = 0
for combination in combinations:
    for i in range(len(runners)):
        runners[i].initProgram(list(data), inputStream=[combination[i]])

    runners[4].retVal = 0
    while runners[4].eop is False:
        runners[0].runProgram(inputStream=[runners[4].retVal])
        runners[1].runProgram(inputStream=[runners[0].retVal])
        runners[2].runProgram(inputStream=[runners[1].retVal])
        runners[3].runProgram(inputStream=[runners[2].retVal])
        runners[4].runProgram(inputStream=[runners[3].retVal])
    maxOutput = max(maxOutput, runners[4].retVal)
print("Part2:", maxOutput)