from shared import *

for i, data in enumerate(INPUT_DATA):
    data = data.split(" ")
    
    # Use a tuple because it can be hashed.
    data[1] = tuple([int(x) for x in data[1].split(",")])

    INPUT_DATA[i] = (data[0], data[1])

# Need to use memoize, otherwise the combinatorial explosion is enough to make my computer cry.
@memoize
def solve(index):
    state, current, groups = index

    if not state:
        # We're at the end of the state.
        if current == 0 and len(groups) == 0:
            # If we're not in a run and there are no remaining groups, we've found a winner.
            return 1
        if len(groups) == 1 and current != 0 and current == groups[0]:
            # If there is one group left and our current run matches the length, we've found a winner.
            return 1
        # Otherwise, this is a loser.
        return 0

    remaining_possibilites = state.count('#') + state.count("?")
    if (remaining_possibilites + current) < sum(groups):
        # If the remaining possibilites is smaller than the number we need, this is a loser.
        return 0
    if current != 0 and len(groups) == 0:
        # If we're in a run and there isn't anything left to be counted, this is a loser.
        return 0

    solved = 0
    if state[0] == '.' and current != 0 and current != groups[0]:
        # If we've come across the end of a run and our current run count doesn't match the next group,
        # this is a loser.
        return 0
    elif state[0] == '.' and current != 0:
        # Otherwise, we want to keep moving forward.
        solved += solve((state[1:], 0, groups[1:]))

    if state[0] == '?' and current != 0 and current == groups[0]:
        # If we've hit a random while in a current run and our current run is the size of the next group,
        # move to the next group.
        solved += solve((state[1:], 0, groups[1:]))
    elif state[0] in ('#', '?') and current != 0:
        # If we we could still go, keep going.
        solved += solve((state[1:], current + 1, groups))
    elif state[0] in ['#', '?'] and current == 0:
        # If we're not in a run, we're about to be.
        solved += solve((state[1:], 1, groups))

    if state[0] in ('.', '?') and current == 0:
        # If we're not in a run, we're possibly still not.
        solved += solve((state[1:], 0, groups))
    return solved

print(sum([solve((line, 0, groups)) for line, groups in INPUT_DATA]))

for i, data in enumerate(INPUT_DATA):
    # Use "?".join() to handle the case that the "?" only comes between the new sets, not after each one.
    state = "?".join([data[0], data[0], data[0], data[0], data[0]])
    groups = data[1] * 5

    INPUT_DATA[i] = (state, groups)

data = [solve((line, 0, groups)) for line, groups in INPUT_DATA]
print(sum(data))