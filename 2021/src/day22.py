from shared import *

# Input data is in INPUT_DATA.
#INPUT_DATA = [int(x) for x in INPUT_DATA]

# Part 1
cubes = set()

for i, line in enumerate(INPUT_DATA):
    on, xStart, xEnd, yStart, yEnd, zStart, zEnd = tuple(parse.parse("{} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}", line).fixed)

    on = on == 'on'
    if xStart >= -50 and xEnd <= 50 and yStart >= -50 and yEnd <= 50 and zStart >= -50 and zEnd <= 50:
        for x in range(xStart, xEnd + 1):
            for y in range(yStart, yEnd + 1):
                for z in range(zStart, zEnd + 1):
                    if on:
                        cubes.add((x, y, z))
                    else:
                        cubes.discard((x, y, z))

print(len(cubes))

# Part 2
rules  = []
for line in INPUT_DATA:
    on, xStart, xEnd, yStart, yEnd, zStart, zEnd = tuple(parse.parse("{} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}", line).fixed)
    on = on == 'on'

    # Add an extra (+1, +1, +1) to the end so that the length of each edge of the cube, when calculated, is correct.
    # We also want to add the (+1, +1, +1) here so we don't accidentally recursively add it more than once.
    rules.append((on, Vector3(xStart, yStart, zStart),  Vector3(xEnd + 1, yEnd + 1, zEnd + 1)))

onVolume = 0
for i, rule in enumerate(rules):
    on, start, end = rule

    # We're only tracking things that have turned on from this global loop. Things that have been turned off will be
    # considered for count().
    if not on: continue

    def count(data, rest):
        _, start, end = data

        # We want to track, from this cube, how many cubes of this are *never* touched by any other cube in a rule
        # following this.
        # The logic being that at some point, any overlapped spaces will be turned on and have no following rules to
        # turn them off.
        conflicts = []

        for nextRule in rest:
            mOn, mStart, mEnd = nextRule

            # If this rule doesn't intersect, don't bother looking at it.
            if mEnd.x <= start.x or mStart.x >= end.x or \
               mEnd.y <= start.y or mStart.y >= end.y or \
               mEnd.z <= start.z or mStart.z >= end.z:
                continue

            # Determine what overlaps. This calculates the bounding box of the intersection.
            cStart = Vector3(max(mStart.x, start.x), max(mStart.y, start.y), max(mStart.z, start.z))
            cEnd   = Vector3(min(mEnd.x,   end.x),   min(mEnd.y, end.y),     min(mEnd.z, end.z))

            # Add the conflicting intersection to the list of conflicts.
            conflicts.append((mOn, cStart, cEnd))

        # Calculate the size of this box, ignoring any future intersections.
        # This calculation already handles the (+1, +1, +1) necessary to get the proper edge lengths.
        size   = end - start
        volume = size.x * size.y * size.z

        # For every conflict cube, determine which conflicts actually matter via the same mechanism as above.
        # This will determine how many unique cubes (in volume) this one rule actually turns on.
        for j, conflict in enumerate(conflicts):
            volume -= count(conflict, conflicts[j + 1:])

        return volume

    # Add up the unique volume enabled by this specific rule.
    onVolume += count(rule, rules[i + 1:])

print(onVolume)