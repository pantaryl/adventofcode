from shared import *

# Input data is in INPUT_DATA.
# INPUT_DATA = [int(x) for x in INPUT_DATA]

end = {
    '[' : ']',
    '{' : '}',
    '<' : '>',
    "(" : ')',
}

# Part 1
errors = defaultdict(list)
for y, line in enumerate(INPUT_DATA):
    stack = []
    for x, char in enumerate(line):
        if char in '[(<{':
            stack.append(char)
        elif char == end[stack[-1]]:
            stack.pop()
        else:
            errors[y].append(char)
            stack.pop()

score = {
    ')' : 3,
    ']' : 57,
    "}" : 1197,
    ">" : 25137,
}

NEW_INPUT_DATA = deepcopy(INPUT_DATA)

count = 0
for y, _ in enumerate(INPUT_DATA):
    error = errors[y]
    if error:
        count += score[error[0]]
        NEW_INPUT_DATA.remove(_)

print(count)

# Part 2
additions = defaultdict(list)
for y, line in enumerate(NEW_INPUT_DATA):
    stack = []
    for x, char in enumerate(line):
        if char in '[(<{':
            stack.append(char)
        elif char == end[stack[-1]]:
            stack.pop()
        else:
            assert()

    while len(stack) > 0:
        char = stack.pop()
        additions[y].append(end[char])

counts = [ 0 ] * len(NEW_INPUT_DATA)
for y in range(len(NEW_INPUT_DATA)):
    addition = additions[y]
    for item in addition:
        counts[y] *= 5
        counts[y]  += { ')' : 1, ']' : 2, '}': 3, '>': 4}[item]

counts = sorted(counts)
middle = len(counts)//2
print(counts[middle])