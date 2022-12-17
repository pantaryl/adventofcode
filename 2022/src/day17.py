from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = deque([x for x in INPUT_DATA[0]])
orig_input = list(INPUT_DATA)

width = 7

shape_list = deque(['-', '+', 'L', '|', '▮' ])
orig_shapes = list(shape_list)
shapes = {
    '-': {
        'layout': [
            0+0j, 1+0j, 2+0j, 3+0j
        ],
        'leftedge': 0+0j,
        'bottom': [ 0+0j, 1+0j, 2+0j, 3+0j ],
        'width': 4,
        'height': 1
    },
    '+': {
        'layout': [
            1+0j, 0-1j, 1-1j, 2-1j, 1-2j
        ],
        'leftedge': 0-1j,
        'bottom': [ 1+0j ],
        'width': 3,
        'height': 3
    },
    'L': {
        'layout': [
            0+0j, 1+0j, 2+0j, 2-1j, 2-2j
        ],
        'leftedge': 0+0j,
        'bottom': [ 0+0j, 1+0j, 2+0j ],
        'width': 3,
        'height': 3
    },
    '|': {
        'layout': [
            0+0j, 0-1j, 0-2j, 0-3j
        ],
        'leftedge': 0+0j,
        'bottom': [ 0+0j ],
        'width': 1,
        'height': 4
    },
    '▮': {
        'layout': [
            0+0j, 1+0j, 0-1j, 1-1j
        ],
        'leftedge': 0+0j,
        'bottom': [ 0+0j, 1+0j ],
        'width': 2,
        'height': 2
    },
}

directions = {
    '>': 1+0j,
    "<": -1+0j,
}

grid = defaultdict(lambda: '.')
for x in range(-1, 8):
    grid[x+4j] = '-'

for y in range(-10000, 5):
    grid[complex(-1, y)] = '|'
    grid[complex(7, y)] = '|'

left_start   = 2+0j
bottom       = 0+0j
current_shape = 0
current_char  = 0
current_pos  = None
# Part 1
changes = ""
i = 0
seen = {}
def do_fall(upper_bound, part2 = False):
    global i, changes, current_shape, current_char, current_pos, bottom
    while i < upper_bound:
        if current_pos is None:
            # Need to spawn the shape now
            start = left_start + bottom
            shape = shape_list[current_shape % len(shape_list)]
            current_pos = [start + x for x in shapes[shape]['layout']]

        char = INPUT_DATA[current_char % len(INPUT_DATA)]
        current_char += 1
        dir = directions[char]
        if any([grid[x+dir] != '.' for x in current_pos]):
            # We hit a wall or rocks. This movement doesn't happen.
            pass
        else:
            current_pos = [x+dir for x in current_pos]

        # Now that we've moved left or right, we have to handle down.
        dir = 0+1j
        if any([grid[x + dir] != '.' for x in current_pos]):
            i += 1
            prev_bottom = bottom
            bottom = complex(0, min([int(x.imag) - 4 for x in current_pos] + [int(bottom.imag)]))
            changes += str(int(prev_bottom.imag - bottom.imag))

            # We're going to hit something, so we stop here without moving.
            for x in current_pos:
                grid[x] = '#'
            current_shape += 1
            current_pos  = None

            value = (current_shape % len(shape_list), current_char % len(INPUT_DATA), changes[-30:])
            if part2 and value in seen:
                rock_idx, new_changes = seen[value]

                new_bottom = abs(int(bottom.imag))
                cycle_count = i - rock_idx
                cycle = changes[-cycle_count:]
                increase_per_cycle = sum([int(x) for x in cycle])
                remaining_cycles = ((upper_bound - i) // cycle_count)
                new_bottom += remaining_cycles * increase_per_cycle
                i += remaining_cycles * cycle_count

                if i < upper_bound:
                    new_bottom += sum([int(x) for x in cycle[0:(upper_bound - i)]])
                    i = upper_bound
                bottom = complex(0, new_bottom)
            else:
                seen[value] = (i, changes)
        else:
            current_pos = [x + dir for x in current_pos]

do_fall(2022)
print(abs(int(bottom.imag)))

# Part 2
do_fall(1000000000000, True)
print(abs(int(bottom.imag)))