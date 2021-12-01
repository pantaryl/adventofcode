from collections import defaultdict
from helpers import memoize
from copy import deepcopy
from enum import Enum
import os
from math_utils import *

# Complex numbers in Python! == i + nj (x + ny), good for coordinates
# complex*+imaginary to rotate left/ccw, complex*-imaginary to rotate right/cw
# For example:
# Rotate CCW by 270 degrees:
#    val *= complex(0, 1) ** 3 [each power represents 90 degrees]

with open(f"../input/{os.path.splitext(os.path.basename(__file__))[0]}.txt", 'r') as inputFile:
    data = [x.rstrip() for x in inputFile.readlines()]
    #data = [int(x) for x in data]

# Part 1
def search(pos, line):
    sum        = 0
    currentOp  = "+"
    while pos < len(line):
        if line[pos] == " ":
            pos += 1
        elif line[pos] in ['*', '+']:
            currentOp = line[pos]
            pos += 2
        elif line[pos] == ')':
            return sum, pos + 1
        elif line[pos] == '(':
            result, pos = search(pos + 1, line)
            if currentOp == '+':
                sum += result
            elif currentOp == '*':
                sum *= result
        else:
            result = 0
            while pos < len(line) and line[pos] not in ['*', '+', ' ', '(', ')']:
                result = (result * 10) + int(line[pos])
                pos += 1
            if currentOp == '+':
                sum += result
            elif currentOp == '*':
                sum *= result
    return sum, pos

part1 = 0
for line in data:
    result, _ = search(0, line)
    part1 += result
print(part1)

# Part 2
class Token(Enum):
    Digit      = 0
    Mult       = 1
    Add        = 2
    ParenStart = 3
    ParenStop  = 4

def simplifyTokens(tokens, highestRefCount):
    # First we want to simplify the parens.
    seeParens  = False
    while highestRefCount > 0:
        origTokenList = deepcopy(tokens)
        tokenSlice  = []
        addTokens   = False
        startRemove = 0
        newHighest  = 0
        removed     = 0
        for i in range(len(origTokenList)):
            token = origTokenList[i]
            if token[0] == Token.ParenStart:
                seeParens = True
                newHighest = max(token[1], newHighest)
                if token[1] == highestRefCount:
                    addTokens = True
                    startRemove = i
                    tokens.pop(i - removed)
                    removed += 1
            elif token[0] == Token.ParenStop:
                seeParens = True
                newHighest = max(token[1], newHighest)
                if token[1] == highestRefCount:
                    addTokens = False
                    tokens.pop(i - removed)
                    removed += 1
                    break
            elif addTokens:
                tokenSlice.append(token)
                tokens.pop(i - removed)
                removed += 1

        if seeParens == False or highestRefCount == 0: break
        elif highestRefCount is not None and highestRefCount > 0: highestRefCount = newHighest

        if tokenSlice:
            newDigits = simplifyTokens(tokenSlice, highestRefCount)
            tokens.insert(startRemove, (Token.Digit, newDigits))


    # Now we should be able to just handle any actual math.
    result  = 0
    idx     = 0
    seenAdd = False
    while len(tokens) > 1:
        try:
            firstAdd = tokens.index((Token.Add, None))
        except ValueError:
            firstAdd = None

        if firstAdd:
            firstDigit  = tokens[firstAdd - 1]
            secondDigit = tokens[firstAdd + 1]
            tokens.pop(firstAdd - 1)
            tokens.pop(firstAdd - 1)
            tokens.pop(firstAdd - 1)
            tokens.insert(firstAdd - 1, (Token.Digit, firstDigit[1] + secondDigit[1]))
        else:
            try:
                firstMul = tokens.index((Token.Mult, None))
            except ValueError:
                firstMul = None

            if firstMul:
                firstDigit  = tokens[firstMul - 1]
                secondDigit = tokens[firstMul + 1]
                tokens.pop(firstMul)
                tokens.remove(firstDigit)
                tokens.remove(secondDigit)
                tokens.insert(firstMul - 1, (Token.Digit, firstDigit[1] * secondDigit[1]))

    result = tokens[0][1]
    return result



def tokenizeLine(line):
    tokens          = []
    pos             = 0
    refCount        = 0
    highestRefCount = 0
    while pos < len(line):
        char = line[pos]
        if char == " ":
            pos += 1
        elif char == '*':
            tokens.append((Token.Mult, None))
            pos += 2
        elif char == '+':
            tokens.append((Token.Add, None))
            pos += 2
        elif char == '(':
            refCount += 1
            highestRefCount = max(highestRefCount, refCount)
            tokens.append((Token.ParenStart, refCount))
            pos += 1
        elif char == ')':
            tokens.append((Token.ParenStop, refCount))
            refCount -= 1
            pos += 1
        else:
            currentVal = 0
            while pos < len(line) and line[pos] not in ['*', '+', ' ', '(', ')']:
                currentVal = (currentVal * 10) + int(line[pos])
                pos += 1
            tokens.append((Token.Digit, currentVal))

    # Time to simplify the tokens.
    result = simplifyTokens(tokens, highestRefCount)

    return result

print(sum([tokenizeLine(line) for line in data]))




