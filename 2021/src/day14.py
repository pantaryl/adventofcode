from shared import *

# Input data is in INPUT_DATA.
# INPUT_DATA = [int(x) for x in INPUT_DATA]
template = INPUT_DATA[0]

rules = {}
for line in INPUT_DATA[2:]:
    orig, result = tuple(parse.parse("{} -> {}", line).fixed)
    rules[orig] = result

def step(template: str, rule: dict) -> str:
    result = ""

    pairs = zip(template[0:], template[1:])
    for i, pair in enumerate(pairs):
        pairString = "".join(pair)
        if i == 0:
            result += pair[0]
        if pairString in rule:
            result += rule[pairString] + pair[1]
        else:
            result += pair[1]

    return result

# Part 1
for i in range(10):
    template = step(template, rules)

chars = set([x for x in template])
step1 = {}
for char in chars:
    step1[char] = template.count(char)

print(max([count for _, count in step1.items()]) - min([count for _, count in step1.items()]))

# Part 2
counts = defaultdict(int)
for rule, val in rules.items():
    counts[rule] += countSubstring(INPUT_DATA[0], rule)

for i in range(0, 40):
    newCounts = defaultdict(int)
    for rule, val in rules.items():
        if counts[rule] > 0:
            pairL = rule[0] + val
            pairR = val + rule[1]
            newCounts[pairL] += counts[rule]
            newCounts[pairR] += counts[rule]

    counts = newCounts

results = defaultdict(int)
for rule, count in newCounts.items():
    results[rule[0]] += count
    results[rule[1]] += count
for char in results.keys():
    results[char] //= 2

firstChar = INPUT_DATA[0][0]
lastChar  = INPUT_DATA[0][-1]
results[firstChar] += 1
if firstChar != lastChar:
    results[lastChar] += 1

most = max([count for _, count in results.items()])
least = min([count for _, count in results.items()])

print(most - least)