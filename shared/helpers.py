from typing import Dict, List, Union
import sys

FILLED_CHAR = '▮'
EMPTY_CHAR  = ' '

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

def getStringFromGrid(grid: dict, set: str, printGrid: bool = False) -> str:
    CHARS = {
        '011010011001111110011001': 'A',
        '111010011110100110011110': 'B',
        '011010011000100010010110': 'C',
        '111010011001100110011110': 'D',
        '111110001110100010001111': 'E',
        '111110001110100010001000': 'F',
        '011010011000101110010111': 'G',
        '100110011111100110011001': 'H',
        '111001000100010001001110': 'I',
        '001100010001000110010110': 'J',
        '100110101100110010101001': 'K',
        '100010001000100010001111': 'L',
        '100111111111100110011001': 'M',
        '100111011101101110111001': 'N',
        '011010011001100110010110': 'O',
        '111010011001111010001000': 'P',
        '011010011001100101100001': 'Q',
        '111010011001111010101001': 'R',
        '011010010100001010010110': 'S',
        '111001000100010001000100': 'T',
        '100110011001100110010110': 'U',
        '100110011001100101100110': 'V',
        '100110011001111111111001': 'W',
        '100110010110011010011001': 'X',
        '101010101010010001000100': 'Y',
        '111100010010010010001111': 'Z',
        '011010111011110111010110': '0',
        '010011000100010001001110': '1',
        '011010010001001001001111': '2',
        '011010010010000110010110': '3',
        '100110011111000100010001': '4',
        '111110001110000100011110': '5',
        '011110001110100110010110': '6',
        '111100010001000100010001': '7',
        '011010010110100110010110': '8',
        '011010010111000100010001': '9',
    }

    minX = int(min([x.real if val == set else  sys.maxsize for x, val in grid.items()]))
    maxX = int(max([x.real if val == set else -sys.maxsize for x, val in grid.items()]))
    minY = int(min([y.imag if val == set else  sys.maxsize for y, val in grid.items()]))
    maxY = int(max([y.imag if val == set else -sys.maxsize for y, val in grid.items()]))
    # print(f"min({minX}, {minY}) -> max({maxX}, {maxY})")

    assert(maxY - minY + 1 == 6)

    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            pos = complex(x, y)
            val = grid[pos]
            val = FILLED_CHAR if val == set else EMPTY_CHAR
            print(val, end='')
        print()
    print(flush=True)

    # Standard AoC Font is 4x6 grid.
    charNum = 0
    offset  = minX
    errors  = []
    while offset + 3 <= maxX:
        data = "".join(['1' if grid[complex(x, y)] == set else '0' for y in range(minY, maxY + 1) for x in range(offset, offset+4)])
        if data in CHARS:
            print(CHARS[data], end='')
            charNum += 1
        else:
            errors.append(f"Faulting char #{charNum} (start from idx0) with data: {data}")
        offset += 5
    print(flush=True)

    if errors:
        print("\033[1;31;48mERROR:")
        for error in errors:
            print(f"\033[1;31;48m  {error}", flush=True)
        exit(-1)
