with open("../input/day16.txt", 'r') as inputFile:
    data = inputFile.read().split("\n\n\n")
    data[0] = data[0].splitlines()
    data[1] = data[1].splitlines()

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
    "addr" : { 'func': addr, 'opNum': None },
    "addi" : { 'func': addi, 'opNum': None },
    "mulr" : { 'func': mulr, 'opNum': None },
    "muli" : { 'func': muli, 'opNum': None },
    "banr" : { 'func': banr, 'opNum': None },
    "bani" : { 'func': bani, 'opNum': None },
    "borr" : { 'func': borr, 'opNum': None },
    "bori" : { 'func': bori, 'opNum': None },
    "setr" : { 'func': setr, 'opNum': None },
    "seti" : { 'func': seti, 'opNum': None },
    "gtir" : { 'func': gtir, 'opNum': None },
    "gtri" : { 'func': gtri, 'opNum': None },
    "gtrr" : { 'func': gtrr, 'opNum': None },
    "eqir" : { 'func': eqir, 'opNum': None },
    "eqri" : { 'func': eqri, 'opNum': None },
    "eqrr" : { 'func': eqrr, 'opNum': None },
}

def registersToList(line):
    return [int(x) for x in line.split(": ")[1].replace("[", '').replace("]", '').split(",")]

def opFromLine(line):
    op, a, b, c = [int(x) for x in line.split(" ")]
    return op, a, b, c

# Part 1
numThreeOrMore = 0
for i in range(len(data[0])):
    myLine = data[0][i].rstrip()
    if 'Before' in myLine:
        beforeRegisters = registersToList(myLine)
        op, a, b, c     = opFromLine(data[0][i+1].rstrip())
        afterRegisters  = registersToList(data[0][i+2].rstrip())

        successfulOps = []
        for opName, func in opcodes.items():
            origSet = beforeRegisters.copy()
            func['func'](a, b, c, origSet)
            if origSet == afterRegisters: successfulOps.append(opName)
        if len(successfulOps) >= 3: numThreeOrMore += 1
        i += 2

print("Part1:", numThreeOrMore)

# Part 2
opcodesByNum = {}
while True:
    i = 0
    while i < len(data[0]):
        myLine = data[0][i].rstrip()
        if 'Before' in myLine:
            beforeRegisters = registersToList(myLine)
            op, a, b, c     = opFromLine(data[0][i+1].rstrip())
            afterRegisters  = registersToList(data[0][i+2].rstrip())

            successfulOps = []
            for opName, func in opcodes.items():
                if func['opNum'] is not None: continue
                origSet = beforeRegisters.copy()
                func['func'](a, b, c, origSet)
                if origSet == afterRegisters: successfulOps.append(opName)
            if len(successfulOps) == 1:
                opcodes[successfulOps[0]]['opNum'] = op
                opcodesByNum[op] = opcodes[successfulOps[0]]
            i += 4
        else: break

    if len(opcodesByNum.keys()) == len(opcodes.keys()): break

registers = [0, 0, 0, 0]
i = 0
while i < len(data[1]):
    myLine = data[1][i].rstrip()
    if '' != myLine:
        op, a, b, c = opFromLine(myLine)
        opcodesByNum[op]['func'](a, b, c, registers)
    i += 1
print("Part2:", registers[0])