with open("../input/day14.txt", 'r') as inputFile:
    data = int(inputFile.read())

# Part 1
startRecipes = [3, 7]
elfOne = 0
elfTwo = 1
while len(startRecipes) < (data + 10):
    newRecipe = str(startRecipes[elfOne] + startRecipes[elfTwo])
    startRecipes.extend([int(x) for x in newRecipe])
    elfOne = (1 + startRecipes[elfOne] + elfOne) % len(startRecipes)
    elfTwo = (1 + startRecipes[elfTwo] + elfTwo) % len(startRecipes)

print("Part1: " + "".join(str(s) for s in startRecipes[-10:]))

# Part 2
currentString = "".join(str(s) for s in startRecipes)
if str(data) in currentString:
    print("Part2: " + str(currentString.index(str(data))))
else:
    dataList = [int(x) for x in str(data)]
    while startRecipes[-len(dataList):] != dataList and startRecipes[-len(dataList)-1:-1] != dataList:
        newRecipe = str(startRecipes[elfOne] + startRecipes[elfTwo])
        startRecipes.extend([int(x) for x in newRecipe])
        elfOne = (1 + startRecipes[elfOne] + elfOne) % len(startRecipes)
        elfTwo = (1 + startRecipes[elfTwo] + elfTwo) % len(startRecipes)

    index = len(startRecipes)-len(dataList) if startRecipes[-len(dataList):] == dataList else len(startRecipes)-len(dataList)-1
    print("Part2: " + str(index))