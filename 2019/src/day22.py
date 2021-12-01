from collections import deque

with open("../input/day22.txt", 'r') as inputFile:
    data = [x.rstrip() for x in inputFile.readlines()]

verbose = False

def dealIntoNewStack(cards: deque):
    cards.reverse()
    if verbose: print(f"deal into new stack: {cards}")
    return cards

def cutNCards(cards: deque, n: int):
    cards.rotate(-n)
    if verbose: print(f"cut {n}: {cards}")
    return cards

def dealIncrementN(cards: deque, n: int):
    newCards = deque(cards)
    origLength = len(cards)
    for i in range(origLength):
        newCards.popleft()
        newCards.appendleft(cards[i])
        newCards.rotate(-n)
    if verbose: print(f"deal increment {n}: {cards} {newCards}")
    return newCards

def factoryOrder(size: int):
    return deque([i for i in range(size)])

def parseLine(cards: deque, line: str):
    if "deal with increment" in line:
        count = int(line.split("increment")[1])
        cards = dealIncrementN(cards, count)
    elif "deal into new stack" in line:
        cards = dealIntoNewStack(cards)
    elif "cut" in line:
        n = int(line.split(" ")[1])
        cards = cutNCards(cards, n)
    return cards

# Part 1
cards = factoryOrder(10007)
for line in data:
    cards = parseLine(cards, line)
print("Part1:", cards.index(2019))

# The math that follows really comes from this extremely helpful explanation of the math:
# https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/
# Without it, I wouldn't have understood how to do this problem at all!
def applyOp(offset: int, increment: int, size: int):
    for line in data:
        if 'cut' in line:
            offset += int(line.split(" ")[1]) * increment
            offset %= size
        elif 'stack' in line:
            increment *= -1
            increment %= size
            offset += increment
            offset %= size
        else:
            increment *= pow(int(line.split("increment")[1]), size-2, size)
            increment %= size
    return offset, increment

def calcOffset(offset_diff: int, increment_mul: int, iterations: int, mod: int):
    inv = lambda x: pow(x, mod-2, mod)
    offset = offset_diff * (1 - pow(increment_mul, iterations, mod)) * inv(1 - increment_mul)
    increment = pow(increment_mul, iterations, mod)
    return offset, increment

def getValAtOffset(offset, increment, pos, size):
    return (offset + increment*pos) % size

offset, increment = applyOp(0, 1, 119315717514047)
offset, increment = calcOffset(offset, increment, 101741582076661, 119315717514047)
print("Part2:", getValAtOffset(offset, increment, 2020, 119315717514047))