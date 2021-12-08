from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [(x.split(" | ")[0].split(), x.split(" | ")[1].split()) for x in INPUT_DATA]

# Part 1
count = 0
for line in INPUT_DATA:
    output = line[1]
    for item in output:
        if len(item) in [2, 4, 3, 7]:
            count += 1

print(count)

# Part 2
class SevenSegment:
    def __init__(self):
        self.data = [None for i in range(7)]

    def setSegment(self, idx):
        self.data[idx] = True

    @property
    def top(self):
        return self.data[0]
    @property
    def tl(self):
        return self.data[1]
    @property
    def tr(self):
        return self.data[2]
    @property
    def mid(self):
        return self.data[3]
    @property
    def bl(self):
        return self.data[4]
    @property
    def br(self):
        return self.data[5]
    @property
    def bot(self):
        return self.data[6]

    @property
    def type(self):
        if self.top and self.tl and self.tr and self.mid and self.bl and self.br and self.bot:
            return 8
        elif self.top and self.tl and self.tr and self.bl and self.br and self.bot:
            return 0
        elif self.top and self.tl and self.mid and self.bl and self.br and self.bot:
            return 6
        elif self.top and self.tl and self.tr and self.mid and self.br and self.bot:
            return 9
        elif self.top and self.tr and self.mid and self.bl and self.bot:
            return 2
        elif self.top and self.tr and self.mid and self.br and self.bot:
            return 3
        elif self.top and self.tl and self.mid and self.br and self.bot:
            return 5
        elif self.tl and self.tr and self.mid and self.br:
            return 4
        elif self.top and self.tr and self.br:
            return 7
        elif self.tr and self.br:
            return 1
        else:
            return None

# Segment Top      (0) is in 8 numbers.
# Segment TopLeft  (1) is in 6 numbers.
# Segment TopRight (2) is in 8 numbers.
# Segment Middle   (3) is in 7 numbers.
# Segment BotLeft  (4) is in 4 numbers.
# Segment BotRight (5) is in 9 numbers.
# Segment Bottom   (6) is in 7 numbers.

part2 = 0
for line in INPUT_DATA:
    first = sorted(line[0], key=lambda x: len(x))
    counts = [(char, sum([item.count(char) for item in first])) for char in 'abcdefg']
    found = {}
    for key, val in counts:
        if val == 9:
            found[key] = 5
        elif val == 6:
            found[key] = 1
        elif val == 4:
            found[key] = 4
        elif val == 7 and any([True if key not in x else False for x in first[6:9]]):
            # first[6:9] are all of the 6 segment cases, and only one of them is missing Segment 3.
            found[key] = 3
        elif val == 7:
            # If we didn't already find Segment 3, this must be Segment 6.
            found[key] = 6
        elif val == 8 and key not in first[0]:
            # Segment 0 (Top) is not in the Number 1.
            found[key] = 0
        elif val == 8:
            # If we didn't already find Segment 0, this must be Segment 2.
            found[key] = 2

    outputs = 0
    for item in line[1]:
        segments = SevenSegment()
        for char in item:
            segments.setSegment(found[char])
        outputs = (outputs * 10) + segments.type
    part2 += outputs

print(part2)