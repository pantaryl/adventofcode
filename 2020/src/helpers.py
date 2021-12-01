def memoize(f):
    memo = {}
    def helper(index, *args):
        if index not in memo:
            memo[index] = f(index, *args)
        return memo[index]
    return helper


class LLNode:
    def __init__(self, val):
        self.val  = val
        self.next = None