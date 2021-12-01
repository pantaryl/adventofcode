from collections import defaultdict, deque
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
    data = [int(x) for x in data[0].split(",")]

lastCount = defaultdict(deque)
count = len(data) + 1
for i in range(len(data)):
    start = data[i]
    lastCount[start].appendleft(i + 1)

lastNumber = data[-1]
while count <= 2020:
    newNumber = 0
    if lastNumber in lastCount:
        if len(lastCount[lastNumber]) > 1:
            previousIdx = count - 1
            assert(previousIdx == lastCount[lastNumber][0])
            lastIdx     = lastCount[lastNumber][1]

            newNumber = previousIdx - lastIdx

    lastCount[newNumber].appendleft(count)
    count += 1
    lastNumber = newNumber

print(lastNumber)

while count <= 30000000:
    newNumber = 0
    if lastNumber in lastCount:
        if len(lastCount[lastNumber]) > 1:
            previousIdx = count - 1
            assert(previousIdx == lastCount[lastNumber][0])
            lastIdx     = lastCount[lastNumber][1]

            newNumber = previousIdx - lastIdx

    lastCount[newNumber].appendleft(count)
    count += 1
    lastNumber = newNumber

print(lastNumber)
