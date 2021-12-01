import copy

with open("../input/day7.txt", 'r') as inputFile:
    data = inputFile.readlines()

indices = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

origNodes = [{'name': indices[i], 'prereq': [], 'children': []} for i in range(26)]
database = {}
for node in origNodes:
    database[node['name']] = node

for line in data:
    values = line.rstrip().split(" ")
    parent = values[1]
    child  = values[7]

    origNodes[indices.index(child)]['prereq'].append(parent)
    origNodes[indices.index(parent)]['children'].append(child)

# Part 1
complete = []
nodes = copy.deepcopy(origNodes)
while len(nodes) > 0:
    currentNode = sorted(nodes, key=lambda x: (len(x['prereq']), nodes.index(x)))[0]
    complete.append(currentNode)
    nodes.remove(currentNode)

    for node in nodes:
        if currentNode['name'] in node['prereq']:
            node['prereq'].remove(currentNode['name'])
        if currentNode['name'] in node['children']:
            node['children'].remove(currentNode['name'])

print("".join([x['name'] for x in complete]))

# Part 2
NumWorkers  = 5
workers     = [None] * NumWorkers
TimeForTask = 60 + 1
nodes = copy.deepcopy(origNodes)

currentTime = 0
minNextTime = []

def calcTime(startTime, letter):
    return startTime + TimeForTask + indices.index(letter)

while len(nodes) > 0:
    busyWorker = any(workers)
    if busyWorker:
        for i in range(len(workers)):
            worker = workers[i]
            if worker is not None and calcTime(worker[1], worker[0]['name']) == currentTime:
                minNextTime.remove(currentTime)
                currentNode = worker[0]
                for node in nodes:
                    if currentNode['name'] in node['prereq']:
                        node['prereq'].remove(currentNode['name'])
                    if currentNode['name'] in node['children']:
                        node['children'].remove(currentNode['name'])
                workers[i] = None

    freeWorkers = workers.count(None) > 0
    if freeWorkers:
        nodes.sort(key=lambda x: (len(x['prereq']), indices.index(x['name'])))
        for i in range(len(workers)):
            if workers[i] is not None: continue
            if (len(nodes) == 0): break
            if len(nodes[0]['prereq']) == 0:
                workers[i] = (nodes[0], currentTime)
                minNextTime.append(calcTime(currentTime,(nodes[0]['name'])))
                nodes.remove(nodes[0])

    if len(minNextTime) > 0:
        minNextTime.sort()
        currentTime = minNextTime[0]
    else:
        break

print(sorted(minNextTime)[-1])