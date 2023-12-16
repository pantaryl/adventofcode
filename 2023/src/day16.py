from shared import *

INPUT_DATA = [x for x in INPUT_DATA]

grid = Grid(INPUT_DATA)

start_pos = OrderedComplex(-1, 0)
start_dir = OrderedComplex(1, 0)


def calc_energized(start_pos, start_dir):
    stack = [ [ (start_pos, start_dir) ] ]
    energized = set()
    DP = set()
    while stack:
        current = stack.pop()
        pos, dir = current[-1]

        if (pos, dir) in DP:
            continue

        DP.add((pos, dir))
        energized.add(pos)

        next = pos + dir
        if next in grid.keys():
            next_type = grid[next]

            if next_type == "|":
                if int(dir.imag) == 0:
                    stack.append(current + [(next, OrderedComplex(0, -1))])
                    stack.append(current + [(next, OrderedComplex(0,  1))])
                else:
                    stack.append(current + [(next, dir)])
            elif next_type == "-":
                if int(dir.real) == 0:
                    stack.append(current + [(next, OrderedComplex(-1, 0))])
                    stack.append(current + [(next, OrderedComplex( 1, 0))])
                else:
                    stack.append(current + [(next, dir)])
            elif next_type == "/":
                if int(dir.real) == -1:
                    stack.append(current + [(next, OrderedComplex(0, 1))])
                elif int(dir.real) == 1:
                    stack.append(current + [(next, OrderedComplex(0, -1))])
                elif int(dir.imag) == -1:
                    stack.append(current + [(next, OrderedComplex(1, 0))])
                else:
                    stack.append(current + [(next, OrderedComplex(-1, 0))])
            elif next_type == "\\":
                if int(dir.real) == -1:
                    stack.append(current + [(next, OrderedComplex(0, -1))])
                elif int(dir.real) == 1:
                    stack.append(current + [(next, OrderedComplex(0, 1))])
                elif int(dir.imag) == -1:
                    stack.append(current + [(next, OrderedComplex(-1, 0))])
                else:
                    stack.append(current + [(next, OrderedComplex(1, 0))])
            else:
                stack.append(current + [(next, dir)])

    energized.remove(start_pos)
    return len(energized)

print(calc_energized(OrderedComplex(-1, 0), OrderedComplex(1, 0)))

energized = set()
for x in grid.x_range:
    energized.add(calc_energized(OrderedComplex(x, -1), OrderedComplex(0, 1)))
    energized.add(calc_energized(OrderedComplex(x, grid.height), OrderedComplex(0, -1)))
for y in grid.y_range:
    energized.add(calc_energized(OrderedComplex(-1, y), OrderedComplex(1, 0)))
    energized.add(calc_energized(OrderedComplex(grid.width, y), OrderedComplex(-1, 0)))

print(max(energized))
    