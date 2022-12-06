from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [*INPUT_DATA[0]]

# Part 1
count = 0
four = deque()
for val in INPUT_DATA:
    if len(four) == 4:
        four.popleft()
    four.append(val)
    count += 1

    if len(set(four)) == 4:
        print(count, four)
        break

# Part 2
count = 0
fourteen = deque()
for val in INPUT_DATA:
    if len(fourteen) == 14:
        fourteen.popleft()
    fourteen.append(val)
    count += 1

    if len(set(fourteen)) == 14:
        print(count, fourteen)
        break