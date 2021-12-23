from typing import *
from .classes import OrderedComplex
import sys

# Complex numbers in Python! == i + nj (x + ny), good for coordinates
# complex*+imaginary to rotate left/ccw, complex*-imaginary to rotate right/cw
# For example:
# Rotate CCW by 270 degrees:
#    val *= complex(0, 1) ** 3 [each power represents 90 degrees]

FILLED_CHAR = '▮'
EMPTY_CHAR  = ' '

def squareGridFromChars(input: List[str],
                        isInts=False,
                        conversionDict: dict = None,
                        toSetOnValue = None) -> Dict[complex, Union[int, str]]:
    if toSetOnValue:
        grid = set()
    else:
        grid = {}

    for j, line in enumerate(input):
        for i, char in enumerate(line):
            if toSetOnValue:
                if char == toSetOnValue:
                    grid.add(OrderedComplex(i, j))
            elif conversionDict:
                grid[OrderedComplex(i, j)] = conversionDict[char]
            elif isInts:
                grid[OrderedComplex(i, j)] = int(char)
            else:
                grid[OrderedComplex(i, j)] = char

    return grid

def getOrthogonalSquareNeighbors() -> List[OrderedComplex]:
    return [
        OrderedComplex(0-1j),  # up
        OrderedComplex(0+1j),  # down
        OrderedComplex(-1+0j), # left
        OrderedComplex(1+0j)   # right
    ]

def getAllSquareNeighbors() -> List[OrderedComplex]:
    return [
        OrderedComplex(-1 - 1j), # up-left
        OrderedComplex( 0 - 1j), # up
        OrderedComplex( 1 - 1j), # up-right
        OrderedComplex(-1 + 0j), # left
        OrderedComplex( 1 + 0j), # right
        OrderedComplex(-1 + 1j), # down-left
        OrderedComplex( 0 + 1j), # down
        OrderedComplex( 1 + 1j), # down-right
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
        '100110101100101010101001': 'K',
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