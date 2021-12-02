from shared import *

# Input data is in INPUT_DATA.
# INPUT_DATA = [int(x) for x in INPUT_DATA]

# Part 1
horiz = 0
depth = 0

for line in INPUT_DATA:
    dir, dist = line.split(" ")
    if dir == "forward": horiz += int(dist)
    elif dir == "down": depth += int(dist)
    elif dir == "up": depth -= int(dist)

print(horiz * depth)

# Part 2
horiz = 0
depth = 0
aim = 0
for line in INPUT_DATA:
    dir, dist = line.split(" ")
    if dir == "forward":
        horiz += int(dist)
        depth += aim * int(dist)
    elif dir == "down": aim += int(dist)
    elif dir == "up": aim -= int(dist)

print(horiz * depth)