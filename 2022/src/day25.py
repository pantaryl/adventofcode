from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]

values = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

# Part 1
overall_total = 0
for number in INPUT_DATA:
    total = 0
    base = 0
    for char in reversed(number):
        total += values[char] * (5 ** base)
        base += 1

    overall_total += total

numbers = ""
while overall_total:
    numbers = "012=-"[overall_total % 5] + numbers
    overall_total = (overall_total + 2) // 5

print(numbers)