from shared import *

# Input data is in INPUT_DATA.
# INPUT_DATA = [int(x) for x in INPUT_DATA]

numbers_drawn = [int(x) for x in INPUT_DATA[0].split(',')]

class Bingo:
    def __init__(self, state):
        self.grid = state
        self.grid: list
        assert(isinstance(state, list))
        assert(len(self.grid) == 25)

    def five_win(self, dataList: set):
        return len(dataList) == 1 and None in dataList

    def mark(self, val):
        for i, item in enumerate(self.grid):
            if item == val:
                self.grid[i] = None

    def winner(self):
        win = self.five_win(set(self.grid[0:5]))
        win |= self.five_win(set(self.grid[5:10]))
        win |= self.five_win(set(self.grid[10:15]))
        win |= self.five_win(set(self.grid[15:20]))
        win |= self.five_win(set(self.grid[20:25]))
        win |= self.five_win(set(self.grid[0::5]))
        win |= self.five_win(set(self.grid[1::5]))
        win |= self.five_win(set(self.grid[2::5]))
        win |= self.five_win(set(self.grid[3::5]))
        win |= self.five_win(set(self.grid[4::5]))
        return win

boards = []

data = INPUT_DATA[2:]
index = 0
while index < len(data):
    board = " ".join(data[index:index + 5])
    board = [int(x) for x in board.split(" ") if x not in [" ", '']]
    boards.append(Bingo(board))
    index += 6

part1 = 0
part2 = 0
for item in numbers_drawn:
    winner = None
    for board in list(boards):
        board.mark(item)
        if board.winner():
            if winner is None: winner = board
            boards.remove(board)

    if winner:
        if part1 == 0:
            part1 = item * sum([x for x in winner.grid if x])

        if len(boards) == 0:
            part2 = item * sum([x for x in winner.grid if x])
            break

print(part1)
print(part2)