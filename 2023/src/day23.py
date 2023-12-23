from shared import *

grid = Grid(INPUT_DATA)
start_pos = [pos for pos, value in grid.items() if pos.imag == 0 and value == '.'][0]
end_pos   = [pos for pos, value in grid.items() if pos.imag == grid.height - 1 and value == '.'][0]

def generateShortcuts():
    shortcuts = {}
    stack = [(start_pos, None)]
    while stack:
        orig, prev = stack.pop()
        length = 0

        if orig in shortcuts:
            continue

        current = orig
        seen = {current, prev}

        only_one = True
        while only_one:
            next_locs = []
            current_value = grid[current]
            next_dir = { '^': -1j, 'v': 1j, '>': 1, '<': -1, '.': None }[current_value]
            if next_dir:
                neighbor = current + next_dir
                if grid.get(neighbor, '#') != '#' and neighbor not in seen:
                    next_locs.append(neighbor)
            else:
                not_possible = { -1: '>', 1: '<', 1j: "^", -1j: "v" }
                for dir in getOrthogonalSquareNeighbors():
                    neighbor = current + dir
                    next_val = grid.get(neighbor, '#')
                    if next_val not in ('#', not_possible[dir]) and neighbor not in seen:
                        next_locs.append(neighbor)

            num_next_locs = len(next_locs)
            if num_next_locs == 1:
                length += 1
                prev = current
                current = next_locs[0]
                seen.add(current)
            elif num_next_locs == 0 and current == end_pos:
                shortcuts[orig] = (current, prev, length, seen | {current})
                break
            elif num_next_locs > 0:
                only_one = False
                shortcuts[orig] = (current, prev, length, seen | {current})
                for neighbor in next_locs:
                    stack.append((neighbor, current))
            else:
                break

    return shortcuts

def find_longest_path(shortcuts: Dict[OrderedComplex, Tuple[OrderedComplex, OrderedComplex, int]]):
    stack = deque([ (start_pos, None, 0, set()) ])
    max_length = 0

    DP = set()
    while stack:
        data = stack.pop()
        current, prev, length, seen = data

        if (current, prev, length) in DP:
            continue

        DP.add((current, prev, length))

        if current in shortcuts:
            next_pos, prev, next_length, next_seen = shortcuts[current]
            stack.append((next_pos, prev, length + next_length, seen | next_seen | { next_pos, prev }))
            continue

        seen |= { current, prev }

        if current == end_pos:
            if length > max_length:
                max_length = length
            continue

        current_value = grid[current]
        next_dir = {'^': -1j, 'v': 1j, '>': 1, '<': -1, '.': None}[current_value]
        if next_dir:
            neighbor = current + next_dir
            if grid.get(neighbor, '#') != '#' and neighbor not in seen:
                stack.append((neighbor, current, length + 1, seen | { neighbor }))
        else:
            not_possible = { -1: '>', 1: '<', 1j: "^", -1j: "v" }
            for dir in getOrthogonalSquareNeighbors():
                neighbor = current + dir
                next_val = grid.get(neighbor, '#')
                if next_val not in ('#', not_possible[dir]) and neighbor not in seen:
                    stack.append((neighbor, current, length + 1, seen | {neighbor}))

    return max_length

shortcuts = generateShortcuts()
print(find_longest_path(shortcuts))

# Let's generate a graph of edges instead of brute forcing it.
edges = defaultdict(set)
for y in grid.y_range:
    for x in grid.x_range:
        current = OrderedComplex(x, y)
        if grid[current] in ".>v":
            for dir in getOrthogonalSquareNeighbors():
                neighbor = current + dir
                if grid.get(neighbor, '#') in ".>v":
                    edges[current].add((neighbor, 1))
                    edges[neighbor].add((current, 1))

# Now reduce the edges down.
while True:
    for current, edge in edges.items():
        if len(edge) == 2:
            _prev, _next = edge
            edges[_prev[0]].remove((current, _prev[1]))
            edges[_next[0]].remove((current, _next[1]))
            edges[_prev[0]].add((_next[0], _prev[1] + _next[1]))
            edges[_next[0]].add((_prev[0], _prev[1] + _next[1]))
            del edges[current]
            break
    else:
        break

stack = [ (start_pos, 0, set()) ]
max_length = 0
while stack:
    current, length, seen = stack.pop()

    if current == end_pos:
        max_length = max(max_length, length)
        continue

    if current in seen:
        continue

    seen.add(current)

    for neighbor, next_length in edges[current]:
        stack.append((neighbor, length + next_length, set(seen)))

print(max_length)