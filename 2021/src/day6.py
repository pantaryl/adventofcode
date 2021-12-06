from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [int(x) for x in INPUT_DATA[0].split(",")]

fishes = deque()
for i in range(0, 9):
    fishes.append(INPUT_DATA.count(i))

for i in range(0, 256):
    fishes.rotate(-1)
    fishes[6] += fishes[-1]

    if i == 79 or i == 255:
        print(sum(fishes))
