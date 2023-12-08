from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]

directions = INPUT_DATA[0]
paths = {}
for line in INPUT_DATA[2:]:
    start, left, right = parse("{} = ({}, {})", line)
    paths[start] = (left, right)

@memoize
def get_next(index):
    next, current_pos = index
    if next == "L":
        next_pos = paths[current_pos][0]
    else:
        next_pos = paths[current_pos][1]

    return next_pos

stack = [ 'AAA' ]
pos   = 0
count = 0
while True:
    current = stack.pop()

    if current == 'ZZZ':
        break

    next = directions[pos % len(directions)]
    next_pos = get_next((next, current))
    stack.append(next_pos)

    pos   += 1
    count += 1

print(count)

starting_pos = [x for x in paths.keys() if x[2] == 'A']
end_pos      = [x for x in paths.keys() if x[2] == 'Z']

current  = {x: [x] for x in starting_pos}
seen_end = {}
pos     = 0
while True:
    next = directions[pos % len(directions)]

    for start, depth in current.items():
        current_pos = depth[-1]
        next_pos    = get_next((next, current_pos))

        depth.append(next_pos)

        if next_pos[2] == 'Z':
            if start not in seen_end:
                seen_end[start] = len(depth) - 1

    if len(seen_end) == len(starting_pos):
        break

    pos += 1

print(lcm(seen_end.values()))