from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x.split(" ") for x in INPUT_DATA]

# Part 1
score = 0
for other, me in INPUT_DATA:
    if me == 'X':
        # I throw rock
        score += 1
        if other == "A": score += 3
        elif other == "B": score += 0
        elif other == "C": score += 6
    elif me == "Y":
        # I throw paper
        score += 2
        if other == "A": score += 6
        elif other == "B": score += 3
        elif other == "C": score += 0
    elif me == "Z":
        # I throw scissors
        score += 3
        if other == "A": score += 0
        elif other == "B": score += 6
        elif other == "C": score += 3

print(score)

# Part 2
score = 0
for other, me in INPUT_DATA:
    if me == 'X':
        # Need to lose
        score += 0
        if other == "A": score += 3
        elif other == "B": score += 1
        elif other == "C": score += 2
    elif me == "Y":
        # Need to draw
        score += 3
        if other == "A": score += 1
        elif other == "B": score += 2
        elif other == "C": score += 3
    elif me == "Z":
        # Need to win
        score += 6
        if other == "A": score += 2
        elif other == "B": score += 3
        elif other == "C": score += 1

print(score)