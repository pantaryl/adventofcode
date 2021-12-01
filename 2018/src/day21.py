with open("../input/day21.txt", 'r') as inputFile:
    data = inputFile.readlines()

ip = 0
program = []
for line in data:
    if '#' in line:
        ip = int(line.split(" ")[1])
    else:
        values = line.rstrip().split(" ")
        program.append([values[0], int(values[1]), int(values[2]), int(values[3])])

def addr(a, b, c, registers): registers[c] = registers[a] + registers[b]
def addi(a, b, c, registers): registers[c] = registers[a] + b
def mulr(a, b, c, registers): registers[c] = registers[a] * registers[b]
def muli(a, b, c, registers): registers[c] = registers[a] * b
def banr(a, b, c, registers): registers[c] = registers[a] & registers[b]
def bani(a, b, c, registers): registers[c] = registers[a] & b
def borr(a, b, c, registers): registers[c] = registers[a] | registers[b]
def bori(a, b, c, registers): registers[c] = registers[a] | b
def setr(a, b, c, registers): registers[c] = registers[a]
def seti(a, b, c, registers): registers[c] = a
def gtir(a, b, c, registers): registers[c] = 1 if a > registers[b] else 0
def gtri(a, b, c, registers): registers[c] = 1 if registers[a] > b else 0
def gtrr(a, b, c, registers): registers[c] = 1 if registers[a] > registers[b] else 0
def eqir(a, b, c, registers): registers[c] = 1 if a == registers[b] else 0
def eqri(a, b, c, registers): registers[c] = 1 if registers[a] == b else 0
def eqrr(a, b, c, registers): registers[c] = 1 if registers[a] == registers[b] else 0

opcodes = {
    "addr" : { 'func': addr, 'rA' : True,  'rB' : True,  },
    "addi" : { 'func': addi, 'rA' : True,  'rB' : False, },
    "mulr" : { 'func': mulr, 'rA' : True,  'rB' : True,  },
    "muli" : { 'func': muli, 'rA' : True,  'rB' : False, },
    "banr" : { 'func': banr, 'rA' : True,  'rB' : True,  },
    "bani" : { 'func': bani, 'rA' : True,  'rB' : False, },
    "borr" : { 'func': borr, 'rA' : True,  'rB' : True,  },
    "bori" : { 'func': bori, 'rA' : True,  'rB' : False, },
    "setr" : { 'func': setr, 'rA' : True,  'rB' : False, },
    "seti" : { 'func': seti, 'rA' : False, 'rB' : False, },
    "gtir" : { 'func': gtir, 'rA' : False, 'rB' : True,  },
    "gtri" : { 'func': gtri, 'rA' : True,  'rB' : False, },
    "gtrr" : { 'func': gtrr, 'rA' : True,  'rB' : True,  },
    "eqir" : { 'func': eqir, 'rA' : False, 'rB' : True,  },
    "eqri" : { 'func': eqri, 'rA' : True,  'rB' : False, },
    "eqrr" : { 'func': eqrr, 'rA' : True,  'rB' : True,  },
}

importantLine = None
for i in range(len(program)):
    instruction = program[i]
    if (instruction[1] == 0 and opcodes[instruction[0]]['rA'] == True) or \
       (instruction[2] == 0 and opcodes[instruction[0]]['rB'] == True):
        importantLine = i
        break

importantReg = instruction[2] if instruction[1] == 0 else instruction[1]

def runProgram(program, registers, isPart1=False):
    seenValues = []
    while registers[ip] >= 0 and registers[ip] < len(program):
        lineNum = registers[ip]
        values  = program[lineNum]

        if registers[ip] == importantLine:
            if isPart1:
                return values, registers[importantReg]
            else:
                if registers[importantReg] in seenValues:
                    return values, seenValues[-1]
                seenValues.append(registers[importantReg])
        opcodes[values[0]]['func'](values[1], values[2], values[3], registers)
        registers[ip] += 1

# Part 1
registers = [0, 0, 0, 0, 0, 0]
_, value = runProgram(program, registers, True)
print("Part1:", value)

# Part 2
registers = [0, 0, 0, 0, 0, 0]
_, value = runProgram(program, registers, False)
print("Part2:", value)
