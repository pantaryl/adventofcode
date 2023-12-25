from shared import *
import networkx as nx
#import matplotlib.pyplot as plt

INPUT_DATA = [x for x in INPUT_DATA]

#connections = defaultdict(set)

G = nx.Graph()

for line in INPUT_DATA:
    left, right = line.split(": ")
    right_options = right.split(" ")

    for option in right_options:
        #if left in ('txm', 'fdb') and option in ('txm', 'fdb'):
        #    continue
        #if left in ('mnl', 'nmz') and option in ('mnl', 'nmz'):
        #    continue
        #if left in ('jpn', 'vgf') and option in ('jpn', 'vgf'):
        #    continue

        #connections[left].add(option)
        #connections[option].add(left)
        G.add_edge(left, option)

# I initially visualized this using networkx and matplotlib.
#    nx.draw_networkx(G)
#    plt.show()
#    left = set()
#    stack = [ 'txm' ]
#    while stack:
#        current = stack.pop()
#        if current in left: continue
#
#        left.add(current)
#
#        for item in connections[current]:
#            stack.append(item)
#
#    right = set()
#
#    stack = ['fdb']
#    while stack:
#        current = stack.pop()
#        if current in right: continue
#
#        right.add(current)
#
#        for item in connections[current]:
#            stack.append(item)
#
#    print(len(left) * len(right))

# After reading more, it seems that networkx has the ability to find the minimum
# number of cuts to disconnect the full graph.
cuts = nx.minimum_edge_cut(G)
G.remove_edges_from(cuts)

print(math.prod((len(x) for x in nx.connected_components(G))))