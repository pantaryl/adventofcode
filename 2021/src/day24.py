from shared import *

# Input data is in INPUT_DATA.
#INPUT_DATA = [int(x) for x in INPUT_DATA]

stack = []
rules = {}
pc    = 1
for i in range(14):
    divVal = 0
    xVal   = 0
    yVal   = 0
    while pc < len(INPUT_DATA):
        line = INPUT_DATA[pc]

        if 'inp' in line:
            pc += 1
            break
        elif 'div z' in line:
            divVal = int(line.split("div z ")[1])
            assert(divVal in [1, 26])
        elif parse.parse("add x {:d}", line):
            xVal = int(line.split("add x ")[1])
        elif parse.parse("add y {:d}", line) and "add y w" in INPUT_DATA[pc - 1]:
            yVal = int(line.split("add y ")[1])
        pc += 1
    assert(divVal != 0)
    if divVal == 1:
        stack.append((i, yVal))
    else:
        lastRule = stack.pop()
        assert(i not in rules and lastRule[0] not in rules)
        rules[i] = (lastRule[0], xVal + lastRule[1])
        rules[lastRule[0]] = (i, -(xVal + lastRule[1]))

print("Rules:")
for i in range(14):
    print(f"  {i} = input{rules[i][0]} + {rules[i][1]}")

def solve(largest):
    val = [0] * 14
    space = [9, 8, 7, 6, 5, 4, 3, 2, 1] if largest else [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(14):
        if val[i] == 0:
            rule = rules[i]
            # We're trying to maximize, so...
            for j in space:
                if 1 <= j + rule[1] <= 9:
                    val[i]       = j + rule[1]
                    val[rule[0]] = j
                    break
    print("".join([str(x) for x in val]))

# Part 1
solve(True)

# Part 2
solve(False)