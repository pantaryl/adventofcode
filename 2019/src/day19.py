from intcode import Intcode

def memoize(f):
    memo = {}
    def helper(*args):
        if x not in memo:
            memo[tuple(args)] = f(*args)
        return memo[tuple(args)]
    return helper

with open("../input/day19.txt.txt", 'r') as inputFile:
    splitData = inputFile.read().split(",")
    data = [int(x) for x in splitData]

runner = Intcode(verbose=False)
grid = {}
impacted = 0

@memoize
def isImpacted(x: int, y: int):
    if x < 0 or y < 0:
        return 0
    runner = Intcode(verbose=False)
    runner.initProgram(data, inputStream=[x, y], stallOnOutput=True)
    runner.runProgram()
    assert(runner.readOutput)
    return runner.retVal == 1

# Part 1
for x in range(50):
    for y in range(50):
        grid[(x, y)] = isImpacted(x, y)
        impacted += 1 if isImpacted(x, y) else 0
print("Part1:", impacted)

# Part 2
x = 0
y = 0
while True:
    if y >= 99:
        if isImpacted(x + 99, y - 99):
            y = y - 99
            break

    i = 0
    impacted = False
    while True:
        impacted = isImpacted(x + i, y + 1)
        if not impacted and i <= 10:
            i += 1
        else:
            break

    if impacted:
        x += i
    y += 1

print("Part2:", x * 10000 + y)