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