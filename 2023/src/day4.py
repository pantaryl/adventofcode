from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]
points = []
for line in INPUT_DATA:
    front, back = line.split(" | ")
    winners = set([int(x) for x in front.split(":")[1].split(" ") if x != ""])
    have    = set([int(x) for x in back.split(" ") if x != ""])

    matches = winners.intersection(have)
    if len(matches) > 0:
        points.append(len(matches) - 1)
    else:
        points.append(None)

part1 = 0
for i, matches in enumerate(points):
    if matches is not None:
        part1 += 2 ** matches
print(part1)

part2_counts = defaultdict(int)
for i, matches in enumerate(points):
    part2_counts[i] += 1
    if matches is not None:
        for j in range(matches + 1):
            part2_counts[i+1+j] += part2_counts[i]

part2 = sum(part2_counts.values())
print(part2)
