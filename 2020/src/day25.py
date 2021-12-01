from collections import defaultdict, deque
from helpers import memoize
from copy import deepcopy
from enum import Enum
import os
from math_utils import *
from helpers import *

# Complex numbers in Python! == i + nj (x + ny), good for coordinates
# complex*+imaginary to rotate left/ccw, complex*-imaginary to rotate right/cw
# For example:
# Rotate CCW by 270 degrees:
#    val *= complex(0, 1) ** 3 [each power represents 90 degrees]

with open(f"../input/{os.path.splitext(os.path.basename(__file__))[0]}.txt", 'r') as inputFile:
    data = [x.rstrip() for x in inputFile.readlines()]
    #data = [int(x) for x in data]

card = int(data[0])
door = int(data[1])

def loop(subjectNumber: int, endResult = None, count: int = 100000000):
    newVal     = 1
    for i in range(0, count):
        newVal = newVal * subjectNumber
        newVal %= 20201227
        if endResult and newVal == endResult:
            return i + 1, None
    return newVal

cardLoopSize, _ = loop(7, card)
doorLoopSize, _ = loop(7, door)
print(cardLoopSize, doorLoopSize)

print(loop(door, None, count=cardLoopSize))