with open("../input/day4.txt", 'r') as inputFile:
    data = inputFile.read().rstrip().lstrip().split("-")

data: tuple
testRange = list(range(int(data[0]), int(data[1])+1))

foundCases = set()

def determineCase(val: str):
    containsDoubles = any([x in val for x in ['00', '11', '22', '33', '44', '55', '66', '77', '88', '99']])
    alwaysIncrease  = all([val[x] >= val[x-1] for x in range(1, len(val))])
    return alwaysIncrease and containsDoubles

# Part 1
for i in testRange:
    string = str(i)
    if determineCase(string):
        foundCases.add(string)
print(len(foundCases))

# Part 2:
limitedCases = set()
for case in foundCases:
    counts = [case.count(x) for x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']]
    if 2 in counts:
        limitedCases.add(case)
print(len(limitedCases))