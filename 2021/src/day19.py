from shared import *

# Input data is in INPUT_DATA.
#INPUT_DATA = [int(x) for x in INPUT_DATA]

scanners  = {}
distances = {}
scannerId = None
for line in INPUT_DATA:
    if line:
        if "scanner" in line:
            scannerId = tuple(parse.parse("--- scanner {:d} ---", line).fixed)[0]
            scanners[scannerId] = set()
        else:
            pos = Vector3(*tuple([int(x) for x in line.split(',')]))
            scanners[scannerId].add(pos)


def getSwizzles():
    swizzles = [
        ('x',   'y',   'z'),
        ('-x', '-y',   'z'),
        ('-x',  'y',  '-z'),
        ('x',  '-y',  '-z'),
        ('-x',  'z',   'y'),
        ('x',  '-z',   'y'),
        ('x',   'z',  '-y'),
        ('-x', '-z',  '-y'),

        ('-y',  'x',   'z'),
        ('y',  '-x',   'z'),
        ('y',   'x',  '-z'),
        ('-y', '-x',  '-z'),
        ('y',   'z',   'x'),
        ('-y', '-z',   'x'),
        ('-y',  'z',  '-x'),
        ('y',  '-z',  '-x'),

        ('z',   'x',   'y'),
        ('-z', '-x',   'y'),
        ('-z',  'x',  '-y'),
        ('z',  '-x',  '-y'),
        ('-z',  'y',   'x'),
        ('z',  '-y',   'x'),
        ('z',   'y',  '-x'),
        ('-z', '-y',  '-x'),
    ]
    assert(len(swizzles) == 24)
    return swizzles

# Part 1
# We start by assuming that Scanner0 is in X, Y, Z swizzle,
# and add all of those positions to the found list.
found = set([x for x in scanners[0]])
remainingIds = sorted(list(scanners.keys()))[1:]
knownScanners = { 0: Vector3(0, 0, 0) }

# For our known beacons, we want to calculate unique data for each beacon.
def getDistanceCombs(scannerId: int) -> Dict[int, Tuple[Vector3, Vector3]]:
    results = {}
    combs   = combinations(scanners[scannerId], r=2)

    for comb in combs:
        comb: Tuple[Vector3, Vector3]
        assert(len(comb) == 2)
        a, b = comb

        # Get the vector between these two points.
        vector : Vector3 = b - a
        magnitude = vector.magnitude

        if magnitude not in results:
            results[magnitude] = (a, b)

    return results

magnitudes = {}
magnitudes[0] = getDistanceCombs(0)

while remainingIds:
    scannerId = remainingIds.pop(0)

    for knownScannerId in magnitudes.keys():
        knownMagnitudes = magnitudes[knownScannerId]
        currMagnitudes  = getDistanceCombs(scannerId)

        overlap = set(knownMagnitudes.keys()).intersection(currMagnitudes.keys())
        if len(overlap) >= 12:
            # We know there are enough magnitudes that overlap.
            knownPositions = scanners[knownScannerId]

            for magnitude in overlap:
                currA,  currB  = currMagnitudes[magnitude]
                knownA, knownB = knownMagnitudes[magnitude]

                currVector00  = currB  - currA
                knownVector00 = knownB - knownA
                knownVector01 = knownA - knownB

                for swizzle in getSwizzles():
                    # We now need to swizzle the currVector until it matches the knownVector.
                    a = None
                    b = None
                    if currVector00.swizzle(swizzle) == knownVector00:
                        a = currA
                        b = currB
                    elif currVector00.swizzle(swizzle) == knownVector01:
                        a = currB
                        b = currA

                    if a and b:
                        # First, let's get a list of all of the positions after they have been swizzled.
                        positions = [x.swizzle(swizzle) for x in scanners[scannerId]]

                        a = a.swizzle(swizzle)
                        b = b.swizzle(swizzle)

                        # a is equivalent to knownA, and b is equivalent to knownB
                        # To get to (0, 0, 0) relative to the new scanner, we can invert the swizzled position.
                        scannerPos = knownA + -a

                        # Now that we know the scanner position, let's update the list of positions to be relative to scanner0.
                        positions = [x + scannerPos for x in positions]

                        # Now let's add them to our set of known positions.
                        [found.add(x) for x in positions]

                        # We need to update our list of positions by scanner.
                        scanners[scannerId] = set(positions)

                        # Add the new magnitudes in there.
                        magnitudes[scannerId] = getDistanceCombs(scannerId)

                        knownScanners[scannerId] = scannerPos

                        print(f"Found scanner {scannerId} - {scannerPos}")
                        break

                if scannerId in magnitudes: break
        if scannerId in magnitudes: break
    else:
        remainingIds.append(scannerId)

print(len(found))

# Part 2
combs     = combinations(knownScanners.values(), r = 2)
distances = set()
for comb in combs:
    a, b = comb
    vector = b - a
    manhattan = vector.manhattan
    distances.add(manhattan)

print(max(distances))