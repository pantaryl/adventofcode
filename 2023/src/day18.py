from shared import *

INPUT_DATA = [parse("{} {:d} (#{})", x) for x in INPUT_DATA]

def solve(isPart2):
    start_pos = OrderedComplex(0, 0)
    total = 0
    current = start_pos

    positions = [ start_pos ]

    for _dir, length, color in INPUT_DATA:
        if isPart2:
            # For part 2, color is actually our direction and length
            length = int(color[:-1], 16)
            _dir   = ['R', 'D', 'L', 'U'][int(color[-1])]

        if _dir == 'R':
            dir = OrderedComplex(1, 0)
        elif _dir == 'L':
            dir = OrderedComplex(-1, 0)
        elif _dir == 'U':
            dir = OrderedComplex(0, -1)
        elif _dir == 'D':
            dir = OrderedComplex(0, 1)

        next_vert = current + (dir * length)
        positions.append(next_vert)
        current = next_vert

    return shoelace(positions, True)

print(solve(False))
print(solve(True))