from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]

grid = squareGridFromChars(INPUT_DATA)

start = [pos for pos, value in grid.items() if value == "S"][0]
end   = [pos for pos, value in grid.items() if value == "E"][0]

grid[start] = 'a'
grid[end]   = 'z'

def adjFunc(x):
    cur_grid = x[0]
    cur_pos  = x[1]

    value = cur_grid[cur_pos]

    for dir in getOrthogonalSquareNeighbors():
        new_pos = cur_pos + dir
        if new_pos in cur_grid and (ord(cur_grid[new_pos]) <= ord(value) or ord(value) + 1 == ord(cur_grid[new_pos])):
            yield new_pos


# Part 1
path = aStar(grid, start, end, lambda x: 0, adjFunc, lambda x, y, z: 1)
print(len(path) - 1)

# Part 2
possible_starts = [pos for pos, value in grid.items() if value == 'a']
lengths = []
for i, new_start in enumerate(possible_starts):
    path = aStar(grid, new_start, end, lambda x: 0, adjFunc, lambda x, y, z: 1)
    if path:
        lengths.append(len(path) - 1)

print(sorted(lengths)[0])