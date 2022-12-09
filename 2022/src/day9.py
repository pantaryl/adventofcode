from shared import *
import math

# Input data is in INPUT_DATA.
INPUT_DATA = [parse("{:w} {:d}", x) for x in INPUT_DATA]

# Part 1
head = 0+0j
tail = 0+0j

tail_pos = set([0+0j])

directions = {
    "U" : OrderedComplex(0-1j),  # up
    "D" : OrderedComplex(0+1j),  # down
    "L" : OrderedComplex(-1+0j), # left
    "R" : OrderedComplex(1+0j)   # right
}

for dir, count in INPUT_DATA:
    movement = directions[dir]

    for i in range(count):
        head += movement
        distance = math.sqrt(abs(int(tail.real) - int(head.real)) ** 2 + abs(int(tail.imag) - int(head.imag)) ** 2) // 1
        if distance > 1:
            if tail.real == head.real or tail.imag == head.imag:
                tail += movement
            elif tail.real < head.real and tail.imag > head.imag:
                # Tail bottom left
                tail += 1 - 1j
            elif tail.real < head.real and tail.imag < head.imag:
                # Tail top left
                tail += 1 + 1j
            elif tail.real > head.real and tail.imag > head.imag:
                # Tail bottom right
                tail += -1 - 1j
            elif tail.real > head.real and tail.imag < head.imag:
                # Tail top right
                tail += -1 + 1j

        tail_pos.add(tail)

print(len(tail_pos))

# Part 2

def printgrid():
    char_table = {}
    char_table[0+0j] = 's'
    if head not in char_table:
        char_table[head] = 'H'
    for i, tail in enumerate(tails, start=1):
        if tail not in char_table:
            char_table[tail] = i

    printSetGrid(known_pos=set([head] + tails),
                 char_table=char_table,
                 x_dim=(-11, 14),
                 y_dim=(-15, 5))

head  = 0+0j
tails = [ 0+0j ] * 9
tail_pos = []
for i in range(9):
    tail_pos.append(set([0+0j]))

for line_num, instruction in enumerate(INPUT_DATA):
    dir, count = instruction
    movement = directions[dir]

    for i in range(count):
        head += movement
        for tail_idx, tail in enumerate(tails):
            prev = head if tail_idx == 0 else tails[tail_idx - 1]

            x1x2 = abs(int(tail.real) - int(prev.real)) ** 2
            y1y2 = abs(int(tail.imag) - int(prev.imag)) ** 2
            distance = math.sqrt(x1x2 + y1y2) // 1
            if distance > 1:
                if tail.real == prev.real:
                    if tail.imag > prev.imag:
                        tail += 0-1j
                    else:
                        tail += 0+1j
                elif tail.imag == prev.imag:
                    if tail.real > prev.real:
                        tail += -1+0j
                    else:
                        tail += 1+0j
                elif tail.real < prev.real and tail.imag > prev.imag:
                    # Tail bottom left
                    tail += 1 - 1j
                elif tail.real < prev.real and tail.imag < prev.imag:
                    # Tail top left
                    tail += 1 + 1j
                elif tail.real > prev.real and tail.imag > prev.imag:
                    # Tail bottom right
                    tail += -1 - 1j
                elif tail.real > prev.real and tail.imag < prev.imag:
                    # Tail top right
                    tail += -1 + 1j

            tails[tail_idx] = tail
            tail_pos[tail_idx].add(tail)

    #print(f"== {dir} {count} ==")
    #printgrid()
    #print()
    #print()

#printSetGrid(tail_pos[-1], char_table=None)
print(len(tail_pos[-1]))