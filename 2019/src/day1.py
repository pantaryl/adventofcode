with open("../input/day1.txt", 'r') as inputFile:
    data = inputFile.readlines()

def calcFuelCost(value: int):
    return (value // 3) - 2

# Part 1
value = 0
for item in data:
    value += calcFuelCost(int(item))
print(value)

# Part 2
value = 0
for item in data:
    mass = int(item)
    initialFuel = calcFuelCost(mass)
    fuelForFuel = calcFuelCost(initialFuel)
    while fuelForFuel > 0:
        initialFuel += fuelForFuel
        fuelForFuel  = calcFuelCost(fuelForFuel)
    value    = value + initialFuel
print(value)