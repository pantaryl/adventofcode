from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]

new_data = []
for x in INPUT_DATA:
    x = x.split(",")
    assert(len(x) == 2)
    x[0] = x[0].split("-")
    x[1] = x[1].split("-")

    new_data.append(( int(x[0][0]), int(x[0][1]), int(x[1][0]), int(x[1][1]) ))

# Part 1
num_overlap = 0
for start_x, end_x, start_y, end_y in new_data:
    if start_x >= start_y and end_x <= end_y or \
       start_y >= start_x and end_y <= end_x:
        num_overlap += 1

print(num_overlap)

# Part 2
num_overlap = 0
for start_x, end_x, start_y, end_y in new_data:
    x = set(range(start_x, end_x + 1))
    y = set(range(start_y, end_y + 1))
    intersection = x.intersection(y)
    if len(list(intersection)) > 0:
        num_overlap += 1

print(num_overlap)