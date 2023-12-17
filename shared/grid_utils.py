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

def manhattanDistance(start: complex, end:complex):
    return abs(int(start.real) - int(end.real)) + abs(int(start.imag) - int(end.imag))

class Grid:
    def __init__(self,
                 input: List[str],
                 isInts=False,
                 conversionDict: dict = None,
                 toSetOnValue = None):
        self.data : Union[Dict[complex, Any], Set[Any]] = {}

        self.is_set = toSetOnValue

        if toSetOnValue:
            self.data = set()
        else:
            self.data = {}

        for j, line in enumerate(input):
            for i, char in enumerate(line):
                if toSetOnValue:
                    if char == toSetOnValue:
                        self.data.add(OrderedComplex(i, j))
                elif conversionDict:
                    if conversionDict[char] is not None:
                        self.data[OrderedComplex(i, j)] = conversionDict[char]
                elif isInts:
                    self.data[OrderedComplex(i, j)] = int(char)
                else:
                    self.data[OrderedComplex(i, j)] = char

        self.width  = len(input[0])
        self.height = len(input)

        self.x_range = range(self.width)
        self.y_range = range(self.height)

    @property
    def tl(self):
        return OrderedComplex(0, 0)

    @property
    def br(self):
        return OrderedComplex(self.width - 1, self.height -1)

    def print(self,
              char_table: Optional[Dict[complex, str]],
              known: str = '#',
              empty: str = '.',
              known_pos: Optional[Set[complex]] = None,
              x_dim: Optional[Tuple[int, int]] = None,
              y_dim: Optional[Tuple[int, int]] = None):

        if known_pos is None:
            if self.is_set:
                known_pos = self.data
            else:
                known_pos = self.data.keys()

        if x_dim is None:
            x_dim = (min([int(x.real) for x in known_pos]), max([int(x.real) for x in known_pos]))
        if y_dim is None:
            y_dim = (min([int(x.imag) for x in known_pos]), max([int(x.imag) for x in known_pos]))

        for y in range(y_dim[0], y_dim[1] + 1):
            for x in range(x_dim[0], x_dim[1] + 1):
                pos = complex(x, y)
                if pos in known_pos:
                    if char_table is None:
                        print(known, end='')
                    else:
                        print(char_table[pos], end='')
                else:
                    if char_table and pos in char_table:
                        print(char_table[pos], end='')
                    else:
                        print(empty, end='')
            print()

    def rotate(self, dir: int):
        if self.is_set:
            raise Exception

        assert dir in (-1, 1)
        self.data = {complex(dir * (self.width - 1), 0) + (pos * complex(0, dir)): value for pos, value in self.items()}

    def __str__(self):
        if self.is_set: return str(self.data)

        return "".join([str(self.data[complex(x, y)]) for x in self.x_range for y in self.y_range])

    def __hash__(self):
        if self.is_set:
            raise Exception

        return hash(str(self))

    def __contains__(self, key):
        if self.is_set:
            raise Exception

        return key in self.data

    def __getitem__(self, key):
        if self.is_set:
            raise Exception

        return self.data[key]

    def __setitem__(self, key, value):
        if self.is_set:
            raise Exception

        self.data[key] = value

    def items(self):
        return self.data.items()

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

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
                if conversionDict[char] is not None:
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

def get_min_max(positions: List[complex]):
    x_dim = (min([int(x.real) for x in positions]), max([int(x.real) for x in positions]))
    y_dim = (min([int(x.imag) for x in positions]), max([int(x.imag) for x in positions]))

    return x_dim, y_dim

def grid_ranges(positions: Iterable[complex]):
    x_dim, y_dim = get_min_max(positions)
    return range(x_dim[0], x_dim[1] + 1), range(y_dim[0], y_dim[1] + 1)

def complex_to_int_tuple(pos: complex):
    return (int(pos.real), int(pos.imag))

def grid_to_hash(grid: Dict[complex, Any]):
    x_range, y_range = grid_ranges(grid.keys())
    return hash("".join([str(grid[complex(x, y)]) for x in x_range for y in y_range]))

def printSetGrid(known_pos: Set[complex],
                 char_table: Optional[Dict[complex, str]],
                 known:str = '#',
                 empty:str = '.',
                 x_dim: Optional[Tuple[int, int]] = None,
                 y_dim: Optional[Tuple[int, int]] = None):
    if x_dim is None:
        x_dim = (min([int(x.real) for x in known_pos]), max([int(x.real) for x in known_pos]))
    if y_dim is None:
        y_dim = (min([int(x.imag) for x in known_pos]), max([int(x.imag) for x in known_pos]))

    for y in range(y_dim[0], y_dim[1] + 1):
        for x in range(x_dim[0], x_dim[1] + 1):
            pos = complex(x, y)
            if pos in known_pos:
                if char_table is None:
                    print(known, end='')
                else:
                    print(char_table[pos], end='')
            else:
                if char_table and pos in char_table:
                    print(char_table[pos], end='')
                else:
                    print(empty, end='')
        print()

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
    #print(f"min({minX}, {minY}) -> max({maxX}, {maxY})")

    assert(maxY - minY + 1 == 6)

    if printGrid:
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