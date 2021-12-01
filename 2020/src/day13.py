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

earliestDepart = int(data[0])

# Part 1
availableBuses = [int(x) for x in data[1].split(",") if x.isnumeric()]

closeNums = defaultdict(list)
closestNums = []

for bus in availableBuses:
    time = bus
    while True:
        closeNums[bus].append(time)

        if time >= earliestDepart:
            closestNums.append(time)
            break

        time += bus


#print(earliestDepart)
#print(closestNums)
closestTime = min(closestNums)
#print(closestTime)

waitTime = closestTime - earliestDepart
print(waitTime * availableBuses[closestNums.index(closestTime)])

# Part 2
buses = [x for x in data[1].split(",")]

numbers    = deepcopy(availableBuses)
indices    = [buses.index(str(x)) for x in availableBuses]
remainders = [numbers[i] - (indices[i] % numbers[i]) for i in range(len(availableBuses))]

print(crt(numbers, remainders))