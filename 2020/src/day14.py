from collections import defaultdict
from helpers import memoize
from copy import deepcopy
import os
from math_utils import *

# Complex numbers in Python! == i + nj (x + ny), good for coordinates
# complex*+imaginary to rotate left/ccw, complex*-imaginary to rotate right/cw
# For example:
# Rotate CCW by 270 degrees:
#    val *= complex(0, 1) ** 3 [each power represents 90 degrees]

with open(f"../input/{os.path.splitext(os.path.basename(__file__))[0]}.txt", 'r') as inputFile:
    data = [x.rstrip() for x in inputFile.readlines()]
    #data = [int(x) for x in data]

# Part 1

def applyMask(mask, number):
    andMask = int("0b" + "".join(['1' if x == 'X' else '0' for x in mask]), 2)
    orMask  = int("0b" + "".join([x if x != 'X' else '0' for x in mask]), 2)

    return (number & andMask) | (orMask)

mask   = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
memory = {}

for line in data:
    if 'mask' in line:
        mask = line.split(" = ")[1]
    else:
        location, number = line.split(" = ")
        location = location.replace("mem", "").replace("[", "").replace("]", "")
        number   = int(number)

        memory[location] = applyMask(mask, number)


print(sum(memory.values()))

# Part 2

def determineMemoryLocations(mask: str, memLoc: int):
    binaryMemLoc  = f"{memLoc:036b}"
    updatedMemLoc = ""
    for i in range(len(mask)):
        maskChar = mask[i]
        locChar  = binaryMemLoc[i]

        if maskChar == '0':
            updatedMemLoc += locChar
        elif maskChar == '1':
            updatedMemLoc += "1"
        elif maskChar == 'X':
            updatedMemLoc += "X"

    answers = [ "", ]
    for char in updatedMemLoc[::-1]:
        if char == 'X':
            existing = deepcopy(answers)
            for i in range(len(answers)):
                answers[i] = '0' + answers[i]
            for i in range(len(existing)):
                existing[i] = '1' + existing[i]
            answers.extend(existing)
        else:
            for i in range(len(answers)):
                answers[i] = char + answers[i]

    return answers

mask   = "000000000000000000000000000000000000"
memory = {}
for line in data:
    if 'mask' in line:
        mask = line.split(" = ")[1]
    else:
        location, number = line.split(" = ")
        location = int(location.replace("mem", "").replace("[", "").replace("]", ""))
        number   = int(number)

        locations = determineMemoryLocations(mask, location)
        for loc in locations:
            memory[loc] = number

print(sum(memory.values()))