from collections import defaultdict

with open("../input/day8.txt", 'r') as inputFile:
    data = inputFile.readlines()

def runProgram(data):
    visited = set()
    accum   = 0
    pc      = 0
    while True:
        if pc >= len(data):
            return True, accum
        elif pc in visited:
            return False, accum
        visited.add(pc)

        line = data[pc].rstrip()
        instruction, value = line.split(" ")
        value = int(value)

        if instruction == "nop":
            pc += 1
        elif instruction == "acc":
            accum += value
            pc += 1
        elif instruction == "jmp":
            pc += value

# Part 1
print(runProgram(data)[1])

# Part 2
for i in range(0, len(data)):
    if "acc" in data[i]: continue

    newData = list(data)
    if "jmp" in newData[i]:
        newData[i] = newData[i].replace("jmp", "nop")
    else:
        newData[i] = newData[i].replace("nop", "jmp")

    valid, accum = runProgram(newData)
    if valid:
        print(accum)
        break
