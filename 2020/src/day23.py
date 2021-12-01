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
    data = [int(x) for x in data[0]]


def solve(cups, count):
    for i in range(0, count):
        currentCup = cups[0]
        cups.rotate(-1)

        threeCups = []
        for j in range(0, 3):
            threeCups.append(cups.popleft())

        destination = currentCup - 1
        if destination < min(cups):
            destination = max(cups)
        while destination > 0 and destination not in cups:
            if destination < min(cups):
                destination = max(cups)
            destination -= 1
        print(f"{currentCup} {threeCups} {destination}")
        while cups[0] != destination:
            cups.rotate(-1)
        cups.rotate(-1)
        cups.appendleft(threeCups[0])
        cups.rotate(-1)
        cups.appendleft(threeCups[1])
        cups.rotate(-1)
        cups.appendleft(threeCups[2])

        while cups[0] != currentCup:
            cups.rotate(-1)

        cups.rotate(-1)

    while cups[0] != 1:
        cups.rotate(-1)

cups = deque(data)
solve(cups, 100)
print("".join([str(x) for x in list(cups)[1:]]))

# Part 2
# A lookup-table and linked list make this solution fast. The LUT uses the label of the cup to get you the node,
# and the linked list makes it trivial to add/remove nodes as necessary.
cups = data + list(range(10, 1000000+1))
lut = {}
for i in range(1, 1000000 + 1):
    lut[i] = LLNode(i)

for i, val in enumerate(cups, 0):
    lut[val].next = lut[cups[(i+1) % len(cups)]]

currentCup = lut[cups[0]]
for step in range(10000000):
    if step % 1000000 == 0:
        print(f"{(step / 10000000)*100:2.0f}% complete.")
    threeCups = currentCup.next
    currentCup.next = currentCup.next.next.next.next

    currentCupVal = currentCup.val
    destination   = currentCupVal
    # For performance, explicitly use the four values you know it can't be.
    while destination in [currentCupVal, threeCups.val, threeCups.next.val, threeCups.next.next.val]:
        destination -= 1
        if destination == 0:
            destination = 1000000

    destinationCup = lut[destination]
    threeCups.next.next.next = destinationCup.next
    destinationCup.next = threeCups
    currentCup = currentCup.next

print(lut[1].next.val * lut[1].next.next.val)