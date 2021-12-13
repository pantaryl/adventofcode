from shared import *

# Input data is in INPUT_DATA.
#INPUT_DATA = [int(x) for x in INPUT_DATA]

grid  = defaultdict(lambda: None)
folds = []
fold  = None
for line in INPUT_DATA:
    if line == "":
        fold = True
    elif fold:
        dir, num = tuple(parse.parse("fold along {}={:d}", line).fixed)
        folds.append((dir, num))
        pass
    else:
        x, y = tuple(parse.parse("{:d},{:d}", line).fixed)
        grid[complex(x, y)] = 'X'

# Part 1
def fold(grid, dir, num):
    if dir == 'y':
        minY = 0
        maxY = num * 2
        minX = int(min([x.real for x in grid.keys()]))
        maxX = int(max([x.real for x in grid.keys()]))

        for y in range(num + 1, maxY + 1):
            for x in range(minX, maxX + 1):
                pos = complex(x, y)
                if pos in grid:
                    val = grid[pos]
                    newPos = complex(x, maxY - y)
                    grid[newPos] = 'X' if val == 'X' or grid[newPos] == 'X' else None
                    grid.pop(pos)

        for x in range(minX, maxX + 1):
            pos = complex(x, num)
            if pos in grid: grid.pop(pos)
    elif dir == 'x':
        minY = int(min([y.imag for y in grid.keys()]))
        maxY = int(max([y.imag for y in grid.keys()]))
        minX = 0
        maxX = num * 2

        for x in range(num + 1, maxX + 1):
            for y in range(minY, maxY + 1):
                pos = complex(x, y)
                if pos in grid:
                    val = grid[pos]
                    newPos = complex(maxX - x, y)
                    grid[newPos] = 'X' if val == 'X' or grid[newPos] == 'X' else None
                    grid.pop(pos)

        for y in range(minY, maxY + 1):
            pos = complex(num, y)
            if pos in grid: grid.pop(pos)

fold(grid, folds[0][0], folds[0][1])
#printGrid(grid)

count = 0
for _, val in grid.items():
    count += val == 'X'

print(count)

# Part 2
for dir, num in folds[1:]:
    fold(grid, dir, num)

getStringFromGrid(grid, 'X', printGrid=True)
