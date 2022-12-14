from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x.split(" -> ") for x in INPUT_DATA]

grid = defaultdict(lambda: '.')
for lines in INPUT_DATA:
    for i, pos_str in enumerate(lines[1:], 1):
        prev_pos = lines[i - 1].split(",")
        prev_pos = complex(int(prev_pos[0]), int(prev_pos[1]))

        pos_str  = pos_str.split(",")
        pos_str  = complex(int(pos_str[0]), int(pos_str[1]))

        for x in range(int(min(prev_pos.real, pos_str.real)), int(max(prev_pos.real, pos_str.real) + 1)):
            for y in range(int(min(prev_pos.imag, pos_str.imag)), int(max(prev_pos.imag, pos_str.imag) + 1)):
                grid[complex(x, y)] = '#'

start = 500+0j
min_x = min([int(x.real) for x in grid.keys()] + [500])
max_x = max([int(x.real) for x in grid.keys()] + [500])
min_y = min([int(x.imag) for x in grid.keys()] + [0])
max_y = max([int(x.imag) for x in grid.keys()] + [0])

# Part 1
part1 = deepcopy(grid)
current_sand = None
while True:
    if current_sand is None:
        current_sand = complex(start.real, start.imag)
    elif max_x < int(current_sand.real) or int(current_sand.real) < min_x or max_y < int(current_sand.imag) or int(current_sand.imag) < min_y:
        # We're endless.
        current_sand = None
        break
    else:
        # first try going down
        if part1[current_sand + 0+1j] == '.':
            current_sand += 0+1j
        # then down to the left
        elif part1[current_sand + -1+1j] == '.':
            current_sand += -1+1j
        # then down to the right
        elif part1[current_sand + 1+1j] == '.':
            current_sand += 1+1j
        else:
            # it must be at rest now
            part1[current_sand] = 'o'
            current_sand = None

print(sum([1 for _, val in part1.items() if val == 'o']))

# Part 2
floor = 2 + max_y
part2 = deepcopy(grid)
current_sand = None
while True:
    if part2[start] == 'o':
        break
    elif current_sand is None:
        current_sand = complex(start.real, start.imag)
    elif int((current_sand + 0+1j).imag) == floor:
        # it must be at rest now
        part2[current_sand] = 'o'
        current_sand = None
    else:
        # first try going down
        if part2[current_sand + 0+1j] == '.':
            current_sand += 0+1j
        # then down to the left
        elif part2[current_sand + -1+1j] == '.':
            current_sand += -1+1j
        # then down to the right
        elif part2[current_sand + 1+1j] == '.':
            current_sand += 1+1j
        else:
            # it must be at rest now
            part2[current_sand] = 'o'
            current_sand = None

print(sum([1 for _, val in part2.items() if val == 'o']))