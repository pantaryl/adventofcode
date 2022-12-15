from shared import *

# Input data is in INPUT_DATA.
# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
INPUT_DATA = [parse("Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}", x) for x in INPUT_DATA]

beacons = set()
sensors = []
grid = set()
for data in INPUT_DATA:
    x1, y1, x2, y2 = data

    sensor = complex(x1, y1)
    beacon = complex(x2, y2)

    sensors.append((sensor, beacon))
    beacons.add(beacon)

def get_total_per_y(y_val):
    num_spots = []
    for i, data in enumerate(sensors):
        sensor, beacon = data
        distance = manhattanDistance(sensor, beacon)
        new_distance = manhattanDistance(sensor, complex(sensor.real, y_val))

        if new_distance <= distance:
            num_in_row = ((distance * 2) + 1) - (2 * new_distance)
            half       = num_in_row // 2
            x1         = int(sensor.real) - half
            x2         = int(sensor.real) + half

            num_spots.append([x1, x2])

    intervals = mergeIntervals(num_spots)
    total_count = sum([abs(x1 - x2) + 1 for x1, x2 in intervals])
    for beacon in beacons:
        if int(beacon.imag) == y_val:
            total_count -= 1
    for sensor, _ in sensors:
        if int(sensor.imag) == y_val:
            total_count -= 1
    return intervals, total_count

# Part 1
y_val = 2000000
print(get_total_per_y(y_val)[1])

# Part 2
# Determine min/max x/y
problem_y = 4000000
min_x, max_x, min_y, max_y = problem_y, 0, problem_y, 0
for sensor, beacon in sensors:
    distance = manhattanDistance(sensor, beacon)
    min_x = min(min_x, int(sensor.real) - distance)
    max_x = max(max_x, int(sensor.real) + distance)
    min_y = min(min_y, int(sensor.imag) - distance)
    max_y = max(max_y, int(sensor.imag) + distance)

min_y = max(min_y, 0)
max_y = min(max_y, problem_y)

for y in range(min_y, max_y + 1):
    intervals, total_count  = get_total_per_y(y)
    total_in_range = sum([overlap_1d(x1, x2, 0, problem_y) for x1, x2 in intervals])

    # range of [0, problem_y] is a total of problem_y + 1
    # we're looking for the only y where we're off of the total by 1,
    # which is when total_in_range is equal to problem_y
    if total_in_range == problem_y:
        print("x", intervals[0][1] + 1, "y", y, "tuning frequency", ((intervals[0][1] + 1) * 4000000) + y)
        break

