from shared import *

INPUT_DATA = [parse("{:d}, {:d}, {:d} @ {:d}, {:d}, {:d}", x) for x in INPUT_DATA]

MIN = 200000000000000
MAX = 400000000000000
matches = set()
# y = mx + b
# First find b
for i, first in enumerate(INPUT_DATA):
    x1, y1, z1, vx1, vy1, vz1 = first
    # y1 - (vy1 / vx1) * x1 = b
    m1 = (vy1 / vx1)
    b1 = y1 - m1 * x1
    for j, second in enumerate(INPUT_DATA):
        if i == j: continue
        if (i, j) in matches or (j, i) in matches: continue

        #print(f"Hailstone {i}: {first}")
        #print(f"Hailstone {j}: {second}")

        x2, y2, z2, vx2, vy2, vz2 = second
        m2 = (vy2 / vx2)
        b2 = y2 - m2 * x2

        if math.isclose(m1, m2):
            #print("Hailstones are parallel!\n")
            continue

        # y1 = m1 * x + b1
        # y2 = m2 * x + b2
        #
        # m1 * x + b1 = m2 * x + b2
        # x = (b1 - b2) / (m2 - m1)

        x = (b1 - b2) / (m2 - m1)

        y1_intersect = m1 * x + b1
        y2_intersect = m2 * x + b2

        if math.isclose(y1_intersect, y2_intersect) and MIN <= x <= MAX and MIN <= y1_intersect <= MAX:
            if ((vx1 < 0 and x > x1) or
                (vx1 > 0 and x < x1) or
                (vx2 < 0 and x > x2) or
                (vx2 > 0 and x < x2) or
                (vy1 < 0 and y1_intersect > y1) or
                (vy1 > 0 and y1_intersect < y1) or
                (vy2 < 0 and y2_intersect > y2) or
                (vy2 > 0 and y2_intersect < y2)):
                pass
                #print("Hailstones' paths crossed in the past for both hailstones.")
            else:
                matches.add((i, j))
                matches.add((j, i))
                #print(f"Hailstones' paths will cross inside the test area (at x={x}, y={y1_intersect}).")
        else:
            pass
            #print(f"Will not intersect! x={x}, y1={y1_intersect}, y2={y2_intersect}")
        #print()

print(len(matches) // 2)

from z3 import *

x = Real('x')
y = Real('y')
z = Real('z')

a = Real('a')
b = Real('b')
c = Real('c')

s = Solver()

for i, vec in enumerate(INPUT_DATA):
    x1, y1, z1, vx1, vy1, vz1 = vec

    t = Real(f't{i}')

    s.add(x + t * a == x1 + t * vx1)
    s.add(y + t * b == y1 + t * vy1)
    s.add(z + t * c == z1 + t * vz1)

if s.check() == sat:
    m = s.model()
    print(sum(int(str(m.evaluate(v))) for v in (x, y, z)))