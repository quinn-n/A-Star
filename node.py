
import math

class Node:
    """Class to manage a node's data"""
    def __init__(self, pos, walkable=True):
        self.parent = None
        self.walkable = walkable

        self.g = math.inf
        self.h = math.inf
        self.f = math.inf

        self.pos = pos

        self.closed = False
    
    def calc_f(self):
        """Calculates f and stores it in the internal buffer"""
        self.f = self.g + self.h
    
    def calc_h(self, target: tuple):
        """Calculates h with a given target pos"""
        self.h = dist(self.pos, target)
    
    def __eq__(self, other):
        return type(self) == type(other) and self.pos == other.pos

def dist(a: tuple, b: tuple):
    """Returns the distance between two points"""
    x_diff = a[0] - b[0]
    y_diff = a[1] - b[1]
    return x_diff ** 2 + y_diff ** 2
