from itertools import combinations, permutations
from math import hypot, gcd # Python versions 3.5 and above
from functools import reduce # Python version 3.x
from typing import List

# When encountering problems that deal with unbounded increasing numbers and you need to determine the cycles of them,
# you can simply keep moduloing the growing numbers by the least common multiple (LCM) of all of the cycle intervals.
# This ensures that your numbers do not get unwieldy while still allowing you to test them for the various
# cycles/divisors.
def lcm(integers):
    return reduce(lambda a, b: a * b // gcd(a, b), integers)

# If you're looking for cycles with state changes, record a dict of state: iteration#.
# Then when you find your state again in the dict, you can use a modulo to determine where you will be at the end.
#
#   if hash in dict:
#              # Start  #  # Period     #
#       return dict[hash], i - dict[hash]
#   dict[hash] = i
#
# ...
#
# index = start + ((end_iteration - start) % period)

# To find the area of a strange shaped, closed polygon, apply the shoelace formula.
# https://en.wikipedia.org/wiki/Shoelace_formula
#       running_total += (current.x * next.y) - (current.y * next.x)
# If the area is inclusive (includes the edges), then:
#       running_total += (length_of_line)
# The final solution will be:
#       (running_total // 2) + 1
def shoelace(positions: List[complex], inclusive: bool = False):
    start   = positions[0]
    current = start

    running_total = 0
    edges         = 0
    for i, next in enumerate(positions[1:]):
        running_total += (int(current.real) * int(next.imag)) - \
                         (int(current.imag) * int(next.real))

        edges += int(hypot(int(next.real) - int(current.real),
                           int(next.imag) - int(current.imag)))

        current = next

    running_total += (int(current.real) * int(start.imag)) - \
                     (int(current.imag) * int(start.real))

    edges += int(hypot(int(start.real) - int(current.real),
                       int(start.imag) - int(current.imag)))

    # Area from shoelace:
    area = running_total // 2

    # Pick's theorem
    area = area - edges // 2 + 1

    if inclusive:
        area += edges

    return area

# For 1D segment overlaps:
def overlap_1d(min1, max1, min2, max2):
    return max(0, min(max1, max2) - max(min1, min2)) + \
           1 if max1 <= min2 or min1 <= max2 else 0

def is_power_of_two(n):
    return (n != 0) and (n & (n-1) == 0)

def bit_count(self):
    return bin(self).count("1")

########################################################################################################################
# This came courtesy of some helpful research regarding Chinese Remainder Theorem,
# which is number theory I am 100% not familiar with.

# The modular multiplicative inverse of the product of all primes divided by the current prime (prodDivX),
# with respect to the current prime (x).
def mod_inverse(prodDivX, x):
    return pow(prodDivX, x-2, x)

# Chinese remainder theorem states that there is some number n where:
#    n = ( ∑ (remainder[i] * prodDivX(i) * mod_inverse(prodDivX(i), i) ) % totalProd
# The greek sigma indicates a summation of the above formula for all numbers in the series, denoted by i.
# I saw a problem that needed this in Day13 of 2020: https://adventofcode.com/2020/day/13
def crt(numbers: list, remainders: list):
    totalProd = 1
    for i in range(len(numbers)):
        totalProd *= numbers[i]

    total = 0
    for i in range(len(numbers)):
        prodDivX = totalProd // numbers[i]
        total += remainders[i] * prodDivX * mod_inverse(prodDivX, numbers[i])
    return total % totalProd