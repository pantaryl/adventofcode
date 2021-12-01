from datetime import datetime
from enum import Enum

class TokenType(Enum):
    GUARD = 0
    SLEEP = 2
    WAKE  = 1

class Token():
    def __init__(self, string):
        timestamp = string[0:18]
        info      = string[19:]

        self.time = datetime.strptime(timestamp, "[%Y-%m-%d %H:%M]")
        if "Guard" in info:
            self.type = TokenType.GUARD
            self.data = info.split(" ")[1].replace("#", "")
        elif "wakes" in info:
            self.type = TokenType.WAKE
            self.data = 0
        elif "asleep" in info:
            self.type = TokenType.SLEEP
            self.data = 0

    def __lt__(self, other):
        return self.time < other.time

# Split the file into a token stream
tokens = []
with open("../input/day4.txt", 'r') as inputFile:
    lines = inputFile.readlines()
    for line in lines:
        tokens.append(Token(line.rstrip()))

# Sort it in time order
tokens.sort()

guards = {}
currentGuard = None
sleepTime = None
for token in tokens:
    if token.type == TokenType.GUARD:
        if currentGuard is not None and sleepTime is not None:
            for i in range(sleepTime, 60):
                guards[currentGuard][i] += 1
        currentGuard = token.data
        sleepTime    = None
        if currentGuard not in guards:
            guards[currentGuard] = [0 for i in range(0, 60)]
    elif token.type == TokenType.SLEEP:
        assert(sleepTime == None)
        sleepTime = token.time.minute
    elif token.type == TokenType.WAKE:
        for i in range(sleepTime, token.time.minute):
            guards[currentGuard][i] += 1
        sleepTime = None

# Part 1
maxSleepTime  = 0
maxSleepGuard = None
for guard, times in guards.items():
    maxTime = sum(times)
    if maxTime > maxSleepTime:
        maxSleepTime = maxTime
        maxSleepGuard = guard
minute = guards[maxSleepGuard].index(max(guards[maxSleepGuard]))
print(int(maxSleepGuard) * minute)

# Part 2
maxSleepTime  = 0
maxSleepGuard = None
for guard, times in guards.items():
    maxTime = max(times)
    if maxTime > maxSleepTime:
        maxSleepTime = maxTime
        maxSleepGuard = guard
minute = guards[maxSleepGuard].index(maxSleepTime)
print(int(maxSleepGuard) * minute)