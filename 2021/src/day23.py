from shared import *

# Input data is in INPUT_DATA.
#INPUT_DATA = [int(x) for x in INPUT_DATA]

costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

room1T, room2T, room3T, room4T = tuple(parse.parse('###{}#{}#{}#{}###', INPUT_DATA[2]).fixed)
room1B, room2B, room3B, room4B = tuple(parse.parse('  #{}#{}#{}#{}#', INPUT_DATA[3]).fixed)

rooms = [2, 4, 6, 8]
hallway = [0, 1, 3, 5, 7, 9, 10]
destinations = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8,

    2: 'A',
    4: 'B',
    6: 'C',
    8: 'D',
}

def heuristic(neighbor):
    global depth
    score = 0

    for i, val in enumerate(neighbor):
        for char in val:
            if char != '.':
                destCol = destinations[char]
                score += costs[char] * (abs(destCol - i) + (depth - neighbor[destCol].count(char)))

    return score

def scoreFunc(grid, current, neighbor):
    char      = '.'
    toIndex   = -1
    fromIndex = -1
    depth     = 0
    for i, val in enumerate(current):
        if val != neighbor[i]:
            for j, charVal in enumerate(val):
                if charVal != neighbor[i][j]:
                    if charVal != '.':
                        fromIndex = i
                        char = charVal
                    else:
                        toIndex = i
                        char = neighbor[i][j]
                    if i in rooms:
                        depth = max(depth, j + 1)

    score = costs[char] * (abs(toIndex - fromIndex) + depth)
    return score

@memoize
def adjFunc(data):
    global depth

    grid, current = data

    def isRoomDone(data):
        if isinstance(data, str):
            destCol = destinations[data]
        else:
            assert(isinstance(data, int))
            destCol = data
        char = destinations[destCol]
        return current[destCol].count(char) == depth

    def isRoomSafe(data):
        if isinstance(data, str):
            destCol = destinations[data]
        else:
            assert(isinstance(data, int))
            destCol = data
        char = destinations[destCol]
        return (current[destCol].count(char) + current[destCol].count('.')) == depth

    def isRoomEmpty(idx):
        return current[idx].count('.') == depth

    def isPathEmpty(curIdx, destIdx):
        minIdx = min(curIdx, destIdx)
        maxIdx = max(curIdx, destIdx) + 1
        return all(space == '.' for idx in range(minIdx, maxIdx) for space in current[idx] if idx not in rooms and idx != curIdx)

    neighbors = []

    for idx, space in enumerate(current):
        if idx in hallway and space.count('.') == 0:
            assert(len(space) == 1)
            assert(not isRoomDone(space))

            # This space has an amphipod that needs to go into a room.
            if isRoomSafe(space):
                destCol  = destinations[space]

                if isPathEmpty(idx, destCol):
                    # If the path isn't empty, we can't move into the room.
                    newDepth = current[destCol].count('.')

                    newState = list(current)
                    newState[idx]     = '.'
                    newState[destCol] = ''
                    for charIdx, newChar in enumerate(current[destCol]):
                        newState[destCol] += newChar if charIdx != (newDepth - 1) else space

                    neighbors.append(tuple(newState))
        elif idx in rooms:
            assert(len(space) == depth)
            if isRoomDone(idx):
                # If this room is complete, it can have no valid moves.
                continue
            if isRoomSafe(idx):
                # This room only contains characters that belong here.
                continue
            if isRoomEmpty(idx):
                # There is nothing to move here. Continue on.
                continue

            # Get the top-most space.
            existingDepth = space.count('.')
            char = space[existingDepth]

            for newIdx in hallway:
                if isPathEmpty(idx, newIdx):
                    newState = list(current)
                    newState[idx] = ""
                    for charIdx, newChar in enumerate(space):
                        newState[idx] += newChar if charIdx != existingDepth else '.'
                    newState[newIdx] = char

                    neighbors.append(tuple(newState))

    return neighbors

# Part 1
depth = 2
state = [
    '.',
    '.',
    room1T + room1B,
    '.',
    room2T + room2B,
    '.',
    room3T + room3B,
    '.',
    room4T + room4B,
    '.',
    '.',
]
goal = [
    '.',
    '.',
    'AA',
    '.',
    'BB',
    '.',
    'CC',
    '.',
    'DD',
    '.',
    '.',
]
assert(len(state) == 11)

part1 = list(aStar(None, tuple(state), tuple(goal), heuristic, adjFunc, scoreFunc))
score = sum(scoreFunc(None, x, y) for x, y in zip(part1[0:], part1[1:]))
print(score)
# Part 2
depth = 4
state = [
    '.',
    '.',
    room1T + 'DD' + room1B,
    '.',
    room2T + 'CB' + room2B,
    '.',
    room3T + 'BA' + room3B,
    '.',
    room4T + 'AC' + room4B,
    '.',
    '.',
]
goal = [
    '.',
    '.',
    'AAAA',
    '.',
    'BBBB',
    '.',
    'CCCC',
    '.',
    'DDDD',
    '.',
    '.',
]
assert(len(state) == 11)

part2 = list(aStar(None, tuple(state), tuple(goal), heuristic, adjFunc, scoreFunc))
score = sum(scoreFunc(None, x, y) for x, y in zip(part2[0:], part2[1:]))
print(score)