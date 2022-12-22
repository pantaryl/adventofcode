from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]

conversion_dict = {
    ' ': None,
    '.': '.',
    '#': '#',
}
grid = squareGridFromChars(INPUT_DATA[:-1], conversionDict=conversion_dict)
left_topmost = min(grid.keys())

#print(left_topmost)

rotate_right = lambda x: x * complex(0, 1)
rotate_left  = lambda x: x * complex(0, -1)
dir = 1+0j
current_pos = left_topmost

# Part 1
instructions = re.split(r'(\d+)', INPUT_DATA[-1].lstrip().rstrip())
#print(instructions)

for instruction in instructions:

    if instruction == '':
        continue

    #print(f"Instruction: {instruction}")

    if instruction == 'R':
        dir = rotate_right(dir)
        #print(f"Rotated right. Going {dir}")
    elif instruction == 'L':
        dir = rotate_left(dir)
        #print(f"Rotated left. Going {dir}")
    elif instruction.isdigit():
        count = int(instruction)
        for i in range(count):
            value = grid.get(current_pos + dir, None)
            if value == '.':
                #print(f"Moving forward. Was {current_pos}, now {current_pos + dir}")
                current_pos += dir
            elif value == '#':
                #print(f"Can't move forward. Hit wall at {current_pos + dir}")
                break
            else:
                # We're at an edge. Find the opposite side.
                next_pos = None
                if dir == 1+0j:
                    # We're going right, find the min on the left.
                    next_pos = complex(min([x.real for x in grid.keys() if x.imag == current_pos.imag]), current_pos.imag)
                elif dir == -1+0j:
                    # We're going left, find the max on the right.
                    next_pos = complex(max([x.real for x in grid.keys() if x.imag == current_pos.imag]), current_pos.imag)
                elif dir == 0+1j:
                    # We're going down, find the min on the top.
                    next_pos = complex(current_pos.real, min([x.imag for x in grid.keys() if x.real == current_pos.real]))
                elif dir == 0-1j:
                    # We're going up, find the max on the bottom.
                    next_pos = complex(current_pos.real, max([x.imag for x in grid.keys() if x.real == current_pos.real]))

                if grid.get(next_pos) == '.':
                    #print(f"Moving from {current_pos} to {next_pos}")
                    current_pos = next_pos
                else:
                    assert(grid.get(next_pos) == '#')
                    #print(f"Hit wall at {next_pos}, staying at {current_pos}")
                    break

row = int(current_pos.imag) + 1
column = int(current_pos.real) + 1
facing = { 1+0j: 0, 0+1j: 1, -1+0j: 2, 0-1j: 3 }[dir]
print((row * 1000) + (column * 4) + facing)

# Part 2

