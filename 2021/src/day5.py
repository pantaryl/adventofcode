from shared import *

# Input data is in INPUT_DATA.
# INPUT_DATA = [int(x) for x in INPUT_DATA]

class Line:
    def __init__(self, start: complex, end: complex):
        self.start: complex
        self.start = start
        self.end: complex
        self.end   = end

    @property
    def vertical(self) -> bool:
        return self.start.real == self.end.real

    @property
    def horiz(self) -> bool:
        return self.start.imag == self.end.imag

    def simple_iterator(self):
        if self.horiz:
            large = max(int(self.start.real), int(self.end.real))
            small = min(int(self.start.real), int(self.end.real))
            for i in range(small, large + 1):
                yield i, int(self.start.imag)
        elif self.vertical:
            large = max(int(self.start.imag), int(self.end.imag))
            small = min(int(self.start.imag), int(self.end.imag))
            for i in range(small, large + 1):
                yield int(self.start.real), i
        else:
            x = int(self.start.real)
            y = int(self.start.imag)

            yield x, y

            while x != int(self.end.real) and y != int(self.end.imag):
                x += 1 if self.start.real < self.end.real else -1
                y += 1 if self.start.imag < self.end.imag else -1
                yield x, y

lines = []
for line in INPUT_DATA:
    startx, starty, endx, endy = tuple(parse.parse("{:d},{:d} -> {:d},{:d}", line).fixed)

    lines.append(Line(complex(startx, starty), complex(endx, endy)))

def count(finished_map):
    count = 0
    for _, data in finished_map.items():
        if data >= 2: count += 1
    return count

# Part 1
matching_lines = [line for line in lines if line.vertical or line.horiz]
map = defaultdict(int)

for line in matching_lines:
    for x, y in line.simple_iterator():
        map[(x, y)] += 1

print(count(map))

# Part 2
map = defaultdict(int)
for line in lines:
    for x, y in line.simple_iterator():
        map[(x, y)] += 1

print(count(map))
