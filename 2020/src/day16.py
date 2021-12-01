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

rules    = {}
myTicket = []
tickets  = []

i = 0
# This will parse the rules
while data[i] != "" and data[i] != "\n":
    line = data[i]
    line = line.split(": ")

    ruleName = line[0]

    ranges   = line[1].split(" or ")
    ranges   = [x.split("-") for x in ranges]
    ranges   = [(int(x[0]), int(x[1])) for x in ranges]

    rules[ruleName] = ranges

    i += 1

# This parses my ticket.
i += 1
assert(data[i] == "your ticket:")
i += 1
myTicket = [int(x) for x in data[i].split(",")]
i += 1
assert(data[i] == "" or data[i] == "\n")
i += 1
assert(data[i] == "nearby tickets:")
i += 1

while i < len(data):
    tickets.append([int(x) for x in data[i].split(",")])
    i += 1

def isValidRange(value, ranges) -> bool:
    firstRange  = ranges[0]
    secondRange = ranges[1]
    return value in range(firstRange[0], firstRange[1] + 1) or value in range(secondRange[0], secondRange[1] + 1)

# Part 1
ticketErrorRate = 0
invalidTickets  = []
for ticket in tickets:
    for value in ticket:
        validValue = False
        for _, ranges in rules.items():
            if isValidRange(value, ranges):
                validValue = True
                break
        if validValue is False:
            ticketErrorRate += value
            if ticket not in invalidTickets: invalidTickets.append(ticket)

print(ticketErrorRate)

# Part 2
for invalid in invalidTickets:
    tickets.remove(invalid)

rulePos = defaultdict(list)
for rule, ranges in rules.items():
    positions = []
    for i in range(len(myTicket)):
        valids = 0
        for ticket in tickets:
            if isValidRange(ticket[i], ranges): valids += 1
        if isValidRange(myTicket[i], ranges): valids += 1
        positions.append(valids)

    for i in range(len(positions)):
        position = positions[i]
        if position == len(tickets) + 1:
            rulePos[rule].append(i)

# Reduce the positions down:
while True:
    if all([True if len(positions) == 1 else 0 for positions in rulePos.values()]):
        break

    for _, positions in rulePos.items():
        if len(positions) == 1:
            value = positions[0]
            for other_, otherPositions in rulePos.items():
                if _ == other_: continue
                if value in otherPositions: otherPositions.remove(value)

myTicketMultiplier = 1
for rule, positions in rulePos.items():
    if "departure" in rule:
        assert(len(positions) == 1)
        myTicketMultiplier *= myTicket[positions[0]]
print(myTicketMultiplier)