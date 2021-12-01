from collections import defaultdict
from helpers import memoize
from copy import deepcopy
from enum import Enum
import time
import os
from math_utils import *
import re

# Complex numbers in Python! == i + nj (x + ny), good for coordinates
# complex*+imaginary to rotate left/ccw, complex*-imaginary to rotate right/cw
# For example:
# Rotate CCW by 270 degrees:
#    val *= complex(0, 1) ** 3 [each power represents 90 degrees]

with open(f"../input/{os.path.splitext(os.path.basename(__file__))[0]}.txt", 'r') as inputFile:
    data = [x.rstrip() for x in inputFile.readlines()]
    #data = [int(x) for x in data]

# There are two ways to solve this, both recursive in nature.
# The first way is by understanding that the grammar for the input is essentially regular expressions, and then
# abusing the regular expression engine to solve it.
# Part 2 of the day's problem adds loops, so you solve this in regex by setting a maximum depth. I chose 100
# arbitrarily.
rules = {}
messages = []
for line in data:
    if ':' in line:
        splitLine = line.split()
        rules[splitLine[0][:-1]] = " ".join(splitLine[1:])
    elif not line:
        continue
    else:
        messages.append(line)

def getRegex(ruleNum, depth):
    rule = rules[ruleNum]

    if '\"' in rule:
        return rule[1] # this is our single character
    elif depth >= 100:
        return ""
    else:
        options = rule.split(" | ")
        regexes = []
        for option in options:
            numbers = option.split()
            regexes.append(''.join([getRegex(number, depth + 1) for number in numbers]))
        return '(?:' + '|'.join(regexes) + ')'

start = time.time()
ruleZero = getRegex('0', 0)
part1 = 0
for message in messages:
    if re.fullmatch(ruleZero, message):
        part1 += 1
print(f"Regex Part1: {part1}")

# Part 2 requires us to update the rules a bit.
rules['8']  = '42 | 42 8'
rules['11'] = '42 31 | 42 11 31'
ruleZero = getRegex('0', 0)
part2 = 0
for message in messages:
    if re.fullmatch(ruleZero, message):
        part2 += 1
print(f"Regex Part2: {part2}")
end = time.time()
print(f"Regex Time(s): {end - start}")

# The second way to do this is with a CYK algorithm: https://en.wikipedia.org/wiki/CYK_algorithm
# If my input message is a string consisting of N characters (a1 .. aN),
# And if my grammar contains symbols (r1 .. rN) with start symbol r1,
# And if my memoization contains a key (0..N, 0..N, r) referring to boolean matches, then:
#
# For the first level of the message (full message), if a character correlates to exactly one piece of the grammar, then
#     memo[(start,end,rule)] = True, where s is the start of the message, end is the end of the message, and rule is the active grammar.
#
# Then, for the rest of the levels of the message (1 .. len(message)):
#
# for level in range(2, len(message)): # Level of message, shortening the message by one character each time
#    for start in range(1, len(message) - level + 1): # Start of my span
#        for partition in range(1, level - 1): # Partition of span
#            for each option in the rule:
#                if memo[(start, partition, option[0])] and memo[partition, len(message), option[1:])]:
#                    memo[(start, len(message), rule)] = True
#
# if memo[(0, len(message), rule)] is True:
#    This is a valid message.

grammar  = {}
expanded = {}
memo     = {}
def matchSubset(message, start, end, options):
    if start == end and (options is None or len(options) == 0):
        return True
    elif start == end:
        return False
    elif options is None or len(options) == 0:
        return False

    match = False
    for i in range(start + 1, end + 1):
        if isMatch((start, i, options[0]), message) and matchSubset(message, i, end, options[1:]):
            match = True
    return match

def isMatch(key, message):
    if key in memo:
        return memo[key]

    start   = key[0]
    end     = key[1]
    ruleNum = key[2]

    match   = False
    if ruleNum in expanded:
        match = message[start:end] == expanded[ruleNum]
    else:
        for option in grammar[ruleNum]:
            if matchSubset(message, start, end, option):
                match = True

    memo[key] = match
    return match


def solve(fixes):
    memo.clear()
    grammar.clear()
    expanded.clear()

    count = 0
    for line in data:
        if ':' in line:
            splitLine = line.split()
            ruleNum   = splitLine[0][:-1] # Trim off the ':'

            rest = fixes.get(ruleNum, " ".join(splitLine[1:]))
            if '"' in rest:
                expanded[ruleNum] = rest[1:-1] # This is one of our defined a's or b's.
            else:
                halves = rest.split(" | ")
                grammar[ruleNum] = [x.split() for x in halves]
        elif line:
            memo.clear()
            if isMatch((0, len(line), '0'), line):
                count += 1
    return count

start = time.time()
print(f"CYK Part1: {solve({})}")
print(f'CYK Part2: {solve({"8" : "42 | 42 8", "11": "42 31 | 42 11 31"})}')
end = time.time()

print(f"CYK Time(s): {end - start}")