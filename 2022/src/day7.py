from shared import *

# Input data is in INPUT_DATA.
INPUT_DATA = [x for x in INPUT_DATA]

dir         = { '/' : { 'parent' : None, '_id': '/', '_files': set() }, 'parent': None, '_files': set() }
current_dir = dir['/']
sizes = defaultdict(set)
# Part 1
i = 0
while i < len(INPUT_DATA):
    line = INPUT_DATA[i]
    if line.startswith('$'):
        # this is a command
        if "$ cd" in line:
            if "cd .." in line:
                current_dir = current_dir['parent']
            elif "cd /" in line:
                current_dir = dir["/"]
            else:
                new_dir = line.split("$ cd ")[1]
                if new_dir not in current_dir:
                    assert()
                    current_dir[new_dir] = { 'parent' : current_dir, '_id' : new_dir, '_files': set() }
                current_dir = current_dir[new_dir]
        elif "$ ls" in line:
            i += 1
            while i < len(INPUT_DATA):
                line = INPUT_DATA[i]
                if line.startswith('$'):
                    i -= 1
                    break
                else:
                    if line.startswith('dir'):
                        dir_name = line.split(' ')[1]
                        if dir_name not in current_dir:
                            current_dir[dir_name] = { 'parent' : current_dir, "_id" : dir_name, '_files': set() }
                        if '_has_dir' not in current_dir:
                            current_dir['_has_dir'] = True
                    else:
                        size, filename = line.split(' ')
                        size = int(size)
                        current_dir['_files'].add((filename, size))
                    i += 1
    i += 1

total_sizes = defaultdict(int)
def get_size(current_dir: dict, indent, path):
    total = 0

    _id = current_dir['_id']

    if path in total_sizes:
        return total_sizes[path]

    for key, item in current_dir.items():
        if key in ['parent', '_id', '_has_dir', '_files']:
            pass
        elif isinstance(item, dict):
            total += get_size(item, indent + 1, path + f"/{key}")

    files = current_dir['_files']
    total += sum([x[1] for x in files])

    total_sizes[path] = total

    return total

get_size(dir['/'], 0, '/')
print(sum([x for _, x in total_sizes.items() if x <= 100000]))

# Part 2
disk_space = 70000000
needed_unused = 30000000
remaining_space = disk_space - total_sizes['/']

options = sorted([(x, remaining_space + x) for _, x in total_sizes.items() if remaining_space + x > needed_unused],
                 key=lambda x: x[1])
print(options[0][0])
