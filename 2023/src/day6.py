from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]

times = [int(x) for x in INPUT_DATA[0].split(":")[1].split(" ") if x != ""]
distances = [int(x) for x in INPUT_DATA[1].split(":")[1].split(" ") if x != ""]
win_counts = []

for i, time in enumerate(times):
    record = distances[i]

    wins = []
    for j in range(time + 1):
        distance = (time - j) * j
        if distance > record:
            wins.append(j)

    win_counts.append(len(wins))

prod = 1
for x in win_counts:
    prod *= x
print(prod)

time = int(INPUT_DATA[0].split(":")[1].replace(" ", ""))
distance = int(INPUT_DATA[1].split(":")[1].replace(" ", ""))

win_count = 0
for j in range(time + 1):
    length = (time - j) * j
    if length > distance:
        win_count += 1
print(win_count)