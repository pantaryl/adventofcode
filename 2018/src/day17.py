with open("../input/day17.txt", 'r') as inputFile:
    data = inputFile.readlines()

import colorama, re, sys
from collections import defaultdict

# Need to increase the recursion limit for this problem. 10000 should be fine.
sys.setrecursionlimit(10000)

grid = defaultdict(lambda: '.')

# Parse the input data into our underground system.
for line in data:
    values = line.split(", ")
    xVal = None
    yVal = None
    for value in values:
        if 'x' in value:
            xRange = re.findall(r'(-?\d+)', value)
            if len(xRange) == 1:
                xVal = int(xRange[0])
            else:
                xVal = xRange
        else:
            assert('y' in value)
            yRange = re.findall(r'(-?\d+)', value)
            if len(yRange) == 1:
                yVal = int(yRange[0])
            else:
                yVal = yRange
    if isinstance(xVal, list):
        for x in range(int(xVal[0]), int(xVal[1])+1):
            grid[(x, yVal)] = '#'
    else:
        assert(isinstance(yVal, list))
        for y in range(int(yVal[0]), int(yVal[1])+1):
            grid[(xVal, y)] = '#'

# Determine what the min/max grid coordinates are.
minClayX = sorted(grid.keys(), key=lambda x:x[0])[0][0]
maxClayX = sorted(grid.keys(), key=lambda x:x[0])[-1][0]
minClayY = sorted(grid.keys(), key=lambda y:y[1])[0][1]
maxClayY = sorted(grid.keys(), key=lambda y:y[1])[-1][1]

# Put the water spring at the top.
grid[(500,0)] = '+'

def printGrid():
    for y in range(0, maxClayY+1):
        print(colorama.Style.RESET_ALL)
        for x in range(minClayX, maxClayX+1):
            char = grid[(x, y)]
            if char == '#':
                print(colorama.Fore.RED + colorama.Back.RED + char, end='')
            elif char == '|':
                print(colorama.Fore.GREEN + colorama.Back.GREEN + char, end='')
            elif char == '~':
                print(colorama.Fore.BLUE + colorama.Back.BLUE + char, end='')
            else:
                print(colorama.Style.RESET_ALL + char, end='')

# Part 1
flowing = set()
settled = set()
def fill(point, direction=(0,1)):
    # Add this point to the list of flowing points.
    flowing.add(point)
    grid[point] = '|'

    # Get the point down below this one.
    down = (point[0], point[1] + 1)

    # If the point beneath this one is not clay and it isn't flowing and it is within our map, fill downwards.
    if grid[down] != "#" and down not in flowing and down[1] <= maxClayY:
        fill(down)

    # If the point beneath this one is not clay and it isn't settled, return False (no fill occured)
    if grid[down] != '#' and down not in settled:
        return False

    # Get the points to the left and right of us.
    left  = (point[0] - 1, point[1])
    right = (point[0] + 1, point[1])

    # The left/right is filled if that point is clay or if that point is not flowing and was successfully filled.
    leftFilled  = grid[left] == '#'  or left  not in flowing and fill(left,  direction=(-1, 0))
    rightFilled = grid[right] == '#' or right not in flowing and fill(right, direction=(1,  0))

    if direction == (0, 1) and leftFilled and rightFilled:
        # If we're going down and the left and right are filled, that must mean we are now settled,
        # as are the points to the left and right.
        settled.add(point)
        grid[point] = '~'

        # For the left/right points that are flowing, make them settled.
        while left in flowing:
            settled.add(left)
            grid[left] = '~'
            left = (left[0] - 1, left[1])
        while right in flowing:
            settled.add(right)
            grid[right] = '~'
            right = (right[0] + 1, right[1])

    # We're filled if we're moving leftwards and the left is filled or clay, or
    # if we're moving rightwards and the right is filled or clay.
    return (direction == (-1, 0) and (leftFilled or grid[left] == '#')) or (direction == (1, 0) and (rightFilled or grid[right] == '#'))

fill((500, 0))

# Part 1
print("Part1:", len([point for point in flowing | settled if point[1] >= minClayY and point[1] <= maxClayY]))

# Part 2
print("Part2:", len([point for point in settled if point[1] >= minClayY and point[1] <= maxClayY]))

# Change to True to print the final grid.
if False:
    print()
    printGrid()