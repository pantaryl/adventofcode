from shared import *


# Input data is in INPUT_DATA.
grid = squareGridFromChars(INPUT_DATA)

symbols = set()
for pos, val in grid.items():
    if val.isdigit() is False and val != ".":
        symbols.add(pos)

numbers = set()
for symbol_pos in symbols:
    for dir in getAllSquareNeighbors():
        neighbor = symbol_pos + dir
        if neighbor in grid:
            if grid[neighbor].isdigit():
                start = neighbor
                while start - 1 in grid:
                    if grid[start - 1].isdigit():
                        start = start - 1
                    else:
                        break
                number = int(grid[start])
                while start + 1 in grid:
                    if grid[start + 1].isdigit():
                        number *= 10
                        number += int(grid[start + 1])
                        start += 1
                    else:
                        break

                numbers.add((start, number))

print(sum([x[1] for x in numbers]))
gears = set()
for symbol_pos in symbols:
    could_be_gear = grid[symbol_pos] == "*"
    if not could_be_gear: continue

    neighbor_numbers = set()
    for dir in getAllSquareNeighbors():
        neighbor = symbol_pos + dir
        if neighbor in grid:
            if grid[neighbor].isdigit():
                start = neighbor
                while start - 1 in grid:
                    if grid[start - 1].isdigit():
                        start = start - 1
                    else:
                        break
                number = int(grid[start])
                while start + 1 in grid:
                    if grid[start + 1].isdigit():
                        number *= 10
                        number += int(grid[start + 1])
                        start += 1
                    else:
                        break
                neighbor_numbers.add((start, number))

    if len(neighbor_numbers) == 2:
        neighbor_numbers = list([x[1] for x in neighbor_numbers])
        gears.add((symbol_pos, neighbor_numbers[0] * neighbor_numbers[1]))

print(sum([x[1] for x in gears]))


