from collections import deque, defaultdict

def getScore(NumPlayers, MaxMarble):
    nodes = deque([0])

    currentPlayer = 1
    scores = defaultdict(int)

    for i in range(1, MaxMarble + 1):
        if (i % 23) == 0:
            nodes.rotate(7)
            scores[currentPlayer] += i + nodes.pop()
            nodes.rotate(-1)
        else:
            nodes.rotate(-1)
            nodes.append(i)
        currentPlayer = (currentPlayer + 1) % NumPlayers

    return max(scores.values())

# Example inputs.
assert(getScore(9,  25)   == 32)
assert(getScore(10, 1618) == 8317)
assert(getScore(13, 7999) == 146373)
assert(getScore(17, 1104) == 2764)
assert(getScore(21, 6111) == 54718)
assert(getScore(30, 5807) == 37305)

from timeit import default_timer as timer
import re

with open("../input/day9.txt", 'r') as inputFile:
    data = inputFile.read()

values = re.findall(r'\d+', data)
maxPlayers = int(values[0])
lastMarble = int(values[1])

# Part 1
start = timer()
print("Part1:", getScore(maxPlayers, lastMarble))
end = timer()
print("Part 1 Time (s): {:}".format(end - start))

# Part 2
start = timer()
print("Part2:", getScore(maxPlayers, lastMarble * 100))
end = timer()
print("Part 2 Time (s): {:}".format(end - start))

