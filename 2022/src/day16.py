from shared import *
import networkx as nx

# Input data is in INPUT_DATA.
# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
INPUT_DATA = [parse("Valve {} has flow rate={:d}; {} to {} {}", x) for x in INPUT_DATA]

valves = {}
valves_with_rates = []
rates  = {}

G = nx.Graph()

for data in INPUT_DATA:
    valve, rate, _, __, others = data

    G.add_node(valve)
    valves[valve] = others.split(", ")
    rates[valve] = rate

    if rate > 0:
        valves_with_rates.append(valve)

for valve, others in valves.items():
    for other in others:
        G.add_edge(valve, other)

distances = {}
for valve in G.nodes():
    for other in G.nodes():
        distances[(valve, other)] = nx.shortest_path_length(G, valve, other)


# DP stands for Dynamic Programming
# Set up the size of the DP lookup table, and initialize some defaults
dp = {}
for i in range(0, 31):
    dp[i] = {}
    for valve in valves_with_rates + ['AA']:
        dp[i][valve] = defaultdict(lambda: -999999999)

for i, valve in enumerate(valves_with_rates):
    distance = distances[("AA", valve)]
    dp[distance + 1][valve][1 << i] = 0

# Determine how much flow is active right now from the mask specified.
def get_flow(mask):
    flow = 0
    for i in range(0, len(valves_with_rates)):
        if ((1 << i) & mask) != 0:
            flow += rates[valves_with_rates[i]]
    return flow

max_seen = 0

# If you're not familiar, the idea is to have one dimension in a DP table that represents a subset of items
# out of the group, stored as a bitmask. In my implementation, that was the final axis, with the full
# DP table being defined by:
#
#dp[i][k][j] = maximum amount of pressure released at minute i, standing at
#              location k, with the valves marked in bitset j opened

# To make this reasonably-sized, we can reduce the set of locations to only those that have valves with nonzero flow.
# In my input there were 15 of these, so this table isn't too big, only M x N x 2N where M = 31 and N = 15.
# There are two possible transitions:
#     - either we can do nothing for a minute and gain value equal to the pressure of all opened valves
#       (a transition from dp[i][k][j] to dp[i+1][k][j], where our current valve is open (1 << k) & j != 0) or
#     - we can move to a location (l) with an unopened valve (1 << l) & j == 0) and open it
#       (a transition from dp[i][k][j] to dp[i+dist(k,l)+1][l][j | (1 << l)].
# There are N + 1 total transitions, so the overall complexity is O(M * N^2 * 2^N)
# (assuming you precompute the pairwise distances), which is totally workable with M = 31 and N = 15.

max_val = 1 << len(valves_with_rates)
for i in range(1, 31): # clock
    for j in range(0, max_val): # which valves are open
        for k, current in enumerate(valves_with_rates): # which space we're standing in
            flow = get_flow(j)

            stay = dp[i-1][current][j] + flow

            # If the flow we gain by standing still is more than what we've currently tracked,
            # track is as the next best to use.
            if stay > dp[i][current][j]:
                dp[i][current][j] = stay

            max_seen = max(max_seen, dp[i][current][j])

            if ((1 << k) & j) == 0:
                # This current valve is unopened, we've gotten all the flow from it we can.
                continue

            for possible, valve in enumerate(valves_with_rates):
                if ((1 << possible) & j) != 0:
                    # This possible valve is already opened.
                    # No reason to go visit it again.
                    continue

                distance = distances[(current, valve)]

                if i + distance + 1 >= 31:
                    # We've exceeded our time limit.
                    # Skip.
                    continue

                value = dp[i][current][j] + flow * (distance + 1)

                # If the flow we'd gain by going to the new location (valve) is more than what we've tracked,
                # then track it as the best we've seen so far for this combination.
                if value > dp[i + distance + 1][valve][j | 1 << possible]:
                    dp[i + distance + 1][valve][j | 1 << possible] = value

# Part 1
print(max_seen)

# Part 2
# For part 2, we can reuse the DP table and just have ourself and the elephant pick two disjoint sets of valves to open,
# j1 and j2, and then the flow will be max over k in j1 (dp[26][k][j1]) +
# max over k in j2 (dp[26][k][j2]).
# Looping over all options is O(N^2 * 2^N).

max_seen = 0
for elephant_mask in range(0, max_val):
    # We only need to loop over the maximum number of valid values.
    max_me_mask = 1 if elephant_mask == 0 else ((1 << int(math.log(elephant_mask, 2))) + 1)
    for me_mask in range(0, max_me_mask):
        if (elephant_mask & me_mask) != me_mask:
            continue

        me       = -999999999
        elephant = -999999999

        for valve in valves_with_rates:
            me = max(me, dp[26][valve][me_mask])
            elephant = max(elephant, dp[26][valve][elephant_mask & ~me_mask])

        max_seen = max(max_seen, me + elephant)

print(max_seen)