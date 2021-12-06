from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [int(x) for x in INPUT_DATA[0].split(",")]

# Part 1
counts = defaultdict(int)
for i in range(0, 9):
    counts[i] = INPUT_DATA.count(i)

for i in range(0, 256):
    counts['temp8'] = counts[8]
    counts['temp6'] = counts[6]
    counts[8]       = counts[0]
    counts[6]       = counts[0] + counts[7]

    counts[0]       = counts[1]
    counts[1]       = counts[2]
    counts[2]       = counts[3]
    counts[3]       = counts[4]
    counts[4]       = counts[5]
    counts[5]       = counts['temp6']
    counts[7]       = counts['temp8']

    if i == 79 or i == 255:
        del counts['temp6']
        del counts['temp8']
        print(sum([x for _, x in counts.items()]))
