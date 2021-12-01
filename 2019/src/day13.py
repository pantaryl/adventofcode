from intcode import Intcode

with open("../input/day13.txt.txt", 'r') as inputFile:
    splitData = inputFile.read().split(",")
    data = [int(x) for x in splitData]

def getNumBlocks(tiles: dict, blockType: int):
    return sum([1 if id == blockType else 0 for _, id in tiles.items()])

# Part 1
runner = Intcode(verbose=False)
runner.initProgram(data, stallOnOutput=True)
tiles = {}
runner.runProgram()
while runner.eop is False:
    assert(runner.readOutput)
    x = runner.retVal
    runner.runProgram()
    assert(runner.readOutput)
    y = runner.retVal
    runner.runProgram()
    assert(runner.readOutput)
    id = runner.retVal
    runner.runProgram()

    tiles[(x, y)] = id
print("Part1:", getNumBlocks(tiles, 2))

# Part 2
def calcManhattanDist(loc: tuple, other: tuple):
    return abs(loc[0] - other[0]) + abs(loc[1] - other[1])

def getClosestBallCoord(tiles: dict, paddle: tuple):
    ball = None
    assert(getNumBlocks(tiles, 3) == 1)
    for coord, id in tiles.items():
        if id == 4:
            ball = coord
            break
    return ball

def getPaddle(tiles: dict):
    paddle = None
    for coord, id in tiles.items():
        if id == 3:
            paddle = coord
            break
    return paddle

part2 = list(data)
part2[0] = 2
currentScore = 0
runner.initProgram(part2, stallOnOutput=True)
runner.runProgram()
tiles = {}
while runner.eop is False:
    if runner.needsInput:
        paddle = getPaddle(tiles)
        ball = getClosestBallCoord(tiles, paddle)
        if paddle[0] < ball[0]:
            runner.runProgram(inputStream=[1])
        elif paddle[0] > ball[0]:
            runner.runProgram(inputStream=[-1])
        else:
            runner.runProgram(inputStream=[0])
    elif runner.readOutput:
        x = runner.retVal
        runner.runProgram()
        y = runner.retVal
        runner.runProgram()

        if x == -1 and y == 0:
            currentScore = runner.retVal
        else:
            id = runner.retVal
            tiles[(x, y)] = id
        runner.runProgram()
print("Part2:", currentScore)
