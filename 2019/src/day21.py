from intcode import Intcode
with open("../input/day21.txt", 'r') as inputFile:
    splitData = inputFile.read().split(",")
    data = [int(x) for x in splitData]

runner    = Intcode(verbose=False)
isVerbose = False

def runProgram(springscript: list, labels: str):
    assert(len(springscript) <= 16)

    inputStream = [ord(x) for line in springscript for x in line]
    runner.initProgram(data, stallOnOutput=True)
    runner.runProgram()
    while runner.readOutput:
        if isVerbose: print(chr(runner.retVal), end='')
        runner.runProgram()
    if isVerbose: print("".join(["  " + x for x in springscript]))
    assert(runner.needsInput)
    runner.runProgram(inputStream=inputStream)
    assert(runner.readOutput)
    pos = 0
    x   = 0
    isFloor = False
    while runner.readOutput and not runner.eop:
        if runner.retVal > 127:
            return runner.retVal
        if isVerbose:
            print(chr(runner.retVal), end='')
            if chr(runner.retVal) == '#':
                isFloor = True
            if chr(runner.retVal) == '\n':
                if isFloor:
                    for x in range(17):
                        idx = x - pos + 1
                        if idx >= 0 and idx < len(labels):
                            print(labels[idx], end='')
                        else:
                            print(' ', end='')
                    print()

                x = 0
                isFloor = False
            elif chr(runner.retVal) == '@':
                pos = x
            x += 1

        runner.runProgram()
    return None

springscript = [
    "NOT A T\n",
    "NOT D J\n",
    "AND T J\n",

    "NOT C T\n",
    "AND D T\n",
    "OR T J\n",

    "NOT A T\n",
    "OR T J\n",

    "WALK\n"
]
part1 = runProgram(springscript, labels='RABCD')
assert(part1 is not None)
print("==============================")
print("Part1:", part1)
print("==============================\n")

springscript = [
    "NOT E T\n",
    "NOT H J\n",
    "AND T J\n",
    "NOT J J\n",

    "NOT C T\n",
    "AND T J\n",

    "NOT B T\n",
    "OR T J\n",

    "NOT A T\n",
    "OR T J\n",
    
    "AND D J\n",
    "RUN\n"
]
part2 = runProgram(springscript, labels='RABCDEFGHI')
assert(part2 is not None)
print("==============================")
print("Part2:", part2)
print("==============================\n")