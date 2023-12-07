from shared import *
from enum import Enum

# Input data is in INPUT_DATA.
INPUT_DATA = [x.split(" ") for x in INPUT_DATA]

order = [
    'A',
    'K',
    'Q',
    'J',
    'T',
    '9',
    '8',
    '7',
    '6',
    '5',
    '4',
    '3',
    '2',
]

class Type(Enum):
    FIVE = 0
    FOUR = 1
    FULL = 2
    THREE = 3
    TWOPAIR = 4
    ONEPAIR = 5
    HIGH    = 6

def get_type(hand: str):
    unique_values = list(set(hand))
    num_unique_values = len(unique_values)

    if num_unique_values == 1:
        return Type.FIVE
    elif num_unique_values == 2:
        counts = [hand.count(x) for x in unique_values]
        if 4 in counts:
            return Type.FOUR
        elif 3 in counts:
            return Type.FULL
    elif num_unique_values == 3:
        counts = [hand.count(x) for x in unique_values]
        if 3 in counts:
            return Type.THREE
        elif counts.count(2):
            return Type.TWOPAIR
    elif num_unique_values == 4:
        return Type.ONEPAIR
    else:
        return Type.HIGH

ranks = sorted(INPUT_DATA, reverse=True, key=lambda x: (get_type(x[0]).value, [order.index(y) for y in x[0]]))

print(sum([(i + 1) * int(x[1]) for i, x in enumerate(ranks)]))

order = [
    'A',
    'K',
    'Q',
    'T',
    '9',
    '8',
    '7',
    '6',
    '5',
    '4',
    '3',
    '2',
    'J',
]

def get_type(hand: str):
    unique_values = list(set(hand))
    num_unique_values = len(unique_values)

    num_jokers = hand.count('J')

    if num_unique_values == 1:
        return Type.FIVE
    elif num_unique_values == 2:
        counts = [hand.count(x) for x in unique_values]
        if 4 in counts:
            if num_jokers in (1, 4):
                return Type.FIVE
            return Type.FOUR
        elif 3 in counts:
            if num_jokers in (2, 3):
                return Type.FIVE
            elif num_jokers == 1:
                return Type.FOUR
            return Type.FULL
    elif num_unique_values == 3:
        counts = [hand.count(x) for x in unique_values]
        if 3 in counts:
            if num_jokers in (1, 3):
                return Type.FOUR
            return Type.THREE
        elif counts.count(2):
            if num_jokers == 1:
                return Type.FULL
            elif num_jokers == 2:
                return Type.FOUR
            return Type.TWOPAIR
    elif num_unique_values == 4:
        if num_jokers in (1, 2):
            return Type.THREE
        return Type.ONEPAIR
    else:
        if num_jokers == 1:
            return Type.ONEPAIR
        return Type.HIGH

ranks = sorted(INPUT_DATA, reverse=True, key=lambda x: (get_type(x[0]).value, [order.index(y) for y in x[0]]))

print(sum([(i + 1) * int(x[1]) for i, x in enumerate(ranks)]))