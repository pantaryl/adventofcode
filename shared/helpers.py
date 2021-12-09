from typing import Dict, List, Union

def memoize(f):
    memo = {}
    def helper(index, *args):
        if index not in memo:
            memo[index] = f(index, *args)
        return memo[index]
    return helper


class LLNode:
    def __init__(self, val):
        self.val  = val
        self.next = None


def squareGridFromChars(input: List[str], isInts=False) -> Dict[complex, Union[int, str]]:
    grid = {}

    for j, line in enumerate(input):
        for i, char in enumerate(line):
            grid[complex(i, j)] = int(char) if isInts else char

    return grid

def getOrthogonalSquareNeighbors() -> List[complex]:
    return [
        0-1j,  # up
        0+1j,  # down
        -1+0j, # left
        1+0j   # right
    ]

def getAllSquareNeighbors() -> List[complex]:
    return [
        -1 - 1j, # up-left
         0 - 1j, # up
         1 - 1j, # up-right
        -1 + 0j, # left
         1 + 0j, # right
        -1 + 1j, # down-left
         0 + 1j, # down
         1 + 1j, # down-right
    ]
