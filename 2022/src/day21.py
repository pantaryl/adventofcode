from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]

class Monkey:
    def __init__(self, id, data):
        self.id   = id
        self.data = data
        if any([x in data for x in ['+', '-', '/', '*']]):
            self.isEquation = True
            self.lhs, eq, self.rhs = parse("{} {} {}", data)

            if eq == '+':
                self.eq = lambda x, y: x + y
                self.opp = '-'
            elif eq == '-':
                self.eq = lambda x, y: x - y
                self.opp = '+'
            elif eq == '/':
                self.eq = lambda x, y: x // y
                self.opp = '*'
            elif eq == '*':
                self.eq = lambda x, y: x * y
                self.opp = '/'
            elif eq == '=':
                self.eq = lambda x, y: x == y
            else:
                assert False, "What is this?"
        else:
            self.isEquation = False
            self.value      = parse("{:d}", data)[0]

    def __copy__(self):
        temp = Monkey(self.id, self.data)
        if self.isEquation:
            temp.eq = self.eq
        else:
            temp.value = self.value

    def __repr__(self):
        val = f"{self.id} - "
        if self.isEquation:
            val += self.data
        else:
            val += f"{self.value}"
        return val

monkeys = {}

for line in INPUT_DATA:
    id, data = parse("{}: {}", line)
    monkeys[id] = Monkey(id, data)

# Part 1
while any([monkey.isEquation is True for id, monkey in monkeys.items()]):
    for id, monkey in monkeys.items():
        if monkey.isEquation:
            lhs, rhs = monkey.lhs, monkey.rhs

            assert(lhs in monkeys and rhs in monkeys)
            lhs, rhs = monkeys[lhs], monkeys[rhs]
            if lhs.isEquation is False and rhs.isEquation is False:
                newValue = monkey.eq(lhs.value, rhs.value)
                monkey.isEquation = False
                monkey.value      = newValue

print(monkeys['root'].value)

# Part 2
monkeys = {}

for line in INPUT_DATA:
    id, data = parse("{}: {}", line)
    monkeys[id] = Monkey(id, data)

    if id == 'root':
        monkeys[id].eq = lambda x, y: x == y
    elif id == 'humn':
        monkeys[id].isEquation = None
        monkeys[id].value      = None

seen_lhs  = set()
seen_rhs  = set()
stack = [ (monkeys['root'].lhs, seen_lhs), (monkeys['root'].rhs, seen_rhs) ]
while stack:
    value, tracker = stack.pop()
    tracker.add(value)

    monkey = monkeys[value]
    if monkey.isEquation:
        if monkey.lhs not in tracker:
            stack.append((monkey.lhs, tracker))
        if monkey.rhs not in tracker:
            stack.append((monkey.rhs, tracker))

known = seen_lhs if 'humn' not in seen_lhs else seen_rhs
unknown = seen_rhs if 'humn' not in seen_lhs else seen_lhs
known_id = monkeys['root'].lhs if 'humn' not in seen_lhs else monkeys['root'].rhs
unknown_id = monkeys['root'].rhs if 'humn' not in seen_lhs else monkeys['root'].lhs

# Resolve the "known" side, which ensures that one side of the root is evaluated.
while any([monkeys[id].isEquation is True for id in known]):
    for id in known:
        monkey = monkeys[id]
        if monkey.isEquation:
            lhs, rhs = monkey.lhs, monkey.rhs

            assert(lhs in monkeys and rhs in monkeys)
            lhs, rhs = monkeys[lhs], monkeys[rhs]
            if lhs.isEquation is False and rhs.isEquation is False:
                newValue = monkey.eq(lhs.value, rhs.value)
                monkey.isEquation = False
                monkey.value      = newValue

def DFS(node, visited: set):
    visited.add(node)

    monkey = monkeys[node]
    if monkey.isEquation:
        lhs, rhs = monkey.lhs, monkey.rhs
        if monkeys[lhs].isEquation:
            DFS(lhs, visited)
        if monkeys[rhs].isEquation:
            DFS(rhs, visited)

        if monkeys[lhs].isEquation is False and monkeys[rhs].isEquation is False:
            newValue = monkey.eq(monkeys[lhs].value, monkeys[rhs].value)
            monkey.isEquation = False
            monkey.value = newValue

def DFS_2(node, visited: set):
    visited.add(node)

    monkey = monkeys[node]
    assert(hasattr(monkey, 'value'))

    if monkey.isEquation:
        lhs, rhs = monkey.lhs, monkey.rhs

        # One of these should be known by now.
        lhs_known = monkeys[lhs].isEquation is False
        known = lhs if lhs_known else rhs
        unknown = lhs if lhs_known is False else rhs

        known_value = monkeys[known].value
        if monkey.opp == '+':
            if lhs_known:
                # x - y = parent
                # x - parent = y
                monkeys[unknown].value = known_value - monkey.value
            else:
                # x - y = parent
                # x = parent + y
                monkeys[unknown].value = monkey.value + known_value
        elif monkey.opp == '-':
            # Left or right, this is the same equation.
            # x + y = parent
            # y = parent - x
            # x = parent - y
            monkeys[unknown].value = monkey.value - known_value
        elif monkey.opp == '/':
            # Left or right, this is the same equation
            # x * y = parent
            # x = parent // y
            # y = parent // x
            monkeys[unknown].value = monkey.value // known_value
        elif monkey.opp == '*':
            if lhs_known:
                # x / y = parent
                # y = x / parent
                monkeys[unknown].value = known_value // monkey.value
            else:
                # x / y = parent
                # x = parent * y
                monkeys[unknown].value = monkey.value * known_value

        DFS_2(unknown, visited)

# Resolve all the nodes we can on the unknown side.
DFS(unknown_id, set())

# Once we've resolved what we can and have evaluated the known side,
# we can start trying to resolve the unknown side.
monkeys[unknown_id].value = monkeys[known_id].value
DFS_2(unknown_id, set())

# Print the value associated with the human.
print(monkeys['humn'].value)