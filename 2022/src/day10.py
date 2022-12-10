from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]

register = 1
clock    = 0
# Part 1
line_num = 0
current_inst = None

lengths = { 'noop' : 1, 'addx' : 2 }

tick = -20

strength = {}

matches = defaultdict(lambda: '.')

while line_num < len(INPUT_DATA):
    # start of the cycle
    real_clock = clock + 1
    if (tick + real_clock) % 40 == 0:
        if real_clock not in strength:
            strength[real_clock] = register * real_clock

    pix_y = clock // 40
    pix_x = clock  % 40

    if pix_x in [ register - 1, register, register + 1]:
        if clock == 240: assert()
        matches[complex(pix_x, pix_y)] = '#'

    data = INPUT_DATA[line_num].split()
    instruction = data[0]

    # start execution of instruction
    if instruction == "noop":
        line_num += 1
    elif current_inst is not None and int(current_inst[0]) + 1 == clock:
        line_num += 1
        register += int(data[1])
        current_inst = None
    elif current_inst is None:
        current_inst = (clock, data)

    # end of the cycle
    clock += 1

print(sum([val for clock, val in strength.items()]))

# Part 2
getStringFromGrid(matches, '#', printGrid=False)