from typing import NamedTuple

with open("../input/day5.txt", 'r') as inputFile:
    data = inputFile.readlines()

BoardingPass = NamedTuple("BoardingPass", [('row', str), ('col', str)])

passes = []
for line in data:
    line = line.rstrip()
    newPass = BoardingPass(line[0:7], line[7:])
    passes.append(newPass)

def determineBounds(low: int, high: int, operations: str) -> int:
    while low != high:
        currentVal = operations[0]
        if currentVal == 'F' or currentVal == 'L':
            high -= (high - low + 1) // 2
        else:
            assert(currentVal == 'B' or currentVal == 'R')
            low += ((high - low + 1) // 2)
        if len(operations) > 1:
            operations = operations[1:]

    return low

passesById = {}

def determineSeatId(elfPass : BoardingPass):
    row = determineBounds(0, 127, elfPass.row)
    col = determineBounds(0, 7,   elfPass.col)

    passesById[(row * 8) + col] = (row, col)

    return (row * 8) + col

ids = []
for elfPass in passes:
    ids.append(determineSeatId(elfPass))

print(max(ids))

for num in range(0, 128 * 8):
    row = num % 128
    col = num // 128
    id = (row * 8 + col)
    if id not in passesById and id+1 in passesById and id-1 in passesById:
        print(id)
        break