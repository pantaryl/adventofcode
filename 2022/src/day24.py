from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x[1:-1] for x in INPUT_DATA[1:-1]]

grid = squareGridFromChars(INPUT_DATA)
blizzards = tuple([(pos, value) for pos, value in grid.items() if value in ['v', '>', '^', '<']])

top    = 0
left   = 0
bottom = max([int(pos.imag) + 1 for pos, _ in grid.items()])
right  = max([int(pos.real) + 1 for pos, _ in grid.items()])

player   = complex(0, -1)
exit_pos = complex(right - 1, bottom)
grid[player]   = '.'
grid[exit_pos] = '.'

movement = {
    'v': lambda x, minute: complex(x.real, (int(x.imag) + minute) % bottom),
    '^': lambda x, minute: complex(x.real, (int(x.imag) - minute) % bottom),
    '>': lambda x, minute: complex((int(x.real) + minute) % right, x.imag),
    '<': lambda x, minute: complex((int(x.real) - minute) % right, x.imag),
}
def heuristic(neighbor):
    minute, neighbor_pos, to_start, to_exit = neighbor
    if to_start is False:
        return minute + \
               manhattanDistance(neighbor_pos, player) + \
               manhattanDistance(player, exit_pos)
    else:
        assert(to_start)
        return minute + manhattanDistance(neighbor_pos, exit_pos)

memo = {}
def adjFunc(data):
    orig_grid, current = data
    current_minute, current_pos, to_start, to_exit = current

    if (current_minute + 1) in memo:
        new_blizzards, new_blizzard_locs = memo[current_minute + 1]
    else:
        orig_blizzards = [(pos, value) for pos, value in orig_grid.items() if value not in ['.', '#']]
        new_blizzards = []
        for pos, dir in orig_blizzards:
            new_blizzards.append((movement[dir](pos, current_minute + 1), dir))
        new_blizzard_locs = {pos for pos, _ in new_blizzards}
        memo[current_minute + 1] = (new_blizzards, new_blizzard_locs)

    neighbors = []
    for dir in getOrthogonalSquareNeighbors():
        if current_pos + dir in new_blizzard_locs:
            continue
        elif to_start is False and current_pos + dir == player:
            neighbors.append((current_minute + 1, OrderedComplex(current_pos + dir), True, False))
            #print("Got back to the start!", current_minute + 1)
        elif to_start and to_exit is False and current_pos + dir == exit_pos:
            neighbors.append((current_minute + 1, OrderedComplex(current_pos + dir), True, True))
            #print("Got to the exit again!", current_minute + 1)
        elif orig_grid.get(current_pos + dir, '#') == '#':
            continue
        else:
            neighbors.append((current_minute + 1, OrderedComplex(current_pos + dir), to_start, to_exit))

    if current_pos not in new_blizzard_locs:
        neighbors.append((current_minute + 1, OrderedComplex(current_pos), to_start, to_exit))
    return neighbors
def scoreFunc(grid, current, neighbor):
    current_minute, current_pos, _, __ = current
    next_minute, neighbor_pos, to_start, to_exit = neighbor

    if to_start is False:
        return next_minute + \
               manhattanDistance(neighbor_pos, player) + \
               manhattanDistance(player, exit_pos)
    else:
        assert(to_start)
        return next_minute + manhattanDistance(neighbor_pos, exit_pos)
def metGoalFunc(current, goal):
    _, current_pos, to_start, to_exit = current
    return to_start and to_exit and current_pos == goal

# Part 1
to_end_path = aStar(grid,
                    (0, player, True, False),
                    exit_pos,
                    heuristic,
                    adjFunc,
                    scoreFunc,
                    metGoalFunc=metGoalFunc)
to_end_path_minute = len(to_end_path) - 1
print(to_end_path_minute)

# Part 2
to_end_path_again = aStar(grid,
                          (to_end_path_minute, exit_pos, False, False),
                          exit_pos,
                          heuristic,
                          adjFunc,
                          scoreFunc,
                          metGoalFunc=metGoalFunc)
to_end_path_again_minute = to_end_path_minute + len(to_end_path_again) - 1
print(to_end_path_again_minute)