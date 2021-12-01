from collections import deque
import itertools

with open("../input/day12.txt", 'r') as inputFile:
    data = inputFile.readlines()

stateFromInput = data[0].split(" ")[-1].rstrip()
initialState = deque()
[initialState.append((i, stateFromInput[i])) for i in range(0, len(stateFromInput))]

stateCodes = {}
for state in data[2:]:
    values = state.rstrip().split(" ")
    stateCodes[values[0]] = values[2]

def runGens(part1, state):
    part1Sum = 0
    myState  = state.copy()
    lastSums = deque([(0, 0)])
    i = 1
    while True:
        # If the first or last four characters have a pot in them, we need to add empty pots to the beginning and end of
        # our row, respectively.
        start = list([x[1] for x in itertools.islice(myState, 0, 4)])
        end   = list([x[1] for x in itertools.islice(myState, len(myState) - 4, len(myState))])[::-1]
        if '#' in start:
            [myState.appendleft((myState[0][0]-1, '.')) for i in range(0, 4-start.index('#'))]
        if '#' in end:
            [myState.append((myState[-1][0]+1, '.')) for i in range(0, 4-end.index('#'))]
        
        nextState = myState.copy()

        # For every space in our pot lineup, we want to check if it matches one of the codes.
        # If it does, update nextState with the new pot state.
        # Then move onto the next pot.
        for j in range(len(myState)-4):
            match = "".join([x[1] for x in list(itertools.islice(myState, 0, 5))])
            if match in stateCodes:
                nextState[2] = (myState[2][0], stateCodes[match])
            nextState.rotate(-1)
            myState.rotate(-1)

        # Update our current state with the next generation.
        myState = nextState

        # Move 4 pots so that our most negative index pot is at myState[0]
        myState.rotate(-4)

        # Calculate the sum.
        mySum = sum(x[0] for x in myState if x[1] == '#')

        # Get the value for Part1.
        if i == part1: part1Sum = mySum

        # For Part2, at some point the pattern will even out and increment at a steady rate.
        # Find out when that is and report the increment, the sum at the last iteration, and the iteration count.
        if len(lastSums) == 100:
            lastSums.popleft()
        lastSums.append((mySum, mySum-lastSums[-1][0], i))
        if len(lastSums) == 100 and sum([x[1] for x in lastSums]) // len(lastSums) == lastSums[0][1]:
            break
        i += 1

    return part1Sum, lastSums[-1]

# Part 1
mySum, lastState = runGens(20, initialState)
print("Part 1: ", mySum)

# Part 2
mySum = (50000000000 - lastState[2]) * lastState[1] + lastState[0]
print("Part 2: ", mySum)