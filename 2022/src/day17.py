from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = deque([x for x in INPUT_DATA[0]])
orig_input = list(INPUT_DATA)

width = 7

shape_list = deque(['-', '+', 'L', '|', '▮' ])
orig_shapes = list(shape_list)
shapes = {
    '-': {
        'layout': [
            0+0j, 1+0j, 2+0j, 3+0j
        ],
        'leftedge': 0+0j,
        'bottom': [ 0+0j, 1+0j, 2+0j, 3+0j ],
        'width': 4,
        'height': 1
    },
    '+': {
        'layout': [
            1+0j, 0-1j, 1-1j, 2-1j, 1-2j
        ],
        'leftedge': 0-1j,
        'bottom': [ 1+0j ],
        'width': 3,
        'height': 3
    },
    'L': {
        'layout': [
            0+0j, 1+0j, 2+0j, 2-1j, 2-2j
        ],
        'leftedge': 0+0j,
        'bottom': [ 0+0j, 1+0j, 2+0j ],
        'width': 3,
        'height': 3
    },
    '|': {
        'layout': [
            0+0j, 0-1j, 0-2j, 0-3j
        ],
        'leftedge': 0+0j,
        'bottom': [ 0+0j ],
        'width': 1,
        'height': 4
    },
    '▮': {
        'layout': [
            0+0j, 1+0j, 0-1j, 1-1j
        ],
        'leftedge': 0+0j,
        'bottom': [ 0+0j, 1+0j ],
        'width': 2,
        'height': 2
    },
}

directions = {
    '>': 1+0j,
    "<": -1+0j,
}

grid = defaultdict(lambda: '.')
for x in range(-1, 8):
    grid[x+4j] = '-'

for y in range(-10000000, 5):
    grid[complex(-1, y)] = '|'
    grid[complex(7, y)] = '|'

print("Made grid.")
left_start   = 2+0j
bottom       = 0+0j
current_char = None
current_pos  = []
# Part 1
changes = ""
i = 0
def do_fall(upper_bound, part2 = False):
    global i, changes, current_char, current_pos, bottom
    while i < upper_bound:
        if part2 and i > (len(INPUT_DATA) // 3):
            substr = longestRepeatedSubstring(changes)
            num_rocks = len(substr)
            index  = changes.index(substr)
            if changes[index + num_rocks:index + 2 * num_rocks] == substr:
                total_increase = sum([int(x) for x in substr])
                new_bottom = abs(int(bottom.imag))
                while i + num_rocks < upper_bound:
                    new_bottom += total_increase
                    i += num_rocks

                # Remaining
                if i < upper_bound:
                    new_bottom += sum([int(x) for x in substr[0:(upper_bound - i)]])
                print()
                print(new_bottom)
                exit()

        if current_char is None:
            current_char = shape_list[0]
            shape_list.rotate(-1)

            # Need to spawn the shape now
            start = left_start + bottom
            current_pos = [start + x for x in shapes[current_char]['layout']]

        char = INPUT_DATA[0]
        INPUT_DATA.rotate(-1)
        dir = directions[char]
        if any([grid[x+dir] != '.' for x in current_pos]):
            # We hit a wall or rocks. This movement doesn't happen.
            pass
        else:
            current_pos = [x+dir for x in current_pos]

        # Now that we've moved left or right, we have to handle down.
        dir = 0+1j
        if any([grid[x + dir] != '.' for x in current_pos]):
            i += 1
            prev_bottom = bottom
            bottom = complex(0, min([int(x.imag) - 4 for x in current_pos] + [int(bottom.imag)]))
            changes += f"{int(prev_bottom.imag - bottom.imag)}"
            #print(f"Found rock {i}, {bottom}, {int(prev_bottom.imag - bottom.imag)}, {current_char}")
            # We're going to hit something, so we stop here without moving.
            for x in current_pos:
                grid[x] = '#'
            current_char = None
            current_pos  = None
            print(f"{i}", end="\r")
        else:
            current_pos = [x + dir for x in current_pos]

do_fall(2022)
print(bottom)
print(abs(int(bottom.imag)))

# Part 2
# Returns the longest repeating non-overlapping
# substring in str
def longestRepeatedSubstring(str):
    n = len(str)
    LCSRe = [[0 for x in range(n + 1)]
             for y in range(n + 1)]

    res = ""  # To store result
    res_length = 0  # To store length of result

    # building table in bottom-up manner
    index = 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):

            # (j-i) > LCSRe[i-1][j-1] to remove
            # overlapping
            if (str[i - 1] == str[j - 1] and
                    LCSRe[i - 1][j - 1] < (j - i)):
                LCSRe[i][j] = LCSRe[i - 1][j - 1] + 1

                # updating maximum length of the
                # substring and updating the finishing
                # index of the suffix
                if (LCSRe[i][j] > res_length):
                    res_length = LCSRe[i][j]
                    index = max(i, index)

            else:
                LCSRe[i][j] = 0

    # If we have non-empty result, then insert
    # all characters from first character to
    # last character of string
    if (res_length > 0):
        for i in range(index - res_length + 1,
                       index + 1):
            res = res + str[i - 1]

    return res

do_fall(1000000000000, True)
print(abs(int(bottom.imag)))