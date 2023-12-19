from shared import *

class Part:
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def __repr__(self):
        return f"{{x={self.x},m={self.m},a={self.a},s={self.s}}}"

parts = set()
workflows = {}
parseParts = False
for i, line in enumerate(INPUT_DATA):
    if line == "":
        parseParts = True
    elif parseParts:
        x, m, a, s = parse("{{x={:d},m={:d},a={:d},s={:d}}}", line)
        parts.add(Part(x, m, a, s))
    else:
        label, remainder = line.split("{")
        remainder = remainder[:-1]
        rules_text = remainder.split(",")

        rules = []
        for rule in rules_text:
            if ':' in rule:
                condition, jump = rule.split(":")
                rules.append((lambda x: eval(f"x.{condition}"), jump, condition))
            else:
                rules.append((lambda x: True, rule, None))
        workflows[label] = rules

total = 0
for part in parts:
    workflow = 'in'
    while workflow not in ('A', 'R'):
        rules = workflows[workflow]
        for func, jump, condition in rules:
            if func(part):
                workflow = jump
                break

    if workflow == 'A':
        total += part.x + part.m + part.a + part.s
print(total)

def get_new_range(operation, count, lo, hi):
    # We want to adjust our ranges such that we can find the max/min of possible true cases.

    if operation == '>':
        # if 'y > 1000', then our minimum passing lo value is 1001.
        lo = max(lo, count + 1)
    elif operation == '<':
        # if 'y < 1000', then our minimum passing high value is 999.
        hi = min(hi, count - 1)
    elif operation == '>=':
        # if 'y < 1000' originally, then this case is checking the opposite.
        # which means, we need to restrict our lo to the minimum failing case of 1000.
        lo = max(lo, count)
    elif operation == '<=':
        # if 'y > 1000' originally, then this case is checking the opposite.
        # which means, we need to restrict our hi to the minimum failing case of 1000.
        hi = min(hi, count)
    else:
        assert False
    return (lo, hi)

def get_new_range_for_var(
        variable,
        operation,
        count,
        x_lo, x_hi, m_lo, m_hi, a_lo, a_hi, s_lo, s_hi):
    if variable == 'x':
        x_lo, x_hi = get_new_range(operation, count, x_lo, x_hi)
    elif variable == 'm':
        m_lo, m_hi = get_new_range(operation, count, m_lo, m_hi)
    elif variable == 'a':
        a_lo, a_hi = get_new_range(operation, count, a_lo, a_hi)
    elif variable == 's':
        s_lo, s_hi = get_new_range(operation, count, s_lo, s_hi)
    return (x_lo, x_hi, m_lo, m_hi, a_lo, a_hi, s_lo, s_hi)

total = 0
stack = deque([('in', 1, 4000, 1, 4000, 1, 4000, 1, 4000)])
while stack:
    workflow, x_lo, x_hi, m_lo, m_hi, a_lo, a_hi, s_lo, s_hi = stack.pop()

    if workflow == 'A':
        # The total number of valid combinations is the multiple of all possible ranges.
        total += ((x_hi - x_lo + 1) *
                  (m_hi - m_lo + 1) *
                  (a_hi - a_lo + 1) *
                  (s_hi - s_lo + 1))
        continue
    elif workflow == 'R':
        # Ignore any rejected workflows.
        continue
    else:
        rules = workflows[workflow]
        for func, jump, condition in rules:
            if condition:
                variable  = condition[0]
                operation = condition[1]
                count     = int(condition[2:])

                # Add the case where we passed the condition to our stack.
                stack.append((jump,
                              *get_new_range_for_var(variable,
                                                     operation,
                                                     count,
                                                     x_lo,
                                                     x_hi,
                                                     m_lo,
                                                     m_hi,
                                                     a_lo,
                                                     a_hi,
                                                     s_lo,
                                                     s_hi)))

                # Now, we need to traverse the case where we didn't pass the condition.
                # For this case, we want to restrict the range to the opposite of the operation ('<' becomes '>='),
                # because otherwise we would have passed the condition.
                x_lo, x_hi, m_lo, m_hi, a_lo, a_hi, s_lo, s_hi = get_new_range_for_var(variable,
                                                                                       '<=' if operation == '>' else '>=',
                                                                                       count,
                                                                                       x_lo,
                                                                                       x_hi,
                                                                                       m_lo,
                                                                                       m_hi,
                                                                                       a_lo,
                                                                                       a_hi,
                                                                                       s_lo,
                                                                                       s_hi)
            else:
                # For non-conditional jumps, add it to the stack with the current values.
                stack.append((jump,
                              x_lo,
                              x_hi,
                              m_lo,
                              m_hi,
                              a_lo,
                              a_hi,
                              s_lo,
                              s_hi))
                break
print(total)