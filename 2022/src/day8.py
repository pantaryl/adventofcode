from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]
grid = squareGridFromChars(INPUT_DATA, isInts=True)
width = len(INPUT_DATA[0])
height = len(INPUT_DATA)

# Part 1
visible = 0
for pos, val in grid.items():
    real = int(pos.real)
    imag = int(pos.imag)
    if imag in [0, height - 1] or real in [0, width - 1]:
        visible += 1
    else:
        top_visible = all([True if grid[complex(real, i)] < val else False for i in range(0, imag)])
        bottom_visible = all([True if grid[complex(real, i)] < val else False for i in range(imag + 1, height)])

        left_visible  = all([True if grid[complex(i, imag)] < val else False for i in range(0, real)])
        right_visible = all([True if grid[complex(i, imag)] < val else False for i in range(real + 1, width)])

        if top_visible or bottom_visible or left_visible or right_visible:
            visible += 1

print(visible)

# Part 2
visibility = defaultdict(lambda: 1)
for pos, val in grid.items():
    real = int(pos.real)
    imag = int(pos.imag)

    if imag in [0, height - 1] or real in [0, width - 1]:
        continue

    for dir in getOrthogonalSquareNeighbors():
        visible = 0

        dir_pos = complex(pos.real, pos.imag)
        while True:
            dir_pos += dir
            if dir_pos not in grid: break
            elif grid[dir_pos] >= val:
                visible += 1
                break
            else: visible += 1

        visibility[pos] *= visible

max = sorted([(pos, visible) for pos, visible in visibility.items()], key = lambda x: x[1])[-1]
print(max)