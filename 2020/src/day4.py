with open("../input/day4.txt", 'r') as inputFile:
    data = inputFile.readlines()

def makePassports(inputData):
    passports       = []
    currentPassport = {}
    for line in inputData:
        line = line.rstrip()
        if line == "" or line == "\n":
            passports.append(currentPassport)
            currentPassport = {}
        else:
            splitLine = line.split(" ")
            for split in splitLine:
                key, value = split.split(":")
                currentPassport[key] = value
    passports.append(currentPassport)
    return passports

def part1DetermineLegalPassport(passport):
    required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    return required.issubset(set(passport.keys()))

passports = makePassports(data)

# Part 1
print(sum([1 if part1DetermineLegalPassport(passport) else 0 for passport in passports]))

# Part 2
def part2DetermineLegalPassport(passport):
    validStatus = []
    containsAllNecessaryParts = part1DetermineLegalPassport(passport)
    validStatus.append(containsAllNecessaryParts)

    if containsAllNecessaryParts:
        # Check birth year:
        def verifyByr(byr):
            return len(byr) == 4 and 2002 >= int(byr) >= 1920
        def verifyIyr(iyr):
            return len(iyr) == 4 and 2020 >= int(iyr) >= 2010
        def verifyEyr(eyr):
            return len(eyr) == 4 and 2030 >= int(eyr) >= 2020
        def verifyHgt(hgt):
            return ('in' in hgt and 76 >= int(hgt[:-2]) >= 59) or ('cm' in hgt and 193 >= int(hgt[:-2]) >= 150)
        def verifyHcl(hcl):
            try:
                int(hcl[1:], 16)
            except:
                return False
            else:
                return hcl.startswith('#')
        def verifyEcl(ecl):
            return ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        def verifyPid(pid):
            return len(pid) == 9 and str.isnumeric(pid)

        verificationFuncs = {
            'byr' : verifyByr,
            'iyr' : verifyIyr,
            'eyr' : verifyEyr,
            'hgt' : verifyHgt,
            'hcl' : verifyHcl,
            'ecl' : verifyEcl,
            'pid' : verifyPid
        }
        for key, func in verificationFuncs.items():
            validStatus.append(func(passport[key]))

    return all(validStatus)

print(sum([1 if part2DetermineLegalPassport(passport) else 0 for passport in passports]))

