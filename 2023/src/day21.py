from shared import *

grid = Grid(INPUT_DATA)
start_pos = [pos for pos, value in grid.items() if value == 'S'][0]

def solve(part2: bool, max_distance: int):
    seen = set()
    final = set()
    queue = deque( [(start_pos, 0)]  )
    while queue:
        data = queue.popleft()
        current, distance = data
        if data in seen:
            continue
        seen.add(data)

        if distance == max_distance:
            continue

        for dir in getOrthogonalSquareNeighbors():
            neighbor        = current + dir
            search_neighbor = neighbor
            if part2:
                x, y = complex_to_int_tuple(neighbor)
                search_neighbor = OrderedComplex(x % grid.width, y % grid.height)
                assert search_neighbor in grid

            if grid.get(search_neighbor, '#') in ('.', 'S'):
                queue.append((neighbor, distance + 1))

    return seen

results = solve(False, 64)
print(len([x for _, x in results if x == 64]))

results = solve(True, 65 + 2 * 131)
a0 = len([x for _, x in results if x == 65])
a1 = len([x for _, x in results if x == 65 + 131])
a2 = len([x for _, x in results if x == 65 + 2 * 131])

A = (a2 - 2 * a1 + a0) // 2
B = (a1 - a0) - 3 * A
C = a0 - B - A

polynomial = [
    A,
    B,
    C
]

# 26501365 = 202300 * 131 + 65 where 131 is the dimension of the grid
iteration_count = math.ceil(26501365 / 131)
print(int(polynomial[0] * (iteration_count ** 2) + polynomial[1] * iteration_count + polynomial[2]))