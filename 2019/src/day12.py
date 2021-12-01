from typing import List, Optional
import math

with open("../input/day12.txt", 'r') as inputFile:
    data = inputFile.readlines()

posStr = [line.rstrip()[1:-1].lstrip().split(", ") for line in data]
moons  = [[int(coord[2:]) for coord in line] + [0, 0, 0] for line in posStr]

def step(moons: list):
    outputMoons = [newMoon[:] for newMoon in moons]
    for i, moonA in enumerate(moons):
        for j, moonB in enumerate(moons):
            if i >= j:
                continue
            for axis in (0, 1, 2):
                if moonA[axis] < moonB[axis]:
                    outputMoons[i][axis+3] += 1
                    outputMoons[j][axis+3] -= 1
                elif moonA[axis] > moonB[axis]:
                    outputMoons[i][axis+3] -= 1
                    outputMoons[j][axis+3] += 1
    for newMoon in outputMoons:
        newMoon[0] += newMoon[3]
        newMoon[1] += newMoon[4]
        newMoon[2] += newMoon[5]

    return outputMoons


def calcTotalEnergy(moons: list):
    totalEnergy = 0
    for moon in moons:
        potential = sum([abs(x) for x in moon[:3]])
        kinetic   = sum([abs(x) for x in moon[3:]])
        totalEnergy += potential * kinetic
    return totalEnergy


seen = [set()] * 3
rep = [None] * 3
i = 0
while all([rep[axis] is not None for axis in (0, 1, 2)]) is False:
    moons = step(moons)
    for axis in (0, 1, 2):
        if rep[axis] is None:
            vis = "::".join("-".join([f"{moon[axis]}, {moon[axis+3]}" for moon in moons]))
            if vis in seen[axis]:
                rep[axis] = i
            else:
                seen[axis].add(vis)
    i += 1

    # Part 1
    if i == 1000:
        print("Part1:", calcTotalEnergy(moons))

# Part 2
def leastCommonMultiple(a: int, b: int):
    return a // math.gcd(a, b) * b

rep: List[Optional[int]]
print("Part2:", leastCommonMultiple(rep[0], leastCommonMultiple(rep[1], rep[2])))