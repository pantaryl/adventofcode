from typing import NamedTuple

PasswordConfig = NamedTuple("PasswordConfig", [ ("min", int), ("max", int), ("letter", str), ("password", str)])

with open("../input/day2.txt", 'r') as inputFile:
    lines = inputFile.readlines()
    data  = []
    for line in lines:
        splitLines = line.split(" ")
        assert(len(splitLines) == 3)
        minCount   = int(splitLines[0].split("-")[0])
        maxCount   = int(splitLines[0].split("-")[1])
        letter     = splitLines[1].replace(":", "")
        password   = splitLines[2]
        data.append(PasswordConfig(minCount, maxCount, letter, password))

# Part 1
def oldDetermineValid(config: PasswordConfig):
    return config.max >= config.password.count(config.letter) >= config.min

print(sum([1 if oldDetermineValid(config) else 0 for config in data]))

# Part 2
def newDetermineValid(config: PasswordConfig):
    chars = config.password[config.min-1] + config.password[config.max-1]
    return chars.count(config.letter) == 1

print(sum([1 if newDetermineValid(config) else 0 for config in data]))