from shared import *
import math

# Input data is in INPUT_DATA.
#INPUT_DATA = [int(x) for x in INPUT_DATA]

lines = []

def reduce(tokens, debug=False):
    while True:
        found = False
        # All explodes first (i == 0)
        # Then try splits, if there are no explodes (i == 1)
        for mode in ['explode', 'split']:
            if found: continue

            index = 0
            depth = 0
            while index < len(tokens):
                val = tokens[index]
                if val == '[':
                    depth += 1
                elif val == ']':
                    depth -= 1

                if mode == 'explode' and depth > 4:
                    assert(isinstance(tokens[index + 1], int))
                    assert(isinstance(tokens[index + 3], int))
                    # We need to explode this token, and the next 3 to follow
                    prev = index - 1
                    while prev >= 0 and not isinstance(tokens[prev], int):
                        prev -= 1

                    prevValid = prev >= 0
                    if prevValid:
                        tokens[prev] = tokens[prev] + tokens[index + 1]

                    next = index + 4
                    while next < len(tokens) and not isinstance(tokens[next], int):
                        next += 1

                    nextValid = next < len(tokens)
                    if nextValid:
                        tokens[next] = tokens[next] + tokens[index + 3]

                    tokens.pop(index)
                    tokens.pop(index)
                    tokens.pop(index)
                    tokens.pop(index)
                    tokens.pop(index)
                    tokens.insert(index, 0)

                    if debug: print(f'    after explode:   {printTokens(tokens)}')
                    found = True
                    index = 0
                    break
                elif mode == 'split' and isinstance(val, int) and val >= 10:
                    tokens.pop(index)

                    left = int(math.floor(val / 2))
                    right = int(math.ceil(val / 2))

                    tokens.insert(index, ']')
                    tokens.insert(index, right)
                    tokens.insert(index, ',')
                    tokens.insert(index, left)
                    tokens.insert(index, '[')

                    if debug: print(f'    after split:     {printTokens(tokens)}')
                    index = 0
                    found = True
                    break
                else:
                    index += 1
        if not found: break

    return tokens

def add(left, right):
    tokens = [ '[' ] + left + [ ',' ] + right + [ ']' ]
    return tokens

for line in INPUT_DATA:
    depth  =  0
    tokens = []

    for char in line:
        if char.isdigit():
            tokens.append(int(char))
        else:
            tokens.append(char)

    lines.append(tokens)

def printTokens(tokens):
    output = ""
    depth = 0
    found = False
    for mode in ['explode', 'split']:
        if found: continue
        for i, val in enumerate(tokens):
            if val == '[': depth += 1

            if not found:
                if mode == 'explode' and depth > 4:
                    output += f"\033[4;37m{str(val)}"
                elif mode == 'split' and isinstance(val, int) and val >= 10:
                    output += f"\033[4;37m{str(val)}\033[0m"
                    found = True
                else:
                    output += str(val)
            else:
                output += str(val)

            if val == ']':
                if mode == 'explode' and depth > 4:
                    output += "\033[0m"
                    found = True

                depth -= 1

    return output

def magnitude(tokens):
    while len(tokens) > 1:
        index = 0
        while index < len(tokens):
            if tokens[index] == '['               and \
               isinstance(tokens[index + 1], int) and \
               isinstance(tokens[index + 3], int) and \
               tokens[index + 4] == ']':
                left = tokens[index + 1]
                right = tokens[index + 3]
                tokens.pop(index)
                tokens.pop(index)
                tokens.pop(index)
                tokens.pop(index)
                tokens.pop(index)
                tokens.insert(index, (3 * left) + (2 * right))
            index += 1

    return tokens[0]

Debug = True

# Part 1
part1 = deepcopy(lines)
while len(part1) > 1:
    left = part1.pop(0)
    right = part1.pop(0)
    if Debug: print(f"  {printTokens(left)}")
    if Debug: print(f"+ {printTokens(right)}")
    tokens = reduce(add(left, right), debug=Debug)
    if Debug: print(f"= {printTokens(tokens)}")
    if Debug: print()
    part1.insert(0, tokens)
assert(len(part1) == 1)
print(magnitude(part1[0]))

# Part 2
part2 = deepcopy(lines)
perms = permutations(part2, r=2)

maxMag = 0
for perm in perms:
    assert(len(perm) == 2)
    maxMag = max(maxMag, magnitude(reduce(add(perm[0], perm[1]))))

print(maxMag)
