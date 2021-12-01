with open("../input/day8.txt", 'r') as inputFile:
    data = inputFile.read()
data = data.split(" ")

class Node():
    def __init__(self):
        self.children = []
        self.metadata = []

def parseChild(parent):
    newNode = Node()
    if parent is not None:
        parent.children.append(newNode)

    numChildren = int(data.pop(0))
    numMetadata = int(data.pop(0))

    if numChildren > 0:
        for i in range(numChildren):
            parseChild(newNode)
    for i in range(numMetadata):
        value = int(data.pop(0))
        newNode.metadata.append(value)
    return newNode

root = parseChild(None)

# Part 1
def traversePart1(node):
    mySum  = sum([traversePart1(child) for child in node.children])
    mySum += sum(node.metadata)
    return mySum
print(traversePart1(root))

# Part 2
def traversePart2(node):
    mySum = 0
    if len(node.children) > 0:
        for i in range(len(node.metadata)):
            childIdx = node.metadata[i] - 1
            if childIdx < len(node.children):
                mySum += traversePart2(node.children[childIdx])
    else:
        mySum += sum(node.metadata)
    return mySum
print(traversePart2(root))