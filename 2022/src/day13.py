from shared import *

# Need to make sure that the last entry is an empty line for my parsing to work.
if INPUT_DATA[-1] != "": INPUT_DATA.append("")

# Input data is in INPUT_DATA.
INPUT_DATA = [INPUT_DATA[line_num-2:line_num] for line_num, x in enumerate(INPUT_DATA) if x == ""]

verbose = False

# Return 1 if left is in the right order, -1 if it isn't, and 0 if left and right are equivalent.
def compare(left, right, indent=0):
    if verbose: print((" " * indent) + f"- Compare {left} vs. {right}")

    left_type  = isinstance(left, int)
    right_type = isinstance(right, int)

    if left_type == right_type:
        if not left_type:
            # Both lists
            for i in range(len(left)):
                if i >= len(right):
                    if verbose: print((" " * (indent+1)) + "- Right side ran out of items, so inputs are in the right order")
                    return -1

                left_win = compare(left[i], right[i], indent=indent+1)
                if left_win == 0:
                    continue
                elif left_win == -1:
                    return -1
                else:
                    return 1
            if len(left) == len(right):
                return 0
            else:
                if len(left) < len(right):
                    if verbose: print((" " * (indent + 1)) + "- Left side ran out of items, so inputs are not in the right order")
                    return 1
                else:
                    # Should never be able to hit this case.
                    assert()
                    return -1
        else:
            # Both ints
            if left == right:
                return 0
            else:
                if left < right:
                    if verbose: print((" " * (indent+1)) + "- Left side is smaller, so inputs are in the right order")
                    return 1
                else:
                    if verbose: print((" " * (indent+1)) + "- Right side is smaller, so inputs are not in the right order")
                    return -1
    elif right_type:
        # Right is an int, left is a list.
        right = [ right ]
        return compare(left, right, indent=indent+1)
    elif left_type:
        # Left is an int, right is a list.
        left = [ left ]
        return compare(left, right, indent=indent+1)


# Part 1
right_order = 0

for i, pair in enumerate(INPUT_DATA, 1):
    # We can first get rid of the outside brackets.
    left  = eval(pair[0])
    right = eval(pair[1])

    if verbose: print(f"== Pair {i} ==")
    if compare(left, right) in [0, 1]:
        if verbose: print(i)
        right_order += i

print(right_order)

# Part 2
total_list = []
for left, right in INPUT_DATA:
    total_list.append(eval(left))
    total_list.append(eval(right))

total_list.append([[2]])
total_list.append([[6]])

total_list = sorted(total_list, key=functools.cmp_to_key(compare), reverse=True)
if verbose: pprint.PrettyPrinter().pprint(total_list)

print((total_list.index([[2]]) + 1) * (total_list.index([[6]]) + 1))