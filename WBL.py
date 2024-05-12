import numpy as np


# With Bounded Loads (WBL) Model

# Nodes in WBL
class WBL_Node:
    capacity = 0
    neighbors = []
    items = []
    binary_repr = ""
    index = -1

    def __init__(self, binary_length,  index, capacity=4):
        self.items = [] # list of items (object)
        self.capacity = capacity
        self.binary_length = binary_length
        self.neighbors = []
        self.child = None
        self.index = index
        # binary representation of a node is the conversion of its decimal index to binary representation
        self.binary_repr = self.decimalToBinary(index)

    def decimalToBinary(self, number):
        binary = bin(number).replace("0b", "")
        l = len(binary)
        for i in range(0, self.binary_length - l):
            binary = "0"+binary
        return binary

    def is_full(self):
        return len(self.items) >= self.capacity

    def add_item(self, item):
        self.items.append(item)
        return

    # handling neighbors
    def set_child(self, node):
        self.child = node
        self.neighbors.append(node)
        return

    # checking
    def contains_item(self, item):
        if item in self.items:
            return True
        return False


class WBL_Network:
    num_nodes = 0
    nodes = []
    server_distances = []

    def __init__(self, log_num_nodes, node_cap):
        self.binary_len = log_num_nodes
        self.num_nodes = 2 ** log_num_nodes

        # nodes
        self.nodes = [WBL_Node(log_num_nodes, index=i) for i in range(self.num_nodes)]
        for i in range(0, self.num_nodes):
            thisNode = self.nodes[i]
            if i == self.num_nodes-1:
                _child = self.nodes[0]
            else:
                _child = self.nodes[i+1]

            thisNode.set_child(_child)
            thisNode.capacity = node_cap

        # other initializing
        self.all_dist()
        return

    # distance of nodes
    def all_dist(self):
        self.server_distances = np.zeros((self.num_nodes, self.num_nodes))

        # distance of two nodes in WBL is calculated with their indexes
        for i in range(0, self.num_nodes):
            for j in range(0, self.num_nodes):
                self.server_distances[i][j] = (j - i + self.num_nodes) % self.num_nodes

        return

    def _find_root_node(self, item_binary):
        starting_hash = item_binary[0:self.binary_len]
        for i in range(0, self.num_nodes):
            if self.nodes[i].binary_repr == starting_hash:
                return self.nodes[i]
        return -1

    # greedy allocations
    def find_place_greedy(self, item):
        item_binary = item.binary_repr
        cnt = 1
        root = self._find_root_node(item_binary)

        if not root.is_full():
            root.add_item(item)
            return cnt

        index = root.index
        cnt += 1
        curr_node = root.child
        while True:
            if cnt > self.num_nodes:
                print("Network is full")

            if not curr_node.is_full():
                curr_node.add_item(item)
                return cnt

            else:
                curr_node = curr_node.child

            index = (index + 1) % len(item_binary)
            cnt += 1
        return cnt

    # greedy access
    def access(self, item):
        item_binary = item.binary_repr
        cnt = 1
        root = self._find_root_node(item_binary)

        if root.contains_item(item):
            return cnt

        index = root.index
        cnt += 1
        curr_node = root.child
        while True:
            if cnt > self.num_nodes:
                print("Network is full")

            if curr_node.contains_item(item):
                return cnt

            else:
                curr_node = curr_node.child

            index = (index + 1) % len(item_binary)
            cnt += 1
        return cnt


