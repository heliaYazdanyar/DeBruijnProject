import math
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
        self.prop_fraction_space = np.zeros(2 ** len(binary_repr))
        self.CnA_fraction_space = np.zeros(2 ** len(binary_repr))
        self.src_items = set()

    def add_src_item(self, item_binary):
        self.src_items.add(item_binary)
        return

    def get_proportion(self):
        return len(self.src_items)

    def is_full(self):
        return len(self.items) >= self.capacity

    # recycle
    def remove_allItems(self):
        self.items = []
        return

    def __str__(self):
        return f"Node({self.binary_repr}, items={self.items})"

    # handling items
    def remove_item(self, item):
        self.items.remove(item)
        return

    def add_item(self, item):
        self.items.append(item)
        return

    # handling neighbors (children)
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

    # TODO
    def get_oldest_item(self):
        return

    def get_random_item(self):
        t = len(self.items)
        index = random.randint(0, t-1)
        return self.items[index]

    # fractional
    def allocate_space(self, src_index, dist):
        fraction = 2 ** (2 * dist - 1)
        space = math.ceil(self.capacity / fraction)
        # print("distace from ", self.index, " to ", src_index, " is=", dist)
        # print("allocated space from ", self.index, " to ", src_index, " is=", space)
        self.fraction_space[src_index] = space
        # print("Node ", self.index, "allocated= ", space, " to src ", src_index)
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

    def remove_item_fractional(self, network, item):
        root = network._find_root_node(item)
        self.items.remove(item)
        self.fraction_space[root.index] -= 1
        return

    # proportional
    def allocate_prop_fractional(self, src_index, dist, proportion):
        fraction = 2 ** (2 * dist - 1)
        space = math.ceil(self.capacity / fraction) * proportion
        self.prop_fraction_space[src_index] = space
        # print(self.prop_fraction_space)
        # print("-------------")
        return

    def prop_fraction_is_full(self, src_index):
        return not (self.prop_fraction_space[src_index] > 0)

    def prop_fractional_add_item(self, src_index, item):
        self.items.append(item)
        self.prop_fraction_space[src_index] -= 1
        return

    # CnA fractional
    def CnA_first_allocation(self, network):
        for item in self.items:
            root = network._find_root_node(item.binary_repr)
            self.CnA_fraction_space[root.index] += 1
        return

    def CnA_remaining_allocation(self, network):
        added_fraction_factor = 1.1
        self.capacity = math.ceil(self.capacity * added_fraction_factor)
        remaining_space = self.capacity - len(self.items)
        for i in range(0, network.num_nodes):
            dist = network.server_distances[self.index][i]
            fraction = 2 ** (2 * dist - 1)
            c = math.ceil(remaining_space / fraction)
            self.CnA_fraction_space[i] += c
        return

    def CnA_fraction_is_full(self, src_index):
        if self.CnA_fraction_space[src_index] > 0:
            return False
        return True

    def CnA_fractional_add_item(self,network, item):
        root = network._find_root_node(item.binary_repr)
        self.items.append(item)
        self.CnA_fraction_space[root.index] -= 1
        return

    def CnA_remove_item(self, network, item):
        root = network._find_root_node(item.binary_repr)
        self.items.remove(item)
        self.CnA_fraction_space[root.index] += 1
        return
    # global routing TODO
    def add_to_global_table(self, item, host):
        return

    def remove_from_global_table(self, item):
        return

    def check_global_table(self, item):
        return