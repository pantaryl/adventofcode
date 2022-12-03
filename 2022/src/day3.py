from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [(x[0:len(x)//2], x[len(x)//2:]) for x in INPUT_DATA]

# Part 1
matches_found = []
for left_runsack, right_runsack in INPUT_DATA:
    match = set([*left_runsack]).intersection(set([*right_runsack]))
    assert(len(list(match)) == 1)
    matches_found.append(list(match)[0])

sum = 0
for val in matches_found:
    if val in "abcdefghijklmnopqrstuvwxyz":
        sum += ord(val) - ord('a') + 1
    else:
        assert(val in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        sum += ord(val) - ord('A') + 27

print(sum)

# Part 2
matches_found = []
i = 0
while i < len(INPUT_DATA):
    group = INPUT_DATA[i:i+3]
    i += 3

    match = set([*(group[0][0]+group[0][1])]).intersection(set([*(group[1][0]+group[1][1])])).intersection(set([*(group[2][0]+group[2][1])]))
    assert(len(list(match)) == 1)
    matches_found.append(list(match)[0])

sum = 0
for val in matches_found:
    if val in "abcdefghijklmnopqrstuvwxyz":
        sum += ord(val) - ord('a') + 1
    else:
        assert(val in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        sum += ord(val) - ord('A') + 27
print(sum)