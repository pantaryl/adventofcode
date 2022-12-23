from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]

grid  = squareGridFromChars(INPUT_DATA)
elves = { pos for pos, value in grid.items() if value == '#' }

rules = [
    # North
    (lambda x: all([y not in elves for y in [x + -1-1j, x + 0-1J, x + 1-1j]]), 0-1j),
    # South
    (lambda x: all([y not in elves for y in [x + -1+1j, x + 0+1J, x + 1+1j]]), 0+1j),
    # West
    (lambda x: all([y not in elves for y in [x + -1-1j, x + -1+0j, x + -1+1j]]), -1+0j),
    # East
    (lambda x: all([y not in elves for y in [x + 1-1j, x + 1+0j, x + 1+1j]]), 1+0j),
]

rule_idx = 0
# Part 1
for round in range(0, 10):
    proposed_movement = {}
    for elf in elves:
        if all([(elf + x) not in elves for x in getAllSquareNeighbors()]):
            # Nothing to do for this elf, they stay still.
            proposed_movement[elf] = elf
        else:
            for rule in range(len(rules)):
                start = (rule_idx + rule) % len(rules)
                data  = rules[start]
                if data[0](elf):
                    # We've found our proposed movement
                    proposed_movement[elf] = elf + data[1]
                    break
            else:
                proposed_movement[elf] = elf

    new_positions = [x for _, x in proposed_movement.items()]
    new_positions = [x for x in new_positions if new_positions.count(x) == 1]

    for elf in list(elves):
        if proposed_movement[elf] in new_positions:
            elves.remove(elf)
            elves.add(proposed_movement[elf])

    rule_idx = (rule_idx + 1) % len(rules)

count = 0
x_dim, y_dim = get_min_max(elves)
for x in range(x_dim[0], x_dim[1] + 1):
    for y in range(y_dim[0], y_dim[1] + 1):
        if complex(x, y) not in elves:
            count += 1
print(count)

# Part 2
round = 10
while True:
    proposed_movement = {}
    no_movement = 0
    for elf in elves:
        if all([(elf + x) not in elves for x in getAllSquareNeighbors()]):
            # Nothing to do for this elf, they stay still.
            proposed_movement[elf] = elf
            no_movement += 1
        else:
            for rule in range(len(rules)):
                start = (rule_idx + rule) % len(rules)
                data  = rules[start]
                if data[0](elf):
                    # We've found our proposed movement
                    proposed_movement[elf] = elf + data[1]
                    break
            else:
                proposed_movement[elf] = elf
                no_movement += 1

    print(f"\rRound {round + 1}, Num Elves {len(elves)}, NoMovement {no_movement}", end='')
    if no_movement == len(elves):
        print(f"\r{round + 1}")
        break

    new_positions = [x for _, x in proposed_movement.items()]
    new_positions = [x for x in new_positions if new_positions.count(x) == 1]

    for elf in list(elves):
        if proposed_movement[elf] in new_positions:
            elves.remove(elf)
            elves.add(proposed_movement[elf])

    rule_idx = (rule_idx + 1) % len(rules)
    round += 1
