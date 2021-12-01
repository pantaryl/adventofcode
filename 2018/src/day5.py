import sys

with open("../input/day5.txt", 'r') as inputFile:
    data = inputFile.read()

def reducePolymer(data):
    i = 0
    while i < len(data) - 1:
        if data[i].isupper() != data[i+1].isupper() and \
           data[i].lower() == data[i+1].lower():
            if i == 0:
                data = data[i+2:]
            else:
                data = data[0:i] + data[i+2:]
                i -= 1
        else:
            i += 1
    return data

# Part 1
print(len(reducePolymer(data)))

# Part 2
minCharacter = (None, sys.maxsize)
uniqueCharacters = set(data.lower())
for character in uniqueCharacters:
    newData = data.replace(character, '').replace(character.upper(), '')
    reduction = len(reducePolymer(newData))
    if reduction < minCharacter[1]:
        minCharacter = (character, reduction)

print(minCharacter)