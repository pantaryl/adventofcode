from shared import *

# Input data is in INPUT_DATA.
# INPUT_DATA = [int(x) for x in INPUT_DATA]
template = INPUT_DATA[0]

rules = {}
for line in INPUT_DATA[2:]:
    orig, result = tuple(parse.parse("{} -> {}", line).fixed)
    rules[orig] = result

counts = defaultdict(int)
for rule, val in rules.items():
    counts[rule] += countSubstring(INPUT_DATA[0], rule)

charCounts = defaultdict(int)
for char in INPUT_DATA[0]:
    charCounts[char] += 1

for i in range(0, 40):
    for rule, count in counts.copy().items():
        val   = rules[rule]
        pairL = rule[0] + val
        pairR = val + rule[1]

        counts[pairL] += count
        counts[pairR] += count
        counts[rule]  -= count

        charCounts[val] += count

    if i == 9 or i == 39:
        most  = max([count for _, count in charCounts.items()])
        least = min([count for _, count in charCounts.items()])
        print(most - least)