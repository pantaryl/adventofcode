with open("../input/day6.txt", 'r') as inputFile:
    data = inputFile.readlines()

answers = []
currentAnswer = set()
for line in data:
    line = line.rstrip()
    if line == "" or line == "\n":
        answers.append(currentAnswer)
        currentAnswer = set()
    else:
        for char in line:
            currentAnswer.add(char)

answers.append(currentAnswer)
print(sum([len(x) for x in answers]))

answers = []
currentAnswer = []
for line in data:
    line = line.rstrip()
    if line == "" or line == "\n":
        answers.append(list(set.intersection(*map(set, currentAnswer))))
        currentAnswer = []
    else:
        currentLine = []
        for char in line:
            currentLine.append(char)
        currentAnswer.append(currentLine)

answers.append(list(set().union(*currentAnswer)))
print(sum([len(x) for x in answers]))