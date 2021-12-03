from shared import *

# Input data is in INPUT_DATA.
# INPUT_DATA = [int(x) for x in INPUT_DATA]

# Part 1
gamma = ""
epsilon = ""

for i in range(len(INPUT_DATA[0])):
    count = Counter(x[i] for x in INPUT_DATA)

    if count['1'] > count['0']:
        gamma += "1"
        epsilon += "0"
    else:
        gamma += "0"
        epsilon += "1"

gamma   = int(gamma, 2)
epsilon = int(epsilon, 2)

print(gamma * epsilon)

# Part 2
def solve(rating):
    data = deepcopy(INPUT_DATA)

    for i in range(len(data[0])):
        if len(data) == 1: break

        count = Counter([x[i] for x in data])

        if count['1'] >= count['0']:
            val = '1' if rating == 'o' else '0'
        else:
            val = '0' if rating == 'o' else '1'
        data = [x for x in data if x[i] == val]

    assert(len(data) == 1)
    return int(data[0], 2)

oxy = solve('o')
co2 = solve('c')

print(oxy * co2)

