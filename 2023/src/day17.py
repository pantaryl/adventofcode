from shared import *

grid = Grid(INPUT_DATA, True)

start = grid.tl
end   = grid.br

def heuristic(state):
    return 0

DP = set()
def adjFunc(index):
    _grid, state = index
    current, _dir, length = state

    if state in DP:
        return []
    DP.add(state)

    possible_dirs = {_dir, _dir.rot(1), _dir.rot(-1) }

    neighbors = []
    for new_dir in possible_dirs:
        neighbor = current + new_dir
        new_length = 1 if _dir != new_dir else length + 1

        if neighbor in grid and new_length <= 3:
            neighbors.append((neighbor, new_dir, new_length))
    return neighbors

def scoreFunc(_grid, _current, _neighbor):
    return _grid[_neighbor[0]]

def metGoalFunc(_current, _goal):
    current = _current[0]

    return current == _goal

print(sum([grid[x[0]] for i, x in
           enumerate(aStar(grid, (start, OrderedComplex(1, 0), 0), end, heuristic, adjFunc, scoreFunc, metGoalFunc))
           if i != 0]))

DP = set()
def adjFunc2(index):
    _grid, state = index

    if state in DP:
        return []
    DP.add(state)

    current, _dir, length = state
    if length < 4:
        possible_dirs = { _dir }
    else:
        possible_dirs = {_dir, _dir.rot(1), _dir.rot(-1)}

    for new_dir in possible_dirs:
        neighbor = current + new_dir
        new_length = 1 if _dir != new_dir else length + 1

        if neighbor in grid and new_length <= 10:
            yield (neighbor, new_dir, new_length)

def metGoalFunc2(_current, _goal):
    current = _current[0]

    return current == _goal and _current[2] >= 4

part2 = aStar(grid, (start, OrderedComplex(1, 0), 0), end, heuristic, adjFunc2, scoreFunc, metGoalFunc2)
print(sum([grid[x[0]] for i, x in
           enumerate(part2)
           if i != 0]))