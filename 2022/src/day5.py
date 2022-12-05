from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]

index = INPUT_DATA.index("")
num_crates = len(re.findall(r"\d", INPUT_DATA[index - 1]))
orig_crates = [deque() for i in range(num_crates)]

for i in range(num_crates):
    for idx in range(0, index - 1):
        line = INPUT_DATA[idx][i*4:i*4+4].lstrip().rstrip()
        if line:
            orig_crates[i].append(parse("[{:w}]", line)[0])

# Part 1
crates = deepcopy(orig_crates)
for line in INPUT_DATA[index+1:]:
    count, from_crate, to_crate = parse("move {:d} from {:d} to {:d}", line)
    for i in range(count):
        value = crates[from_crate - 1].popleft()
        crates[to_crate - 1].appendleft(value)

print("".join([x[0] for x in crates]))

# Part 2
crates = deepcopy(orig_crates)
for line in INPUT_DATA[index+1:]:
    count, from_crate, to_crate = parse("move {:d} from {:d} to {:d}", line)
    values = []
    for i in range(count):
        values.append(crates[from_crate - 1].popleft())
    for i in range(count):
        crates[to_crate - 1].appendleft(values.pop())


print("".join([x[0] for x in crates]))