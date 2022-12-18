from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [parse("{:d},{:d},{:d}", x) for x in INPUT_DATA]

# Part 1
points = set()

for x, y, z in INPUT_DATA:
    points.add((x, y, z))

surface_area = 0
for point in points:
    x, y, z = point
    neighbors = set([ (x + 1, y, z), ( x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1) ])
    intersection = points.intersection(neighbors)

    surface_area += len(neighbors) - len(intersection)

print(surface_area)

# Part 2
# Use a flood-fill BFS to determine all coords of air that are not lava that can be reached from a "way outside point".
# Then calculate the surfaces adjacent to these coords.
# Anything completely surrounded by lava will be unreachable by the flood-fill.
min_x, max_x, min_y, max_y, min_z, max_z = 500, 0, 500, 0, 500, 0
for point in points:
    x, y, z = point
    max_x = max(max_x, x)
    max_y = max(max_y, y)
    max_z = max(max_z, z)
    min_x = min(min_x, x)
    min_y = min(min_y, y)
    min_z = min(min_z, z)

max_x, max_y, max_z = max_x + 2, max_y + 2, max_z + 2
min_x, min_y, min_z = min_x - 2, min_y - 2, min_z - 2
way_outside_point = (max_x, max_y, max_z)

valid_neighbors = set()
seen = { way_outside_point }
stack = deque([ way_outside_point ])

while stack:
    point = stack.popleft()
    x, y, z = point

    neighbors = { (x + 1, y, z), ( x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1) }

    for neighbor in neighbors:
        nx, ny, nz = neighbor
        if neighbor in seen or nx < min_x or ny < min_y or nz < min_z or nx > max_x or ny > max_y or nz > max_z:
            seen.add(neighbor)
            continue

        if neighbor in points:
            valid_neighbors.add(point)
        else:
            stack.append(neighbor)
            seen.add(neighbor)

surface_area = 0
for valid in valid_neighbors:
    x, y, z = valid
    neighbors = { (x + 1, y, z), ( x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1) }

    for neighbor in neighbors:
        if neighbor in points:
            surface_area += 1

print(surface_area)