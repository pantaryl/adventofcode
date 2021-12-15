class LLNode:
    def __init__(self, val):
        self.val  = val
        self.next = None


# OrderedComplex is defined so that a complex number can be sorted in a heapq.
class OrderedComplex(complex):
    def __new__(*args):
        return complex.__new__(*args)

    def __lt__(self, other):
        return self.real < other.real and self.imag < other.imag
    def __gt__(self, other):
        return self.real > other.real and self.imag > other.imag
