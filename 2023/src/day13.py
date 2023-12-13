from shared import *

row_grids = [[]]
for line in INPUT_DATA:
    if line == "":
        row_grids.append([])
    else:
        row_grids[-1].append(0)
        for i, char in enumerate(line):
            row_grids[-1][-1] |= (0 if char == '.' else 1) << i

col_grids = [[]]
for i, line in enumerate(INPUT_DATA):
    if line == "":
        col_grids.append([])
    else:
        if len(col_grids[-1]) != len(line):
            col_grids[-1] = [0] * len(line)
        for j, char in enumerate(line):
            col_grids[-1][j] |= (0 if char == '.' else 1) << i

def solve(invalid_count: int):
    num_above = 0
    num_left = 0
    for row in [True, False]:
        data = row_grids if row else col_grids
        for i, grid in enumerate(data):
            for j in range(len(grid) - 1):
                invalid_lines = 0
                for k in range(len(grid)):
                    left_side = j - k
                    right_side = j + 1 + k
                    if left_side < 0 < len(grid) <= right_side:
                        break
                    if 0 <= left_side < right_side < len(grid):
                        invalid_lines += bit_count(grid[left_side] ^ grid[right_side])

                if invalid_lines == invalid_count:
                    if row:
                        num_above += j + 1
                        #print(i + 1, j + 1, "row")
                    else:
                        num_left += j + 1
                        #print(i + 1, j + 1, "col")

    print(num_left + 100 * num_above)

solve(0)
solve(1)