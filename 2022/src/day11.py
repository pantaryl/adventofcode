from shared import *

# Input data is in INPUT_DATA.
class Monkey:
    def __init__(self, id, starting_items, operation, test, trueResult, falseResult):
        self.id = id

        self.orig_items = deepcopy(starting_items)
        self.current_items = deepcopy(starting_items)
        self.operation = operation
        self.test = test
        self.trueResult = trueResult
        self.falseResult = falseResult
        self.inspections = 0

    def __copy__(self):
        return Monkey(self.id,
                      self.orig_items,
                      self.operation,
                      self.test,
                      self.trueResult,
                      self.falseResult,
                      kwargs=self.kwargs)

    def doOperation(self, value):
        rhs = value if self.operation[1] == "old" else int(self.operation[1])

        if self.operation[0] == '+':
            return value + rhs
        elif self.operation[0] == '-':
            return value - rhs
        elif self.operation[0] == '/':
            return value // rhs
        elif self.operation[0] == '*':
            return value * rhs

        assert()

    def inspect(self, isPartTwo: bool):
        self.inspections += 1

        unique, value = self.current_items[0]

        value = self.doOperation(value)

        if not isPartTwo:
            value //= 3
        value %= total_test

        return (unique, value)

    def doTest(self, item, players: List["Monkey"]):
        unique, value = item
        if value % self.test == 0:
            players[self.trueResult].receive(item)
        else:
            players[self.falseResult].receive(item)
        self.current_items.popleft()

    def receive(self, item):
        self.current_items.append(item)

    def round(self, isPartTwo: bool, players: List["Monkey"]):
        while len(self.current_items) > 0:
            item = self.inspect(isPartTwo)
            self.doTest(item, players)

unique = 0
monkeys = []
monkey  = None
line_num = 0
total_test = 1

while line_num < len(INPUT_DATA):
    line = INPUT_DATA[line_num]
    if line == "":
        monkeys.append(Monkey(id=len(monkeys),
                              starting_items=starting_items,
                              operation=operation, test=test,
                              trueResult=trueResult,
                              falseResult=falseResult))
        monkey = None
    elif "Monkey" in line:
        assert(monkey is None)
        monkey = True
    elif line.lstrip().startswith("Starting items"):
        starting_items = deque()
        for x in line.split(': ')[1].split(','):
            starting_items.append((unique, int(x)))
            unique += 1
    elif line.lstrip().startswith("Operation"):
        operation = parse("new = old {} {}", line.split(": ")[1])
    elif line.lstrip().startswith("Test"):
        test = parse("divisible by {:d}", line.split(": ")[1])[0]
        total_test *= test
    elif line.lstrip().startswith("If true:"):
        trueResult = parse("throw to monkey {:d}", line.split(": ")[1])[0]
    elif line.lstrip().startswith("If false:"):
        falseResult = parse("throw to monkey {:d}", line.split(": ")[1])[0]

    line_num += 1

assert(monkey is not None)
monkeys.append(Monkey(id=len(monkeys),
                      starting_items=starting_items,
                      operation=operation, test=test,
                      trueResult=trueResult,
                      falseResult=falseResult))
monkey = None

# Part 1
part1 = deepcopy(monkeys)
for round in range(0, 20):
    for i, monkey in enumerate(part1):
        monkey.round(isPartTwo=False, players=part1)

inspections = sorted([x.inspections for x in part1])
print(inspections[-1] * inspections[-2])

# Part 2
part2 = deepcopy(monkeys)
for round in range(0, 10000):
    for i, monkey in enumerate(part2):
        monkey.round(isPartTwo=True, players=part2)

inspections = sorted([x.inspections for x in part2])
print(inspections[-1] * inspections[-2])