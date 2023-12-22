from shared import *

INPUT_DATA = [parse("{:d},{:d},{:d}~{:d},{:d},{:d}", x) for x in INPUT_DATA]

class Block:
    def __init__(self, id, data):
        self.id = id
        x1, y1, z1, x2, y2, z2 = data

        self.min = (x1, y1, z1)
        self.max = (x2, y2, z2)
        self.width = abs(x2 - x1)
        self.height = abs(y2 - y1)
        self.depth  = abs(z2 - z1)

        self.supported_by = set()
        self.supports     = set()

    def overlaps(self, other: "Block", offset: Tuple[int, int, int]):
        return len(self.occupied(offset) & other.occupied()) > 0

    @property
    def xrange(self):
        return range(self.min[0], self.max[0] + 1)

    @property
    def yrange(self):
        return range(self.min[1], self.max[1] + 1)

    @property
    def zrange(self):
        return range(self.min[2], self.max[2] + 1)

    def occupied(self, offset: Tuple[int, int, int] = (0, 0, 0)):
        return set((x + offset[0], y + offset[1], z + offset[2]) for x in self.xrange for y in self.yrange for z in self.zrange)

    def __repr__(self):
        return f"{self.id} - {self.min} | {self.max}"

    def chain(self):
        queue = deque([x for x in self.supports if len(x.supported_by) == 1])
        seen  = { self }
        count = 0
        while queue:
            current = queue.popleft()
            if current in seen: continue

            if len(current.supported_by & seen) != len(current.supported_by):
                continue

            count += 1
            seen.add(current)

            for x in current.supports:
                queue.append(x)

        return count

blocks = sorted([Block(i, x) for i, x in enumerate(INPUT_DATA)], key=lambda x: x.min[2])
occupied = set()
for block in blocks:
    for x in range(block.min[0], block.max[0] + 1):
        for y in range(block.min[1], block.max[1] + 1):
            for z in range(block.min[2], block.max[2] + 1):
                occupied.add((x, y, z))

movement = True
while movement:
    moved = False
    for i, block in enumerate(blocks):
        while block.min[2] > 1:
            seen = [((x, y, block.min[2] - 1) not in occupied, (x, y, block.min[2] - 1)) for x in block.xrange for y in block.yrange]
            if all([a for a, _ in seen]):
                occupied -= block.occupied()
                block.min = (*block.min[:-1], block.min[2] - 1)
                block.max = (*block.max[:-1], block.max[2] - 1)
                occupied.update(block.occupied())
                moved = True
            else:
                break
    movement = moved

for i, block in enumerate(blocks):
    for j, other in enumerate(blocks):
        if i == j: continue

        if block.overlaps(other, (0, 0, 1)):
            other.supported_by.add(block)
            block.supports.add(other)

part1 = 0
part2 = 0
for block in blocks:
    if len(block.supports) >= 0:
        if all([len(other.supported_by) > 1 for other in block.supports]):
            part1 += 1
    part2 += block.chain()

print(part1)
print(part2)
