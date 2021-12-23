from copy import deepcopy
import math

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

    def __add__(self, other):
        return OrderedComplex(complex(self.real, self.imag) + complex(other.real, other.imag))

    def __sub__(self, other):
        return OrderedComplex(complex(self.real, self.imag) - complex(other.real, other.imag))

class Vector3:
    x: int
    y: int
    z: int

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __floordiv__(self, other):
        return Vector3(self.x // other.x, self.y // other.y, self.z // other.z)

    def __neg__(self):
        return self * Vector3(-1, -1, -1)

    def __abs__(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash(self.z)

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __lt__(self, other):
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __getitem__(self, item):
        if item == 0: return self.x
        if item == 1: return self.y
        if item == 2: return self.z

    def __setitem__(self, key, value):
        if key == 0: self.x = value
        elif key == 1: self.y = value
        elif key == 2: self.z = value
        else: assert()

    def swizzle(self, direction):
        newVec = Vector3()
        for axis in [0, 1, 2]:
            if 'x' in direction[axis]:
                newVec[axis] = self.x
            elif 'y' in direction[axis]:
                newVec[axis] = self.y
            elif 'z' in direction[axis]:
                newVec[axis] = self.z

            if '-' in direction[axis]:
                newVec[axis] = -newVec[axis]
        return newVec

    def deswizzle(self, direction):
        newVec = Vector3()
        for axis in [0, 1, 2]:
            if 'x' in direction[axis]:
                newVec.x = self[axis]
                if '-' in direction[axis]: newVec.x = -newVec.x
            elif 'y' in direction[axis]:
                newVec.y = self[axis]
                if '-' in direction[axis]: newVec.y = -newVec.y
            elif 'z' in direction[axis]:
                newVec.z = self[axis]
                if '-' in direction[axis]: newVec.z = -newVec.z
        return newVec

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    @property
    def manhattan(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    @staticmethod
    def Zero():
        return Vector3(0, 0, 0)