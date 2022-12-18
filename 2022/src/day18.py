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
surface_area = 0
min_x, max_x, min_y, max_y, min_z, max_z = 500, 0, 500, 0, 500, 0
for point in points:
    x, y, z = point
    max_x = max(max_x, x)
    max_y = max(max_y, y)
    max_z = max(max_z, z)
    min_x = min(min_x, x)
    min_y = min(min_y, y)
    min_z = min(min_z, z)

max_x, max_y, max_z = max_x + 1, max_y + 1, max_z + 1
min_x, min_y, min_z = min_x - 1, min_y - 1, min_z - 1
way_outside_point = (max_x, max_y, max_z)
valid_neighbors = set()
invalid_neighbors = set()
for idx, point in enumerate(points):
    x, y, z = point
    neighbors = set([ (x + 1, y, z), ( x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1) ])

    # def aStar(grid, start, goal, heuristic, adjFunc, scoreFunc, metGoalFunc=None, printStateFunc=None):
    def heuristic(neighbor):
        if neighbor in valid_neighbors: return 1
        x, y, z = neighbor
        if x < min_x or y < min_y or z < min_z or x > max_x or y > max_y or z > max_z:
            return 1000000000000000000
        else:
            return 1000000000000000000 if neighbor in points else 1
    def adjFunc(data):
        _, current = data
        x, y, z = current
        return set([ (x + 1, y, z), ( x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1) ])
    def scoreFunc(grid, current, neighbor):
        if neighbor in valid_neighbors: return 1
        if current in points: return 1000000000000000000
        if neighbor in points: return 1000000000000000000
        x, y, z = neighbor
        if x < min_x or y < min_y or z < min_z or x > max_x or y > max_y or z > max_z:
            return 1000000000000000000
        return 1
    for neighbor in neighbors:
        if neighbor in invalid_neighbors:
            continue
        if neighbor not in valid_neighbors:
            best_path = aStar(None, way_outside_point, neighbor, heuristic, adjFunc, scoreFunc)
        else:
            best_path = []
        if best_path is None:
            invalid_neighbors.add(neighbor)
            continue
        intersection = points.intersection(set(best_path))
        if len(intersection) == 0:
            for item in best_path:
                valid_neighbors.add(item)
            valid_neighbors.add(neighbor)
            surface_area += 1
print(surface_area)