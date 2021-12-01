from intcode import Intcode

with open("../input/day2.txt", 'r') as inputFile:
    data = [int(x) for x in inputFile.read().split(",")]

def setInputs(program:list,
              noun: int,
              verb: int):
    program[1] = noun
    program[2] = verb

# Part 1
part1 = list(data)
setInputs(part1, 12, 2)
runner = Intcode()
runner.initProgram(part1)
print("Part1:", runner.runProgram())

# Part 2
answer = 0
nounPoss = list(range(0, 100))
verbPoss = list(range(0, 100))
shouldBreak = False
for noun in nounPoss:
    for verb in verbPoss:
        part2 = list(data)
        setInputs(part2, noun, verb)
        runner.initProgram(part2)
        ret = runner.runProgram()
        if ret == 19690720:
            answer = (100*noun) + verb
            print("Part2:", answer)
            shouldBreak = True
            break
    if shouldBreak:
        break