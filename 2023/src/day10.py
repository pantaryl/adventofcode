from shared import *

grid = squareGridFromChars(INPUT_DATA)
start_pos = [pos for pos, char in grid.items() if char == 'S'][0]

def get_neighbors(pos):
    if pos not in grid: return

    current_type = grid[pos]

    if current_type == '-':
        yield pos + -1 + 0j
        yield pos +  1 + 0j
    elif current_type == '|':
        yield pos +  0 - 1j
        yield pos +  0 + 1j
    elif current_type == 'L':
        yield pos + 0 - 1j
        yield pos + 1 + 0j
    elif current_type == 'J':
        yield pos + 0 - 1j
        yield pos + -1 + 0j
    elif current_type == '7':
        yield pos + 0 + 1j
        yield pos + -1 + 0j
    elif current_type == 'F':
        yield pos + 0 + 1j
        yield pos + 1 + 0j

neighbors = []
for dir in getOrthogonalSquareNeighbors():
    for neighbor in get_neighbors(start_pos + dir):
        if neighbor == start_pos:
            neighbors.append(dir)

assert len(neighbors) == 2
neighbors = set(neighbors)

if neighbors == { -1 + 0j, 1 + 0j }:
    grid[start_pos] = '-'
elif neighbors == { 0 + -1j, 0 + 1j }:
    grid[start_pos] = '|'
elif neighbors == { 0 + -1j, 1 + 0j }:
    grid[start_pos] = 'L'
elif neighbors == {0 + -1j, -1 + 0j}:
    grid[start_pos] = 'J'
elif neighbors == {0 + 1j, -1 + 0j}:
    grid[start_pos] = '7'
elif neighbors == {0 + 1j, 1 + 0j}:
    grid[start_pos] = 'F'

stack = [ [ start_pos ] ]
paths = []
longest_path = {}
seen = set()
while stack:
    current_path = stack.pop()
    current_pos  = current_path[-1]

    if current_pos not in grid:
        continue

    if longest_path.get(current_pos, 999999999999) < len(current_path):
        continue

    longest_path[current_pos] = len(current_path) - 1

    current_type = grid[current_pos]
    seen.add(current_pos)

    if current_type == '-':
        stack.append(current_path + [ current_pos + 1 + 0j ])
        stack.append(current_path + [ current_pos + -1 + 0j ])
    elif current_type == '|':
        stack.append(current_path + [ current_pos + 0 - 1j ])
        stack.append(current_path + [ current_pos + 0 + 1j ])
    elif current_type == 'L':
        stack.append(current_path + [ current_pos + 0 - 1j ])
        stack.append(current_path + [ current_pos + 1 + 0j ])
    elif current_type == 'J':
        stack.append(current_path + [ current_pos + 0 - 1j ])
        stack.append(current_path + [ current_pos + -1 + 0j ])
    elif current_type == '7':
        stack.append(current_path + [ current_pos + 0 + 1j ])
        stack.append(current_path + [ current_pos + -1 + 0j ])
    elif current_type == 'F':
        stack.append(current_path + [ current_pos + 0 + 1j ])
        stack.append(current_path + [ current_pos + 1 + 0j ])
    else:
        assert False, f"{current_pos}, {current_type}"

part1 = sorted([length for _, length in longest_path.items()], reverse=True)[0]
print(part1)

count = 0
x_dim, y_dim = get_min_max(longest_path.keys())
for y in range(y_dim[0], y_dim[1] + 1):
    for x in range(x_dim[0], x_dim[1] + 1):
        pos = complex(x, y)
        if pos in longest_path: continue

        seen_pipes = 0
        next_pos = pos + -1+0j
        while next_pos.real >= 0:
            if next_pos in longest_path and grid[next_pos] in ("|", 'J', 'L'):
                seen_pipes += 1
            next_pos += -1+0j
        if seen_pipes % 2 == 1:
            count += 1
print(count)