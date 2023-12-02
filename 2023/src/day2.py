from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]

total = 0
part2 = 0
for game in INPUT_DATA:
    id, data = game.split(":")
    id = int(id.split(" ")[1])

    my_set = [0, 0, 0]

    amounts = {
        'red' : 0,
        'green' : 0,
        'blue': 0,
    }

    possible = True

    for info in data[1:].split("; "):
        for counts in info.split(", "):
            count, color = counts.split(" ")
            count = int(count)

            if color == 'red':
                my_set = (max(my_set[0], count), my_set[1], my_set[2])
            elif color == 'green':
                my_set = (my_set[0], max(my_set[1], count), my_set[2])
            elif color == 'blue':
                my_set = (my_set[0], my_set[1], max(my_set[2], count))

            if {'red': 12, 'green': 13, 'blue': 14}[color] < count:
                possible = False

    if possible:
        total += int(id)

    part2 += my_set[0] * my_set[1] * my_set[2]

print(total)
print(part2)