from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]

seeds = [int(x) for x in INPUT_DATA[0].split(":")[1].split(" ") if x != ""]

seed_to_soil = {}
soil_to_fert = {}
fert_to_water = {}
water_to_light = {}
light_to_temp = {}
temp_to_humidity = {}
humidity_to_loc = {}

def get_data(idx):
    output = {}
    next_line_start = idx + 1
    next_line = INPUT_DATA[next_line_start]
    while next_line != "":
        dst_start, src_start, map_range = [int(x) for x in next_line.split(" ")]
        output[(src_start, map_range)] = dst_start

        next_line_start += 1

        if next_line_start >= len(INPUT_DATA):
            break
        next_line = INPUT_DATA[next_line_start]

    idx = next_line_start
    return idx, output

i = 2
while i < len(INPUT_DATA):
    line = INPUT_DATA[i]
    if line.startswith("seed-to-soil map:"):
        i, seed_to_soil = get_data(i)
    elif line.startswith("soil-to-fertilizer map:"):
        i, soil_to_fert = get_data(i)
    elif line.startswith("fertilizer-to-water map:"):
        i, fert_to_water = get_data(i)
    elif line.startswith("water-to-light map:"):
        i, water_to_light = get_data(i)
    elif line.startswith("light-to-temperature map:"):
        i, light_to_temp = get_data(i)
    elif line.startswith("temperature-to-humidity map:"):
        i, temp_to_humidity = get_data(i)
    elif line.startswith("humidity-to-location map:"):
        i, humidity_to_loc = get_data(i)
    i += 1

xlate = {
'seed_to_soil' : seed_to_soil,
'soil_to_fert' : soil_to_fert,
'fert_to_water' : fert_to_water,
'water_to_light' : water_to_light,
'light_to_temp' : light_to_temp,
'temp_to_humidity' : temp_to_humidity,
'humidity_to_loc' : humidity_to_loc,
}

@memoize
def get_value(id):
    num, type_name, inverted = id
    type = xlate[type_name]
    for key in type.keys():
        start, length = key
        dest = type[key]
        if inverted and dest <= num and num < dest + length:
            return start + (num - dest)
        elif inverted is False and start <= num and num < start + length:
            return type[key] + (num - start)

    return num

def get_loc(seed_num):
    soil_num = get_value((seed_num, 'seed_to_soil', False))
    fert_num = get_value((soil_num, 'soil_to_fert', False))
    water_num = get_value((fert_num, 'fert_to_water', False))
    light_num = get_value((water_num, 'water_to_light', False))
    temp_num  = get_value((light_num, 'light_to_temp', False))
    humidity_num = get_value((temp_num, 'temp_to_humidity', False))
    loc_num = get_value((humidity_num, 'humidity_to_loc', False))

    return loc_num

print(min([get_loc(x) for x in seeds]))

needed_ranges = list(zip(seeds[::2], seeds[1::2]))

def is_needed(seed_num):
    return any([start <= seed_num <= start + length for start, length in needed_ranges])

i = 0
while True:
    humidity_num = get_value((i, 'humidity_to_loc', True))
    temp_num = get_value((humidity_num, 'temp_to_humidity', True))
    light_num  = get_value((temp_num, 'light_to_temp', True))
    water_num = get_value((light_num, 'water_to_light', True))
    fert_num = get_value((water_num, 'fert_to_water', True))
    soil_num = get_value((fert_num, 'soil_to_fert', True))
    seed_num = get_value((soil_num, 'seed_to_soil', True))

    if i == 46:
        pass

    if is_needed(seed_num):
        print(i)
        break

    i += 1