from shared import *

# Input data is in INPUT_DATA.
NEW_INPUT_DATA = [[int(y) for y in x if y.isdigit()] for x in INPUT_DATA]

print(sum([x[0] * 10 + x[-1] for x in NEW_INPUT_DATA]))

translation = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

part2 = 0
for i, line in enumerate(INPUT_DATA):
    numbers = []
    for j, x in enumerate(line):
        if x.isdigit():
            numbers.append(int(x))
        else:
            for k, y in enumerate(translation.keys()):
                if line[j:].startswith(y):
                    numbers.append(k + 1)
    part2 += numbers[0] * 10 + numbers[-1]

print(part2)