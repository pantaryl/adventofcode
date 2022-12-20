from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [(i, int(x)) for i, x in enumerate(INPUT_DATA)]
num_inputs = len(INPUT_DATA)

d = deque(INPUT_DATA)

# Part 1
for index, value in INPUT_DATA:
    while True:
        nIndex, _ = d[0]
        if nIndex == index:
            break
        d.rotate(-1)

    nIndex, nValue = d.popleft()
    d.rotate(-1 * nValue)
    d.appendleft((nIndex, nValue))

zero_index = 0
while True:
    _, nValue = d[0]
    if nValue != 0:
        d.rotate(-1)
    else:
        break

print(d[1000 % num_inputs][1] + d[2000 % num_inputs][1] + d[3000 % num_inputs][1])

# Part 2
for i, data in enumerate(INPUT_DATA):
    INPUT_DATA[i] = (data[0], data[1] * 811589153)

d = deque(INPUT_DATA)

for i in range(1, 11):
    for index, value in INPUT_DATA:
        while True:
            nIndex, _ = d[0]
            if nIndex == index:
                break
            d.rotate(-1)

        nIndex, nValue = d.popleft()

        max_rotate = len(INPUT_DATA) - 1
        sign = (nValue // abs(nValue)) if nValue != 0 else 1
        amount_to_rotate = ((abs(nValue) % max_rotate) * sign * -1)

        d.rotate(amount_to_rotate)
        d.appendleft((nIndex, nValue))

    while True:
        _, nValue = d[0]
        if nValue != 0:
            d.rotate(-1)
        else:
            break

zero_index = 0
while True:
    _, nValue = d[0]
    if nValue != 0:
        d.rotate(-1)
    else:
        break

one, two, three = d[1000 % num_inputs][1], d[2000 % num_inputs][1], d[3000 % num_inputs][1]
print(one + two + three)