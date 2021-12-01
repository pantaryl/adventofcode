from collections import defaultdict
from helpers import memoize
from copy import deepcopy
from enum import Enum
import os
import re
from math_utils import *

# Complex numbers in Python! == i + nj (x + ny), good for coordinates
# complex*+imaginary to rotate left/ccw, complex*-imaginary to rotate right/cw
# For example:
# Rotate CCW by 270 degrees:
#    val *= complex(0, 1) ** 3 [each power represents 90 degrees]

with open(f"../input/{os.path.splitext(os.path.basename(__file__))[0]}.txt", 'r') as inputFile:
    data = [x.rstrip() for x in inputFile.readlines()]
    #data = [int(x) for x in data]

ingredients = defaultdict(int)
allergens   = set()
allergenPossibilies = defaultdict(list)
for line in data:
    if "(" in line:
        first, second = line.split("(")
        newIngredients = first.rstrip().split(" ")
        newAllergens   = second.replace("contains ", "").replace(")", "").split(", ")
        for ingredient in newIngredients:
            ingredients[ingredient] += 1
        allergens.update(newAllergens)
        for allergen in newAllergens:
            allergenPossibilies[allergen].append(newIngredients)

intersection = {}
for allergen in allergens:
    possibilities = allergenPossibilies[allergen]
    intersect     = set(possibilities[0])
    for i in range(1, len(possibilities)):
        intersect = intersect.intersection(possibilities[i])

    intersection[allergen] = list(intersect)


foundIngredients = {}
while len(foundIngredients.keys()) != len(allergens):
    for allergen in allergens:
        if allergen in foundIngredients: continue
        if len(intersection[allergen]) > 1: continue

        foundIngredients[allergen] = intersection[allergen][0]
        for a in allergens:
            if foundIngredients[allergen] in intersection[a]:
                intersection[a].remove(foundIngredients[allergen])
        ingredients.pop(foundIngredients[allergen])

# Part 1
print(sum(ingredients.values()))

# Part 2
print(",".join(foundIngredients[x] for x in sorted(foundIngredients.keys())))