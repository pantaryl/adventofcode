import string

with open("../input/day24.txt", 'r') as inputFile:
    data = inputFile.readlines()

class Group():
    def __init__(self, numUnits, hitPoints, damage, dmgType, immunities=None, weakness=None, initiative=0, isInfection=False, id=0):
        self.numUnits   = numUnits
        self.hp         = hitPoints
        self.immunities = [] if immunities is None else immunities
        self.weakness   = [] if weakness is None else weakness
        self.damage     = damage
        self.dmgType    = dmgType
        self.initiative = initiative
        self.isInfection = isInfection
        self.id = id

    def effectivePower(self):
        return self.numUnits * self.damage

    def determineDamage(self, other):
        if self.dmgType in other.immunities:
            return 0
        elif self.dmgType in other.weakness:
            return self.effectivePower()*2
        else:
            return self.effectivePower()

    def takeDamage(self, damage):
        unitsKilled = damage // self.hp
        self.numUnits -= unitsKilled
        return self.numUnits <= 0, unitsKilled

    def __repr__(self):
        return str(self.numUnits) + str(self.immunities) + str(self.weakness) + self.dmgType

def generateInput(boost=0):
    infection = []
    immune    = []

    isImmune = False
    for line in data:
        if '' == line.rstrip(): continue
        if 'Immune' in line:
            isImmune = True
        elif 'Infection' in line:
            isImmune = False
        else:
            values = line.rstrip().split(" ")
            numUnits = hp = damage = dmgType = initiative = None
            immunities = []
            weakness = []
            i = 0
            while i < len(values):
                value = values[i]
                if numUnits is None and value.isdigit():
                    numUnits = int(value)
                elif hp is None and value.isdigit():
                    hp = int(value)
                elif 'immune' in value:
                    i+=2
                    while True:
                        newData = values[i].translate(str.maketrans('','',string.punctuation))
                        immunities.append(newData)
                        if ')' in values[i] or ';' in values[i]:
                            break
                        else:
                            i+=1
                elif 'weak' in value:
                    i+=2
                    while True:
                        newData = values[i].translate(str.maketrans('','',string.punctuation))
                        weakness.append(newData)
                        if ')' in values[i] or ';' in values[i]:
                            break
                        else:
                            i+=1
                elif damage is None and value.isdigit():
                    damage  = int(value)
                    if isImmune: damage += boost
                    i += 1
                    dmgType = values[i]
                elif initiative is None and value.isdigit():
                    initiative = int(value)
                i += 1

            id = len(immune) if isImmune else len(infection)
            group = Group(numUnits, hp, damage, dmgType, immunities, weakness, initiative, isInfection=(isImmune==False), id=id)
            if isImmune:
                immune.append(group)
            else:
                infection.append(group)
    return immune, infection

def runSimulation(boost=0):
    immune, infection = generateInput(boost=boost)
    allGroups = immune + infection
    while len(immune) > 0 and len(infection) > 0:
        targetOrder = sorted(allGroups, key=lambda x: (x.effectivePower(), x.initiative), reverse=True)
        attackSide    = {}
        defendSide    = {}
        for group in targetOrder:
            targetArmy = immune if group.isInfection else infection
            choices    = sorted([(group.determineDamage(x), x.effectivePower(), x.initiative, x, x.hp) if x not in defendSide else (0, 0, 0, None, 0) for x in targetArmy])
            bestChoice = choices[-1]
            if bestChoice[0] == 0:
                bestChoice = (0, 0, 0, None, 0)
            attackSide[group] = bestChoice[3]
            defendSide[bestChoice[3]] = group

        attackOrder = sorted(allGroups, key=lambda x: x.initiative, reverse=True)
        damageDone = 0
        for group in attackOrder:
            defendTarget = attackSide[group]
            if defendTarget is None or group.numUnits <= 0 or defendTarget.numUnits <= 0: continue

            damage = group.determineDamage(defendTarget)
            damageDone += damage
            killed, unitsKilled = defendTarget.takeDamage(damage)
            if killed:
                allGroups.remove(defendTarget)
                infection.remove(defendTarget) if defendTarget.isInfection else immune.remove(defendTarget)
        if damageDone == 0: return None

    return max(immune, infection, key=len)

# Part 1
winner = runSimulation()
print("Part1:", sum([x.numUnits for x in winner]))

# Part 2
import sys
winningBoost = sys.maxsize
currentBoost = 1
while True:
    winner = runSimulation(boost=currentBoost)
    if winner and not winner[0].isInfection:
        winningBoost = min(winningBoost, currentBoost)
        currentBoost -= 1
    else:
        if winningBoost - currentBoost == 1:
            print("Part2: {} (boost={})".format(sum([x.numUnits for x in runSimulation(boost=winningBoost)]), winningBoost))
            break
        currentBoost *= 2