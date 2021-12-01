with open("../input/day2.txt", 'r') as inputFile:
    data = [x.rstrip() for x in inputFile.readlines()]

# Part 1
seen2 = 0
seen3 = 0
for string in data:
    uniqueValues = list(set(string))
    oldSeen2 = seen2
    oldSeen3 = seen3
    for value in uniqueValues:
        count = string.count(value)
        if count == 2 and (seen2 - oldSeen2) == 0:
            seen2 += 1
        elif count == 3 and (seen3 - oldSeen3) == 0:
            seen3 += 1
        if (seen2 - oldSeen2) == 1 and (seen3 - oldSeen3) == 1:
            break

checksum = seen2 * seen3
print(checksum)

# Part 2
result = None
for i in range(0, len(data)):
    stringLeft = data[i]
    if result:
        break
    for j in range(0, len(data)):
        if j == i:
            continue
        stringRight = data[j]
        diffValues = [1 if stringLeft[i] != stringRight[i] else 0 for i in range(0, len(stringLeft))]
        diff = sum(diffValues)

        if diff == 1:
            offset = diffValues.index(1)
            result = stringLeft[:offset] + stringRight[offset+1:]
            break

print("".join(result))