# Make the faces numbered. This part is generic.
count = 1
x_dim, y_dim = get_min_max(grid.keys())
layout = {}
print("===")
for y in range(y_dim[0] // 50, (y_dim[1] // 50) + 1):
    for x in range(x_dim[0] // 50, (x_dim[1] // 50) + 1):
        if grid.get(complex(x * 50, y * 50), None):
            print(count, end='')
            layout[complex(x, y)] = count
            count += 1
        else:
            print(' ', end='')
    print()
print("===")

# Define the "teleportation/transportation" rules for each face going in a specific direction.
# This part is *not* generic and is hardcoded to my input.
# Some of these rules are unnecessary. The only rules that should be necessary are those that hop into
# unexplored areas.
transportation = {
    1: {
        1+0j: (lambda x: x + 1+0j, 1+0j),
        -1+0j: (lambda x: complex(0, 149 - x.imag), 1+0j),
        0+1j: (lambda x: x + 1j, 0+1j),
        0-1j: (lambda x: complex(0, x.real + 100), 1+0j)
    },
    2: {
        1+0j: (lambda x: complex(99, 149-x.imag), -1+0j),
        -1+0j: (lambda x: x + -1+0j, -1+0j),
        0+1j: (lambda x: complex(99, x.real - 100 + 50), -1+0j),
        0-1j: (lambda x: complex(x.real - 100, 199), 0-1j),
    },
    3: {
        1+0j: (lambda x: complex(x.imag - 50 + 100, 49), 0-1j),
        -1+0j: (lambda x: complex(x.imag - 50, 100), 0+1j),
        0+1j: (lambda x: x + 0+1j, 0+1j),
        0-1j: (lambda x: x + 0-1j, 0-1j),
    },
    4: {
        1+0j: (lambda x: x + 1+0j, 1+0j),
        -1+0j: (lambda x: complex(50, 49 - (x.imag - 100)), 1+0j),
        0+1j: (lambda x: x + 0+1j, 0+1j),
        0-1j: (lambda x: complex(50, x.real + 50), 1+0j)
    },
    5: {
        1+0j: (lambda x: complex(149, 49 - (x.imag - 100)), -1+0j),
        -1+0j: (lambda x: x + -1+0j, -1+0j),
        0+1j: (lambda x: complex(49, x.real - 50 + 150), -1+0j),
        0-1j: (lambda x: x + 0-1j, 0-1j)
    },
    6: {
        1+0j: (lambda x: complex(x.imag - 150 + 50, 149), 0-1j),
        -1+0j: (lambda x: complex(x.imag - 150 + 50, 0), 0+1j),
        0+1j: (lambda x: complex(x.real + 100, 0), 0+1j),
        0-1j: (lambda x: x + 0-1j, 0-1j)
    }
}

# Reset our current position to the left-topmost one, and our dir to right.
current_pos = left_topmost
dir = 1+0j
for instruction in instructions:
    if instruction == '':
        continue

    #print(f"Instruction: {instruction}")

    if instruction == 'R':
        dir = rotate_right(dir)
        #print(f"Rotated right. Going {dir}")
    elif instruction == 'L':
        dir = rotate_left(dir)
        #print(f"Rotated left. Going {dir}")
    elif instruction.isdigit():
        count = int(instruction)
        for i in range(count):
            value = grid.get(current_pos + dir, None)
            if value == '.':
                #print(f"Moving forward. Was {current_pos}, now {current_pos + dir}")
                current_pos += dir
            elif value == '#':
                #print(f"Can't move forward. Hit wall at {current_pos + dir}")
                break
            else:
                # We're at an edge. Find the opposite side.

                # Determine what the origin of our face is, and then from that which face we are.
                origin = complex(current_pos.real // 50, current_pos.imag // 50)
                face   = layout[origin]

                # Retrieve the transportation equation and our new dir on that face.
                eq, new_dir = transportation[face][dir]
                # Determine what our position on the new face will be.
                next_pos = eq(current_pos)

                # This next bit is sanity checking.
                # We should be able to, from our new position, turn around and come back
                # to our original position.
                # If we don't, then there is a bug in our transportation equations.
                san_origin = complex(next_pos.real // 50, next_pos.imag // 50)
                san_face   = layout[san_origin]
                san_eq, san_new_dir = transportation[san_face][new_dir * complex(0, 1) ** 2]
                orig_pos = san_eq(next_pos)
                assert current_pos == orig_pos
                assert dir         == (san_new_dir * complex(0, 1) ** 2)

                if grid.get(next_pos) == '.':
                    #print(f"Moving from {current_pos} to {next_pos}")
                    # We only update our current position and direction to the new ones
                    # if we can move there. Otherwise we stay facing the same way.
                    current_pos = next_pos
                    dir         = new_dir
                else:
                    assert grid.get(next_pos) == '#', (current_pos, dir, next_pos, new_dir, origin, face)
                    #print(f"Hit wall at {next_pos}, staying at {current_pos}")
                    break

row = int(current_pos.imag) + 1
column = int(current_pos.real) + 1
facing = { 1+0j: 0, 0+1j: 1, -1+0j: 2, 0-1j: 3 }[dir]
print((row * 1000) + (column * 4) + facing)