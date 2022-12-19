from shared import *

# Input data is in INPUT_DATA.
# Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
INPUT_DATA = [parse("Blueprint {:d}: Each ore robot costs {:d} ore. Each clay robot costs {:d} ore. "
                    "Each obsidian robot costs {:d} ore and {:d} clay. Each geode robot costs {:d} ore and {:d} obsidian.", x) for x in INPUT_DATA]

class Blueprint:
    def __init__(self, id):
        self.id = id
        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geode = 0

    def __repr__(self):
        return f"{self.id} - O{self.ore}, C{self.clay}, Ob{self.obsidian}, G{self.geode}"

    @property
    def max_ore_spend(self):
        return max(self.ore, self.clay, self.obsidian[0], self.geode[0])

blueprints = []
for i, blueprint in enumerate(INPUT_DATA, 1):
    id, ore, clay, obsid_ore, obsid_clay, geode_ore, geode_obsid  = blueprint
    assert(id == i)

    bp = Blueprint(id)
    bp.ore = ore
    bp.clay = clay
    bp.obsidian = (obsid_ore, obsid_clay)
    bp.geode = (geode_ore, geode_obsid)
    blueprints.append(bp)

def run_sim_2(blueprint: Blueprint, max_tick: int):
    max_val = 0
    stack   = [(1, 1, 0, 0, 0, 0, 0, 0, 0)]
    seen    = set()

    while stack:
        state = stack.pop()

        tick, num_ore_r, num_ore, num_clay_r, num_clay, num_obsid_r, num_obsid, num_geode_r, num_geode = state

        if tick == max_tick:
            max_val = max(max_val, num_geode)
            #results[state] = num_geode
            continue

        remaining_ticks = max_tick - tick
        if num_ore >=  (remaining_ticks * blueprint.max_ore_spend) - (num_ore_r * (remaining_ticks - 1)):
            num_ore = (remaining_ticks * blueprint.max_ore_spend) - (num_ore_r * (remaining_ticks - 1))
        if num_clay >= (remaining_ticks * blueprint.obsidian[1]) - (num_clay_r * (remaining_ticks - 1)):
            num_clay = (remaining_ticks * blueprint.obsidian[1]) - (num_clay_r * (remaining_ticks - 1))
        if num_obsid >= (remaining_ticks * blueprint.geode[1]) - (num_obsid_r * (remaining_ticks - 1)):
            num_obsid = (remaining_ticks * blueprint.geode[1]) - (num_obsid_r * (remaining_ticks - 1))


        state = (tick, num_ore_r, num_ore, num_clay_r, num_clay, num_obsid_r, num_obsid, num_geode_r, num_geode)
        if state in seen: continue
        seen.add(state)

        # We have 5 options. We can build one of any robot, or we can wait.

        if num_ore >= blueprint.geode[0] and num_obsid >= blueprint.geode[1]:
            # Add an option to build a geode
            stack.append((
                tick + 1,
                num_ore_r,
                num_ore - blueprint.geode[0] + num_ore_r,
                num_clay_r,
                num_clay + num_clay_r,
                num_obsid_r,
                num_obsid - blueprint.geode[1] + num_obsid_r,
                num_geode_r + 1,
                num_geode + num_geode_r
            ))
        if num_ore >= blueprint.obsidian[0] and num_clay >= blueprint.obsidian[1] and num_obsid_r < blueprint.geode[1]:
            # Add an option to build an obsidian
            stack.append((
                tick + 1,
                num_ore_r,
                num_ore - blueprint.obsidian[0] + num_ore_r,
                num_clay_r,
                num_clay - blueprint.obsidian[1] + num_clay_r,
                num_obsid_r + 1,
                num_obsid + num_obsid_r,
                num_geode_r,
                num_geode + num_geode_r
            ))
        if num_ore >= blueprint.clay and num_clay_r < blueprint.obsidian[1]:
            # Add an option to build an clay
            stack.append((
                tick + 1,
                num_ore_r,
                num_ore - blueprint.clay + num_ore_r,
                num_clay_r + 1,
                num_clay + num_clay_r,
                num_obsid_r,
                num_obsid + num_obsid_r,
                num_geode_r,
                num_geode + num_geode_r
            ))
        if num_ore >= blueprint.ore and num_ore_r < blueprint.max_ore_spend:
            # Add an option to build an clay
            stack.append((
                tick + 1,
                num_ore_r + 1,
                num_ore - blueprint.ore + num_ore_r,
                num_clay_r,
                num_clay + num_clay_r,
                num_obsid_r,
                num_obsid + num_obsid_r,
                num_geode_r,
                num_geode + num_geode_r
            ))

        # Let's add wait last.
        stack.append((
            tick + 1,
            num_ore_r,
            num_ore + num_ore_r,
            num_clay_r,
            num_clay + num_clay_r,
            num_obsid_r,
            num_obsid + num_obsid_r,
            num_geode_r,
            num_geode + num_geode_r
        ))

    return max_val



# Part 1
total = 0
for blueprint in blueprints:
    result = run_sim_2(blueprint, 25)
    total += blueprint.id * result
print(total)

# Part 2
total = 1
for blueprint in blueprints[:3]:
    result = run_sim_2(blueprint, 33)
    total *= result
print(total)