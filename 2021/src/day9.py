from shared import *

# Input data is in INPUT_DATA.
# INPUT_DATA = [int(x) for x in INPUT_DATA]
caves = squareGridFromChars(INPUT_DATA, isInts=True)

# Part 1

lowPoints = []
for pos, val in caves.items():
    lower = True
    for neighbor in getOrthogonalSquareNeighbors():
        if pos + neighbor in caves:
            if caves[pos + neighbor] <= val:
                lower = False
                break
        if lower is False: break

    if lower:
        lowPoints.append((pos, val))

print(sum([x[1] + 1 for x in lowPoints]))

# Part 2
lowPointPos = [x[0] for x in lowPoints]
basins = []
for pos in lowPointPos:
    seen  = set()
    stack = [ pos ]
    while stack:
        currentPos = stack.pop()
        currentVal = caves[currentPos]
        assert(currentVal != 9)
        seen.add(currentPos)

        for neighbor in getOrthogonalSquareNeighbors():
            neighborPos = currentPos + neighbor
            neighborVal = caves.get(neighborPos, None)
            if neighborVal and neighborPos not in seen and neighborVal > currentVal and neighborVal != 9:
                stack.append(neighborPos)

    _debug = False
    if _debug:
        maxI = int(max([x.real for x in seen]))
        minI = int(min([x.real for x in seen]))
        maxJ = int(max([x.imag for x in seen]))
        minJ = int(min([x.imag for x in seen]))

        print(pos - complex(minI, minJ), pos)
        for j in range(minJ, maxJ + 1):
            for i in range(minI, maxI + 1):
                if complex(i, j) not in seen:
                    print('X', end='')
                else:
                    print(caves[complex(i, j)], end='')
            print()
        print()
        print()


    basins.append(len(seen))

largest = sorted(basins, reverse=True)
print(largest[0] * largest[1] * largest[2])