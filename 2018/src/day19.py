with open("../input/day19.txt.txt", 'r') as inputFile:
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
    "addr" : addr,
    "addi" : addi,
    "mulr" : mulr,
    "muli" : muli,
    "banr" : banr,
    "bani" : bani,
    "borr" : borr,
    "bori" : bori,
    "setr" : setr,
    "seti" : seti,
    "gtir" : gtir,
    "gtri" : gtri,
    "gtrr" : gtrr,
    "eqir" : eqir,
    "eqri" : eqri,
    "eqrr" : eqrr,
}

def runProgram(program, registers, breakOnBackJump=False):
    while registers[ip] >= 0 and registers[ip] < len(program):
        lineNum = registers[ip]
        values  = program[lineNum]
        oldIpLoc = registers[ip]
        opcodes[values[0]](values[1], values[2], values[3], registers)
        registers[ip] += 1
        if breakOnBackJump and registers[ip] <= oldIpLoc: break

# Part 1
registers = [0, 0, 0, 0, 0, 0]
runProgram(program, registers)
print("Part1:", registers[0])

# Part 2
registers = [1, 0, 0, 0, 0, 0]
runProgram(program, registers, breakOnBackJump=True)

finalNumber = max(registers)
factors = 0
for i in range(1, finalNumber+ 1):
    if finalNumber % i == 0:
        factors += i
print("Part2:", factors)