from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [int(x) for x in INPUT_DATA]

# Part 1
count = 0
for i, val in enumerate(INPUT_DATA):
    if i == 0: continue
    if val > INPUT_DATA[i - 1]: count += 1

print(count)

# Part 2
count = 0
prevWindow = None
curWindow  = 0
for i, val in enumerate(INPUT_DATA):
    if i < 2: continue
    curWindow = INPUT_DATA[i - 2] + INPUT_DATA[i - 1] + INPUT_DATA[i]
    if prevWindow and curWindow > prevWindow: count += 1
    prevWindow = curWindow

print(count)