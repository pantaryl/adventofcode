from shared import *

grid = squareGridFromChars(INPUT_DATA)

cols_to_copy = set()
rows_to_copy = set()

x_range, y_range = grid_ranges(grid.keys())
for y in y_range:
    if all([grid[complex(x, y)] == '.' for x in x_range]):
        rows_to_copy.add(y)

for x in x_range:
    if all([grid[complex(x, y)] == '.' for y in y_range]):
        cols_to_copy.add(x)

galaxies = {pos for pos, val in grid.items() if val == '#'}
pairs    = set(combinations(galaxies, 2))

INCREASE_P1 = 2
INCREASE_P2 = 1000000
distances = 0
part1     = 0
part2     = 0
for i, data in enumerate(pairs):
    start, end = data
    distances += manhattanDistance(start, end)

    x_start, y_start = complex_to_int_tuple(start)
    x_end,   y_end   = complex_to_int_tuple(end)

    copied_rows = 0
    copied_cols = 0

    for row in rows_to_copy:
        if y_start < row < y_end or y_end < row < y_start:
            copied_rows += 1
    for col in cols_to_copy:
        if x_start < col < x_end or x_end < col < x_start:
            copied_cols += 1

    part1 += (copied_rows + copied_cols) * (INCREASE_P1 - 1)
    part2 += (copied_rows + copied_cols) * (INCREASE_P2 - 1)

print(distances + part1)
print(distances + part2)