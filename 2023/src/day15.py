from shared import *

assert(len(INPUT_DATA) == 1)
INPUT_DATA = [x for x in INPUT_DATA[0].split(",")]

def _hash(string):
    starting_val = 0
    for char in string:
        starting_val += ord(char)
        starting_val *= 17
        starting_val %= 256
    return starting_val

print(sum(_hash(step) for step in INPUT_DATA))

boxes = [[] for i in range(256)]
for step in INPUT_DATA:
    if '-' in step:
        label = step[:-1]
    elif '=' in step:
        label, id = parse("{}={:d}", step)

    box_id = _hash(label)

    if '-' in step:
        boxes[box_id] = [x for x in boxes[box_id] if x[0] != label]
    else:
        if any([x[0] == label for x in boxes[box_id]]):
            boxes[box_id] = [x if x[0] != label else (label, id) for x in boxes[box_id]]
        else:
            boxes[box_id].append((label, id))

print(sum([i * j * item[1]
           for i, box in enumerate(boxes, 1)
           for j, item in enumerate(box, 1)]))