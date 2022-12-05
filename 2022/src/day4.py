from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [parse("{:d}-{:d},{:d}-{:d}", x) for x in INPUT_DATA]

# Part 1
num_overlap = 0
for start_x, end_x, start_y, end_y in INPUT_DATA:
    if start_x >= start_y and end_x <= end_y or \
       start_y >= start_x and end_y <= end_x:
        num_overlap += 1

print(num_overlap)

# Part 2
num_overlap = 0
for start_x, end_x, start_y, end_y in INPUT_DATA:
    x = set(range(start_x, end_x + 1))
    y = set(range(start_y, end_y + 1))
    intersection = x.intersection(y)
    if len(list(intersection)) > 0:
        num_overlap += 1

print(num_overlap)