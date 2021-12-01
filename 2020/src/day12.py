from collections import defaultdict
from helpers import memoize
from copy import deepcopy

# Complex numbers in Python! == i + nj (x + ny), good for coordinates
# complex*i to rotate left/ccw, complex*-i to rotate right/cw

with open("../input/day12.txt", 'r') as inputFile:
    data = [x.rstrip() for x in inputFile.readlines()]
    #data = [int(x) for x in data]
# Part 1
pos   = 0 + 0j
slope = 1 + 0j
for line in data:
    direction = line[0]
    count     = int(line[1:])

    if direction == 'F':
        pos += slope * count
    elif direction == 'N':
        pos += complex(0, count)
    elif direction == 'E':
        pos += complex(count, 0)
    elif direction == 'W':
        pos += complex(-count, 0)
    elif direction == 'S':
        pos += complex(0, -count)
    elif direction == 'L':
        turns = count // 90
        slope *= complex(0, 1) ** turns
    elif direction == 'R':
        turns = count // 90
        slope *= complex(0, -1) ** turns

print(int(abs(pos.real) + abs(pos.imag)))

# Part 2
waypoint = 10 + 1j
pos      = 0  + 0j
for line in data:
    direction = line[0]
    count     = int(line[1:])

    if direction == 'F':
        pos += waypoint * count
    elif direction == 'N':
        waypoint += complex(0, count)
    elif direction == 'E':
        waypoint += complex(count, 0)
    elif direction == 'W':
        waypoint += complex(-count, 0)
    elif direction == 'S':
        waypoint += complex(0, -count)
    else:
        turns = (count // 90)
        if direction == 'L':
            waypoint *= complex(0, 1)**turns
        elif direction == 'R':
            waypoint *= complex(0, -1)**turns
    #print(f"{line} - pos = {pos}, waypoint = {waypoint}")

print(int(abs(pos.real) + abs(pos.imag)))