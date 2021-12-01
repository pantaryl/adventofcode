from intcode import Intcode

verbose = False

with open("../input/day25.txt", 'r') as inputFile:
    splitData = inputFile.read().split(",")
    data = [int(x) for x in splitData]

commands = [
    'east',
    'take whirled peas',
    'east',
    'north',
    'take prime number',
    'south',
    'west', # Sick Bay
    'north', # Passages
    'west', # Science Lab
    'south', # Storage
    'take antenna',
    'north',
    'east',
    'south', # Sick Bay
    'west', # Hull Breach
    'north', # Holodeck
    'take fixed point',
    'north',
    'east',
    'south'
]

inputStream = [ord(x) for line in commands for x in line+'\n']
runner = Intcode(verbose=False)
runner.initProgram(data, stallOnOutput=True)
runner.runProgram(inputStream=inputStream)
# Part 1
while runner.eop is False:
    while runner.readOutput:
        print(chr(runner.retVal), end='')
        runner.runProgram()
    if runner.needsInput:
        myInput = input("Input: ") + "\n"
        assert('\n' in myInput)
        runner.runProgram(inputStream=[ord(x) for x in myInput])

# Part 2
# Click a button and you're done!