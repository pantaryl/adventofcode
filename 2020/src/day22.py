from collections import defaultdict, deque
from helpers import memoize
from copy import deepcopy
from enum import Enum
from typing import Tuple
import os
from math_utils import *

# Complex numbers in Python! == i + nj (x + ny), good for coordinates
# complex*+imaginary to rotate left/ccw, complex*-imaginary to rotate right/cw
# For example:
# Rotate CCW by 270 degrees:
#    val *= complex(0, 1) ** 3 [each power represents 90 degrees]

with open(f"../input/{os.path.splitext(os.path.basename(__file__))[0]}.txt", 'r') as inputFile:
    data = [x.rstrip() for x in inputFile.readlines()]
    #data = [int(x) for x in data]

data = "\n".join(data).split("\n\n")

player1 = deque([int(x.rstrip()) for x in data[0].split("\n")[1:]])
player2 = deque([int(x.rstrip()) for x in data[1].split("\n")[1:]])

while player1 and player2:
    a = player1.popleft()
    b = player2.popleft()

    if a > b:
        winner = player1, a, b
    else:
        winner = player2, b, a
    winner[0].append(winner[1])
    winner[0].append(winner[2])

print(sum(i * x for i, x in enumerate(list(player1)[::-1] if player1 else list(player2)[::-1], 1)))

verbose   = False
gameCount = 1
def solve(player1: list, player2: list, depth) -> Tuple[int, list]:
    if verbose: print(f"=== Game {depth} ===")
    if verbose: print()
    round = 1
    memo = {}
    while player1 and player2:
        if verbose: print(f"-- Round {round} (Game {depth}) --")

        key = (",".join([str(x) for x in player1]), ",".join([str(x) for x in player2]))
        if verbose: print(f"Player 1's deck: {key[0]}")
        if verbose: print(f"Player 2's deck: {key[1]}")
        if key in memo:
            return 1, player1
        else:
            memo[key] = True

        a = player1.pop(0)
        b = player2.pop(0)
        if verbose: print(f"Player 1 plays: {a}")
        if verbose: print(f"Player 2 plays: {b}")

        if a <= len(player1) and b <= len(player2):
            if verbose: print("Playing a sub-game to determine the winner...")
            if verbose: print()
            global gameCount
            gameCount += 1
            winner = solve(player1[:a], player2[:b], gameCount)
        elif a > b:
            winner = 1, player1
        else:
            assert(b > a)
            winner = 2, player2

        if winner[0] == 1:
            if verbose: print(f"Player 1 wins round {round} of game {depth}!")
            player1.append(a)
            player1.append(b)
        else:
            assert(winner[0] == 2)
            if verbose: print(f"Player 2 wins round {round} of game {depth}!")
            player2.append(b)
            player2.append(a)

            if verbose: print()
        round += 1
        if verbose: print(f"The winner of game {depth} is player {1 if player1 else 2}!")
    return 1 if player1 else 2, player1 if player1 else player2

player1 = [int(x.rstrip()) for x in data[0].split("\n")[1:]]
player2 = [int(x.rstrip()) for x in data[1].split("\n")[1:]]
_, winner = solve(player1, player2, gameCount)

if verbose: print(_, winner)
print(sum(i * x for i, x in enumerate(winner[::-1], 1)))