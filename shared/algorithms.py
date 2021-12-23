from .classes import OrderedComplex
import heapq, sys
from collections import defaultdict, deque

def memoize(f):
    memo = {}
    def helper(index, *args):
        if index not in memo:
            memo[index] = f(index, *args)
        return memo[index]
    return helper

def aStar(grid, start, goal, heuristic, adjFunc, scoreFunc, metGoalFunc=None, printStateFunc=None):
    def reconstructPath(path, current):
        totalPath = deque([ current ])
        while current in path:
            current = path[current]
            totalPath.appendleft(current)
            current = current
        return totalPath

    discovered = [(0, start)]
    heapq.heapify(discovered)
    path       = {}

    gScore     = defaultdict(lambda: sys.maxsize)
    gScore[start] = 0

    while discovered:
        current = heapq.heappop(discovered)[1]

        if printStateFunc: printStateFunc(current)
        if metGoalFunc:
            if metGoalFunc(current, goal):
                return reconstructPath(path, current)
        elif current == goal:
            return reconstructPath(path, current)

        for neighbor in adjFunc((grid, current)):
            tentativeGScore = gScore[current] + scoreFunc(grid, current, neighbor)
            if tentativeGScore < gScore[neighbor]:
                # This path to neighbor is better than any previous one.
                gScore[neighbor] = tentativeGScore
                fScore = tentativeGScore + heuristic(neighbor)
                path[neighbor] = current
                priority = (fScore, neighbor)
                if priority not in discovered:
                    heapq.heappush(discovered, priority)

    return None