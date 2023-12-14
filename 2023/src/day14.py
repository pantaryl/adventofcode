from shared import *

grid = Grid(INPUT_DATA)

balls = sorted([pos for pos, value in grid.items() if value == "O"], key=lambda x: x.imag)

def move_ball():
    balls = sorted([pos for pos, value in grid.items() if value == "O"], key=lambda x: x.imag)

    for ball_pos in balls:
        y_val = int(ball_pos.imag)
        while y_val > 0 and grid[complex(ball_pos.real, y_val - 1)] == '.':
            y_val -= 1
        if y_val == int(ball_pos.imag):
            continue
        grid[complex(ball_pos.real, y_val)] = "O"
        grid[ball_pos] = '.'

def calc_score():
    return sum([grid.height - int(pos.imag) for pos, value in grid.items() if value == "O"])

move_ball()
print(calc_score())

grid = Grid(INPUT_DATA)
DP = {}
result = None
iterations = 1000000000
for i in range(iterations):
    grid_hash = hash(grid)
    if grid_hash in DP:
        result = DP[grid_hash][0], i - DP[grid_hash][0]
        break
    DP[grid_hash] = (i, calc_score())

    for rot in range(4):
        move_ball()
        grid.rotate(1)

states = {i[0]: i[1] for state, i in DP.items()}
state  = states[result[0] + ((1000000000 - result[0]) % result[1])]
print(state)