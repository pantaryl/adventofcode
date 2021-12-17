from shared import *

# Input data is in INPUT_DATA.
#INPUT_DATA = [int(x) for x in INPUT_DATA]
xStart, xEnd, yStart, yEnd = tuple(parse.parse("target area: x={:d}..{:d}, y={:d}..{:d}", INPUT_DATA[0]).fixed)

found = []
goals = set()

for x in range(xStart, xEnd + 1):
    for y in range(yStart, yEnd + 1):
        goals.add(complex(x, y))

for x in range(-abs(xStart), abs(xEnd) + 1):
    for y in range(-abs(yStart) - 1, abs(yStart) + 1):
        currentPos = complex(0, 0)
        startingVelocity = complex(x, y)
        velocity   = startingVelocity
        ys = []
        while currentPos.real <= xEnd and currentPos.imag >= yStart:
            currentPos += velocity
            if velocity.real > 0: velocity += complex(-1, 0)
            elif velocity.real < 0: velocity += complex(1, 0)

            velocity += complex(0, -1)

            ys.append(currentPos.imag)
            if currentPos in goals:
                found.append((startingVelocity, int(max(ys))))
                break


# Part 1
print(max(x[1] for x in found))

# Part 2
print(len(set([x[0] for x in found])))