import random
import numpy as np

class Node:
    capacity = 0
    neighbors = []
    items = []
    binary_repr = ""
    index = -1

    # for global routing
    global_table = {}

    def __init__(self, binary_repr, capacity=4, index=-1):
        self.binary_repr = binary_repr
        self.items = []
        self.capacity = capacity
        self.neighbors = []
        self.left = None
        self.right = None
        self.index = index
        self.fraction_space = np.zeros(2 ** len(binary_repr))


    def is_full(self):
        return len(self.items) >= self.capacity

    def __str__(self):
        return f"Node({self.binary_repr}, items={self.items})"

    def add_item(self, item):
        self.items.append(item)
        return

    # handling neighbors
    def set_left(self, leftNode):
        self.left = leftNode
        self.neighbors.append(leftNode)
        return

    def set_right(self, rightNode):
        self.right = rightNode
        self.neighbors.append(rightNode)
        return

    # checking
    def contains_item(self, item):
        if item in self.items:
            return True
        return False

    # online functions
    def remove_item(self, item):
        self.items.remove(item)
        return

    def get_oldest_item(self):
        return

    def get_random_item(self):
        t = len(self.items)
        index = random.randint(0, t-1)
        return self.items[index]

    # fractional
    def allocate_space(self, src_index, dist):
        fraction = 2 ** (2 * dist - 1)
        space = int(self.capacity / fraction)
        # print("distace from ", self.index, " to ", src_index, " is=", dist)
        # print("allocated space from ", self.index, " to ", src_index, " is=", space)
        self.fraction_space[src_index] = space
        return

    def pick_remaining_space(self, index):
        k = self.capacity - np.sum(self.fraction_space)
        if k > 0:
            self.fraction_space[index] += k
        return

    def fraction_is_full(self, src_index):
        if self.fraction_space[src_index] > 0:
            return False
        return True

    def fractional_add_item(self, src_index, item):
        self.items.append(item)
        self.fraction_space[src_index] -= 1
        return

    # global routing

    def add_to_global_table(self, item, host):
        return

    def remove_from_global_table(self, item):
        return

    def check_global_table(self, item):
        return