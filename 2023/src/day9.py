from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [[int(y) for y in x.split(" ")] for x in INPUT_DATA]

part1_total = 0
part2_total = 0
for line in INPUT_DATA:
    results = [ list(line) ]
    while True:
        new_list = []
        for i in range(1, len(results[-1])):
            new_list.append(results[-1][i] - results[-1][i - 1])
        results.append(new_list)

        if all(x == 0 for x in new_list):
            break

    part1 = deepcopy(results)
    part1[-1].append(0)
    part1 = list(reversed(part1))

    part2 = deepcopy(results)
    part2[-1].insert(0, 0)
    part2 = list(reversed(part2))

    assert len(part1) == len(part2)
    for level in range(len(part1) - 1):
        next_level = level + 1
        part1[next_level].append(part1[next_level][-1] + part1[level][-1])
        part2[next_level].insert(0, part2[next_level][0] - part2[level][0])

    part1_total += part1[-1][-1]
    part2_total += part2[-1][0]

print(part1_total)
print(part2_total)